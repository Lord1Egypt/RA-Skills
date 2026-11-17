#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ext4journal.py —— 通用 ext4 删除恢复库：日志环解析 + 数据块多版本索引 + inode/目录读取

设计原则
  1. 设备仅以只读方式打开（mmap PROT_READ），绝不写入、绝不挂载。
  2. 读取数据块时优先使用日志中的历史版本；日志中没有的块直接读原始磁盘
     —— 已释放但未被复用的块，内容通常仍然是删除前的有效数据。
  3. 事务顺序一律按 seq 号排序，不能按物理位置：日志环会绕回，两者不同序。

核心 API
    fs = Ext4FS('/dev/sdbX')
    fs.info()                       # 超级块要点
    js = JournalScanner(fs)
    js.build()                      # 解析日志环，建立 fs_block -> 版本列表 索引
    js.block_data(blk)              # 取某块的最佳内容 (bytes, source)
    js.inode_versions(ino)          # 某 inode 在日志中的所有历史版本
    js.best_inode(ino)              # 选出一个可用版本
    js.dir_entries(info)            # 列目录条目（含已删除条目）
    js.lookup_deleted(parent_ino, name)   # 在父目录中找被删条目 -> inode
    js.search_name(name)            # 全日志搜索某名字 -> [(block, seq, ino)]
"""
import os
import mmap
import struct
import collections

J_MAGIC = b"\xc0\x3b\x39\x98"
T_DESC, T_COMMIT, T_REVOKE, T_SB2 = 1, 2, 3, 4
F_ESCAPE, F_SAME_UUID, F_DELETED, F_LAST_TAG = 1, 2, 4, 8

S_IFMT, S_IFDIR, S_IFREG, S_IFLNK = 0o170000, 0o040000, 0o100000, 0o120000

MAX_NAME = 255


def now():
    import time
    return time.strftime("%F %T")


def fmt_ts(t):
    if 1_000_000_000 < t < 2_200_000_000:
        import datetime
        return datetime.datetime.fromtimestamp(t).strftime("%F %T")
    return str(t)


# ---------------------------------------------------------------- 基础
class Ext4FS:
    """只读 ext4 文件系统访问器"""

    def __init__(self, dev):
        self.dev = dev
        self.fd = os.open(dev, os.O_RDONLY)
        # 注意：块设备的 fstat().st_size 为 0，此时 mmap(length=0) 会报 EINVAL，
        # 必须先显式取得设备大小（/sys 或 BLKGETSIZE64），失败则退回 pread。
        size = self._device_size()
        try:
            self.mm = mmap.mmap(self.fd, size, prot=mmap.PROT_READ) if size else None
        except OSError:
            self.mm = None
        first = self._pread(1024, 1024)
        sb = first
        (self.inodes_count, self.blocks_count_lo, _rb, _fb, self.free_inodes,
         self.first_data_block, self.log_block_size) = struct.unpack("<7I", sb[0:28])
        (self.blocks_per_group, _cpg, self.inodes_per_group) = struct.unpack("<3I", sb[32:44])
        self.magic = struct.unpack("<H", sb[0x38:0x3A])[0]
        self.state = struct.unpack("<H", sb[0x3A:0x3C])[0]
        self.mtime = struct.unpack("<I", sb[0x2C:0x30])[0]
        self.wtime = struct.unpack("<I", sb[0x30:0x34])[0]
        self.lastcheck = struct.unpack("<I", sb[0x40:0x44])[0]
        self.first_ino = struct.unpack("<I", sb[0x54:0x58])[0]
        self.inode_size = struct.unpack("<H", sb[0x58:0x5A])[0]
        (self.feature_compat, self.feature_incompat,
         self.feature_ro_compat) = struct.unpack("<3I", sb[0x5C:0x68])
        self.uuid = sb[0x68:0x78]
        self.blocks_count = self.blocks_count_lo | \
            (struct.unpack("<I", sb[0x150:0x154])[0] << 32)
        self.block_size = 1024 << self.log_block_size
        self.per_block = self.block_size // self.inode_size
        self.has_64bit = bool(self.feature_incompat & 0x80)
        self.has_extents = bool(self.feature_incompat & 0x40)
        self.has_metadata_csum = bool(self.feature_ro_compat & 0x400)
        self._gdt = None
        if self.magic != 0xEF53:
            raise RuntimeError("%s 不是 ext2/3/4 文件系统 (magic=0x%X)" % (dev, self.magic))

    # ---------- 设备大小 / 原始读取 ----------
    def _device_size(self):
        try:
            st = os.fstat(self.fd)
            if st.st_size > 0:
                return st.st_size
        except OSError:
            pass
        name = os.path.basename(os.path.realpath(self.dev))
        try:
            with open("/sys/class/block/%s/size" % name) as fh:
                return int(fh.read().strip()) * 512
        except Exception:      # noqa: BLE001
            pass
        try:
            import fcntl
            import array
            buf = array.array("Q", [0])
            fcntl.ioctl(self.fd, 0x80081272, buf, True)   # BLKGETSIZE64
            return int(buf[0])
        except Exception:      # noqa: BLE001
            return 0

    def _pread(self, off, n):
        if self.mm is not None:
            return self.mm[off:off + n]
        return os.pread(self.fd, n, off)

    def read_block(self, b):
        return self._pread(b * self.block_size, self.block_size)

    def read_blocks(self, b, n):
        return self._pread(b * self.block_size, n * self.block_size)

    def valid_block(self, b):
        return 0 <= b < self.blocks_count

    # ---------- 组描述符 ----------
    def group_descs(self):
        """返回 [inode_table_block, ...]，下标即组号"""
        if self._gdt is not None:
            return self._gdt
        groups = (self.inodes_count + self.inodes_per_group - 1) // self.inodes_per_group
        dsz = 64 if self.has_64bit else 32
        # 4K 块：超级块在 block 0 的 1024..2048，GDT 从 block 1 开始；
        # 1K 块：超级块独占 block 1，GDT 从 block 2 开始
        if self.block_size == 1024:
            gdt_off = 2 * self.block_size
        else:
            gdt_off = self.block_size          # block 1
        raw = self.mm[gdt_off:gdt_off + groups * dsz]
        out = []
        for g in range(groups):
            d = raw[g * dsz:(g + 1) * dsz]
            lo = struct.unpack("<I", d[8:12])[0]
            hi = struct.unpack("<I", d[40:44])[0] if dsz == 64 and len(d) >= 44 else 0
            out.append(lo | (hi << 32))
        self._gdt = out
        return out

    def inode_location(self, ino):
        """返回 (表块号, 块内偏移)"""
        g = (ino - 1) // self.inodes_per_group
        idx = (ino - 1) % self.inodes_per_group
        tbl = self.group_descs()
        if g >= len(tbl):
            return None, None
        blk = tbl[g] + idx // self.per_block
        return blk, (idx % self.per_block) * self.inode_size

    def read_inode(self, ino):
        """读磁盘上的 inode（返回 (raw, info) 或 (None, None)）"""
        blk, off = self.inode_location(ino)
        if blk is None or not self.valid_block(blk):
            return None, None
        raw = self.read_block(blk)[off:off + self.inode_size]
        if len(raw) < self.inode_size:
            return None, None
        return raw, parse_inode(raw, self.inode_size)

    # ---------- 日志位置 ----------
    def journal_map(self):
        """返回 [(j_first, count, fs_first), ...]，即日志块号 -> fs 块号的分段映射"""
        raw, info = self.read_inode(8)
        if info is None:
            raise RuntimeError("无法读取日志 inode 8")
        segs = []
        j = 0
        if info["flags"] & 0x00080000:
            exts = extents_of(info, self)
            for (lblk, llen, pblk) in sorted(exts):
                if lblk != j:
                    break
                segs.append((j, llen, pblk))
                j += llen
        else:
            blkmap = legacy_blocks(info)
            for pblk in blkmap:
                if not pblk:
                    break
                segs.append((j, 1, pblk))
                j += 1
        if not segs:
            raise RuntimeError("日志 inode 无数据块")
        return segs

    def info_lines(self):
        groups = (self.inodes_count + self.inodes_per_group - 1) // self.inodes_per_group
        return [
            ("设备", self.dev),
            ("块大小", "%d 字节" % self.block_size),
            ("块总数", "%d (%.1f GiB)" % (self.blocks_count, self.blocks_count * self.block_size / 2**30)),
            ("inode 数", "%d (inode 大小 %d)" % (self.inodes_count, self.inode_size)),
            ("每组 inode", self.inodes_per_group),
            ("块组数", groups),
            ("UUID", "-".join("%02x" % c for c in self.uuid)),
            ("文件系统状态", "clean" if self.state == 1 else "not-clean (%d)" % self.state),
            ("features incompat", "0x%08x" % self.feature_incompat),
            ("64bit/extents/csum", "%s/%s/%s" % (self.has_64bit, self.has_extents, self.has_metadata_csum)),
            ("最后挂载时间", fmt_ts(self.mtime)),
            ("最后写入时间", fmt_ts(self.wtime)),
        ]


# ---------------------------------------------------------------- inode / extent
def parse_inode(raw, inode_size=256):
    mode = struct.unpack("<H", raw[0:2])[0]
    if mode == 0:
        return None
    return {
        "mode": mode,
        "uid": struct.unpack("<H", raw[2:4])[0],
        "size": struct.unpack("<I", raw[4:8])[0] |
                ((struct.unpack("<I", raw[0x6C:0x70])[0] << 32)
                 if inode_size > 128 else 0),
        "atime": struct.unpack("<I", raw[8:12])[0],
        "ctime": struct.unpack("<I", raw[12:16])[0],
        "mtime": struct.unpack("<I", raw[16:20])[0],
        "dtime": struct.unpack("<I", raw[20:24])[0],   # 非 0 表示已删除
        "links": struct.unpack("<H", raw[0x1A:0x1C])[0],
        "blocks": struct.unpack("<I", raw[0x1C:0x20])[0],
        "flags": struct.unpack("<I", raw[0x20:0x24])[0],
        "i_block": raw[0x28:0x64],
        "raw": raw,
    }


def legacy_blocks(info):
    """非 extent inode 的块映射（仅取 i_block 的 15 个指针，够小文件用）"""
    if len(info["i_block"]) < 60:
        return []
    return list(struct.unpack("<15I", info["i_block"][:60]))


def resolve_extents(info, fs=None, block_reader=None, seen=None):
    """把小端 extent 树完整展开为 [(lblk, llen, pblk), ...]

    注意：ext4_extent_header 与 ext4_extent 全部为小端；
    ext4_extent 字段序为 u32 ee_block / u16 ee_len / u16 ee_start_hi / u32 ee_start_lo；
    ext4_extent_idx 字段序为 u32 ei_block / u32 ei_leaf_lo / u16 ei_leaf_hi / u16 unused。
    """
    if seen is None:
        seen = set()
    ib = info["i_block"]
    if len(ib) < 12:
        return []
    magic, entries, _mx, depth, _gen = struct.unpack("<HHHHI", ib[0:12])
    if magic != 0xF30A:
        return []
    out = []
    if depth == 0:
        for k in range(entries):
            e = ib[12 + k * 12: 24 + k * 12]
            if len(e) < 12:
                break
            lblk, llen, hi, lo = struct.unpack("<IHHI", e)
            if llen == 0:
                continue
            p = lo | (hi << 32)
            if (fs is None or fs.valid_block(p)) and (fs is None or fs.valid_block(p + llen - 1)):
                out.append((lblk, llen, p))
    else:
        reader = block_reader or (fs.read_block if fs else None)
        for k in range(entries):
            e = ib[12 + k * 12: 24 + k * 12]
            if len(e) < 12:
                break
            _blk, leaf_lo, leaf_hi, _u = struct.unpack("<IIHH", e)
            leaf = leaf_lo | (leaf_hi << 32)
            if not leaf or leaf in seen or (fs and not fs.valid_block(leaf)):
                continue
            seen.add(leaf)
            d = reader(leaf)
            if d is None:
                continue
            out.extend(resolve_extents({"i_block": d}, fs, reader, seen))
    return out


def extents_of(info, fs=None, block_reader=None):
    return resolve_extents(info, fs, block_reader)


# ---------------------------------------------------------------- 目录
def parse_dir_block(data):
    """解析 ext4 目录块 -> [(ino, name, ftype)]；不是合法目录块返回 None"""
    ents = []
    off = 0
    n = len(data)
    while off + 12 <= n:
        # metadata_csum 启用的目录块末尾有 12 字节 tail
        if n - off == 12:
            ino, rl, _nl, ft = struct.unpack("<IHBB", data[off:off + 8])
            if ino == 0 and rl == 12 and ft == 0xDE:
                return ents
        ino, rec_len, name_len, ftype = struct.unpack("<IHBB", data[off:off + 8])
        if rec_len < 8 or rec_len % 4 or off + rec_len > n:
            return None
        if ino != 0 and name_len:
            if name_len > MAX_NAME or off + 8 + name_len > n:
                return None
            name = data[off + 8: off + 8 + name_len]
            if any(c < 32 or c > 126 for c in name):
                return None
            ents.append((ino, name, ftype))
        off += rec_len
    return None


class JournalScanner:
    """解析 ext4 日志环并建立「fs 块 -> 历史版本」索引"""

    def __init__(self, fs, verbose=True):
        self.fs = fs
        self.verbose = verbose
        self.segs = fs.journal_map()
        self.versions = collections.defaultdict(list)   # fs_block -> [(seq, jpos)]
        self.tx_count = 0
        self.seq_range = None
        self.tag_mode = None
        self.sb = None

    def log(self, *a):
        if self.verbose:
            print(*a, flush=True)

    # ---------- 日志块号 -> fs 块号 ----------
    def jfs(self, jpos):
        for (j0, cnt, f0) in self.segs:
            if j0 <= jpos < j0 + cnt:
                return f0 + (jpos - j0)
        return None

    def jbytes(self, jpos, nblocks=1):
        """读取日志中连续 nblocks 块的数据"""
        buf = bytearray()
        for i in range(jpos, jpos + nblocks):
            b = self.jfs(i)
            if b is None:
                return None
            buf.extend(self.fs.read_block(b))
        return bytes(buf)

    @property
    def maxlen(self):
        return sum(c for _j, c, _f in self.segs)

    # ---------- 日志超级块 ----------
    def read_super(self):
        raw = self.jbytes(0, 1)[:1024]
        (magic, btype, hseq) = struct.unpack(">III", raw[0:12])
        (s_blocksize, s_maxlen, s_first, s_sequence, s_start,
         s_errno) = struct.unpack(">IIIIII", raw[12:36])
        fc, fi, fr = struct.unpack(">III", raw[36:48])
        self.sb = {
            "magic": magic, "blocktype": btype, "h_sequence": hseq,
            "block_size": s_blocksize, "maxlen": s_maxlen, "first": s_first,
            "sequence": s_sequence, "start": s_start, "errno": s_errno,
            "uuid": raw[48:64],
            "incompat": fi,
            "csum_v3": bool(fi & 0x10), "csum_v2": bool(fi & 0x08),
            "f64": bool(fi & 0x02), "revoke": bool(fi & 0x01),
        }
        return self.sb

    def _tag_size(self, mode):
        sb = self.sb
        if sb["csum_v3"]:
            return 16
        if sb["csum_v2"]:
            return 12
        return 8 if sb["f64"] else 4

    def _parse_tags(self, jpos, tsz, uuid_skip):
        raw = self.jbytes(jpos, 1)
        if raw is None:
            return [], False
        tags = []
        off = 12
        while off + tsz <= len(raw):
            chunk = raw[off:off + tsz]
            if tsz == 16:
                blk, flags, hi, _cs = struct.unpack(">IIII", chunk)
            elif tsz == 12:
                blk, _cs, flags, hi = struct.unpack(">IIHI", chunk)
            elif tsz == 8:
                blk, flags = struct.unpack(">II", chunk[:8])
                hi = 0
            else:
                blk, flags = struct.unpack(">II", chunk[:8])
                hi = 0
            # 尾部填充（全零 tag）视为结束
            if blk == 0 and flags == 0 and hi == 0:
                break
            tags.append((blk | (hi << 32), flags))
            off += tsz
            # 关键：csum_v3 的 tag 之后，当 SAME_UUID 未置位时要跳过 16 字节 UUID
            if uuid_skip and not (flags & F_SAME_UUID):
                off += 16
            if flags & F_LAST_TAG:
                break
        return tags, bool(tags and (tags[-1][1] & F_LAST_TAG))

    def _is(self, jpos, btype):
        raw = self.jbytes(jpos, 1)
        if raw is None or raw[0:4] != J_MAGIC:
            return None
        if struct.unpack(">I", raw[4:8])[0] != btype:
            return None
        return struct.unpack(">I", raw[8:12])[0]

    def detect_tag_mode(self):
        """自动判断 tag 解析是否需要跳过 UUID 字段

        判据：正确模式下单个描述符块会包含大量 tag（通常 ~253）；
        错误模式会把 16 字节 UUID 当成空 tag，从而每块只解析出 1 个 tag。
        """
        stats = {}
        for skip in (True, False):
            tsz = self._tag_size(skip)
            total = 0
            ndesc = 0
            commits = 0
            pos = 1
            end = min(self.maxlen, 200000)
            while pos < end and ndesc < 40:
                seq = self._is(pos, T_DESC)
                if seq is None:
                    pos += 1
                    continue
                tags, _last = self._parse_tags(pos, tsz, skip)
                ndesc += 1
                total += len(tags)
                nxt = pos + 1 + len(tags)
                if nxt < self.maxlen and self._is(nxt, T_COMMIT) is not None:
                    commits += 1
                pos += 1
            stats[skip] = {
                "avg_tags": total / ndesc if ndesc else 0,
                "desc": ndesc, "commits": commits, "tags": total,
            }
        best = max(stats, key=lambda k: (stats[k]["avg_tags"], stats[k]["tags"]))
        self.tag_mode = best
        if self.verbose:
            for k in (True, False):
                s = stats[k]
                self.log("  uuid_skip=%-5s 描述符=%d 平均tag=%.1f 匹配commit=%d"
                         % (k, s["desc"], s["avg_tags"], s["commits"]))
            self.log("  => 采用 uuid_skip=%s" % best)
        return best

    # ---------- 遍历事务 ----------
    def build(self):
        self.read_super()
        if self.verbose:
            sb = self.sb
            self.log("日志超级块: maxlen=%d first=%d sequence=%d start=%d "
                     "csum_v3=%s f64=%s" % (sb["maxlen"], sb["first"], sb["sequence"],
                                            sb["start"], sb["csum_v3"], sb["f64"]))
            if sb["start"] == 0:
                self.log("  注意: s_start=0 表示日志被 checkpoint 复位（正常卸载后常见），"
                         "现成工具会因此看不到旧事务；本库改为直接扫描物理日志数据。")
        skip = self.detect_tag_mode()
        tsz = self._tag_size(skip)
        mx = self.maxlen
        seqs = []
        pos = 1
        while pos < mx:
            seq = self._is(pos, T_DESC)
            if seq is None:
                pos += 1
                continue
            # 一个事务可能横跨多个描述符块，直到出现 LAST_TAG
            spans = []
            cur = pos
            complete = False
            while cur < mx:
                s2 = self._is(cur, T_DESC)
                if s2 is None:
                    break
                tags, last = self._parse_tags(cur, tsz, skip)
                if not tags:
                    break
                for i, (blk, flags) in enumerate(tags):
                    spans.append((blk, cur + 1 + i, flags))
                cur += 1 + len(tags)
                if last:
                    complete = True
                    break
            if spans:
                for (blk, jb, flags) in spans:
                    if jb < mx:
                        self.versions[blk].append((seq, jb))
                seqs.append(seq)
                self.tx_count += 1
            pos = cur if complete else pos + 1
        for k in list(self.versions):
            self.versions[k].sort()
        if seqs:
            self.seq_range = (min(seqs), max(seqs))
        self.log("  事务=%d seq 范围=%s 唯一 fs block=%d"
                 % (self.tx_count, self.seq_range, len(self.versions)))
        return self

    # ---------- 块与 inode 访问 ----------
    def block_data(self, blk):
        """取某 fs 块内容：优先日志中最新版本，否则读原始磁盘"""
        vs = self.versions.get(blk)
        if vs:
            seq, jpos = vs[-1]
            d = self.jbytes(jpos, 1)
            if d is not None:
                return d, "journal(seq=%d)" % seq
        if not self.fs.valid_block(blk):
            return b"\x00" * self.fs.block_size, "invalid"
        return self.fs.read_block(blk), "disk"

    def block_versions(self, blk):
        return self.versions.get(blk, [])

    def inode_versions(self, ino):
        """该 inode 在日志中的所有版本 -> [(seq, raw, info)]"""
        if ino < 1 or ino > self.fs.inodes_count:
            return []
        blk, off = self.fs.inode_location(ino)
        if blk is None:
            return []
        out = []
        for (seq, jpos) in self.versions.get(blk, []):
            d = self.jbytes(jpos, 1)
            if d is None or len(d) < off + self.fs.inode_size:
                continue
            raw = d[off:off + self.fs.inode_size]
            info = parse_inode(raw, self.fs.inode_size)
            if info is not None:
                out.append((seq, raw, info))
        return out

    def best_inode(self, ino):
        """选可用版本。优先级：
        1) 日志中 links>0 且有数据块的最新版本（删除前的最后状态）
        2) 磁盘上 links>0 且有数据块（该文件其实还存在）
        3) 日志中任意有数据块的版本
        4) 磁盘 inode
        返回 (seq_or_None, raw, info, source)
        """
        fs = self.fs

        def has_data(info):
            typ = info["mode"] & S_IFMT
            if info["size"] == 0:
                return True
            if typ == S_IFLNK and info["size"] < 60:
                return True
            if info["flags"] & 0x00080000:
                return bool(resolve_extents(info, fs, self.block_data))
            return bool(legacy_blocks(info)[0])

        jvers = self.inode_versions(ino)
        live = [v for v in jvers if v[2]["links"] > 0 and has_data(v[2])]
        if live:
            seq, raw, info = max(live, key=lambda v: v[0])
            return seq, raw, info, "journal-live"
        draw, dinfo = fs.read_inode(ino)
        if dinfo and dinfo["links"] > 0 and has_data(dinfo):
            return None, draw, dinfo, "disk"
        anyd = [v for v in jvers if has_data(v[2])]
        if anyd:
            seq, raw, info = max(anyd, key=lambda v: v[0])
            return seq, raw, info, "journal-any"
        if jvers:
            seq, raw, info = max(jvers, key=lambda v: v[0])
            return seq, raw, info, "journal-stale"
        if dinfo:
            return None, draw, dinfo, "disk"
        return None, None, None, "missing"

    def read_inode_data(self, info, limit=None):
        """按 extent/块映射读取 inode 数据（日志优先，缺失回退磁盘）"""
        bs = self.fs.block_size
        size = info["size"]
        if size == 0:
            return b""
        if (info["mode"] & S_IFMT) == S_IFLNK and size < 60:
            return info["i_block"][:size]
        if info["flags"] & 0x00080000:
            exts = resolve_extents(info, self.fs, self.block_data)
            if not exts:
                return None
            buf = bytearray()
            logical = 0
            for (lblk, llen, pblk) in sorted(exts):
                if lblk > logical:
                    buf.extend(b"\x00" * ((lblk - logical) * bs))
                    logical = lblk
                # 整段都不在日志里 -> 一次批量读磁盘（大文件快很多）
                if not any(b in self.versions
                           for b in range(pblk, min(pblk + llen, self.fs.blocks_count))):
                    buf.extend(self.fs.read_blocks(pblk, llen))
                else:
                    for i in range(llen):
                        d, _src = self.block_data(pblk + i)
                        buf.extend(d)
                logical += llen
                if limit and len(buf) >= limit:
                    break
            return bytes(buf[:size])
        # 传统块映射（仅直接块，够用即可）
        buf = bytearray()
        for b in legacy_blocks(info):
            if not b or not self.fs.valid_block(b):
                break
            d, _src = self.block_data(b)
            buf.extend(d)
            if len(buf) >= size:
                break
        return bytes(buf[:size])

    def dir_entries(self, info):
        """列目录条目（含已删除条目）"""
        data = self.read_inode_data(info)
        if data is None:
            return None
        bs = self.fs.block_size
        ents = []
        for off in range(0, len(data), bs):
            blk = data[off:off + bs]
            if len(blk) < bs:
                break
            e = parse_dir_block(blk)
            if e:
                ents.extend(e)
        return ents

    # ---------- 定位被删条目 ----------
    def dir_blocks_of(self, info):
        if info["flags"] & 0x00080000:
            return [p + i for (_l, ln, p) in sorted(resolve_extents(info, self.fs, self.block_data))
                    for i in range(ln)]
        return [b for b in legacy_blocks(info) if b and self.fs.valid_block(b)]

    def lookup_deleted(self, parent_ino, name):
        """在父目录的历史版本中查找名字 -> [(seq, ino, block)]"""
        if isinstance(name, str):
            name = name.encode()
        _seq, _raw, pinfo, src = self.best_inode(parent_ino)
        if pinfo is None:
            return []
        hits = []
        for blk in self.dir_blocks_of(pinfo):
            for (seq, jpos) in self.versions.get(blk, []):
                d = self.jbytes(jpos, 1)
                if d is None or name not in d:
                    continue
                ents = parse_dir_block(d)
                if not ents:
                    continue
                for (ino, nm, _ft) in ents:
                    if nm == name:
                        hits.append((seq, ino, blk))
        hits.sort()
        return hits

    def search_name(self, name):
        """全日志搜索某文件/目录名 -> [(fs_block, seq, ino)]"""
        if isinstance(name, str):
            name = name.encode()
        out = []
        for blk, vers in self.versions.items():
            for (seq, jpos) in vers:
                d = self.jbytes(jpos, 1)
                if d is None or name not in d:
                    continue
                ents = parse_dir_block(d)
                if not ents:
                    continue
                for (ino, nm, _ft) in ents:
                    if nm == name:
                        out.append((blk, seq, ino))
        out.sort()
        return out

    def seq_time_hint(self):
        """用日志中 inode 表块的时间戳估计日志覆盖的时间范围"""
        tables = set(self.fs.group_descs())
        lo = hi = None
        for blk, vers in self.versions.items():
            if blk not in tables:
                continue
            for (seq, jpos) in vers:
                d = self.jbytes(jpos, 1)
                if d is None:
                    continue
                for k in range(0, self.fs.block_size, self.fs.inode_size):
                    raw = d[k:k + self.fs.inode_size]
                    if len(raw) < 24 or struct.unpack("<H", raw[0:2])[0] == 0:
                        continue
                    for off in (16, 20):
                        t = struct.unpack("<I", raw[off:off + 4])[0]
                        if 1_000_000_000 < t < 2_200_000_000:
                            lo = t if lo is None or t < lo else lo
                            hi = t if hi is None or t > hi else hi
        return lo, hi
