#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ext4recover.py —— 通用 ext4 删除恢复命令行工具（只读）

子命令
  info                            文件系统与日志概况
  scan                            扫描日志环，报告可恢复范围与覆盖时间
  find <name>                     全日志搜索文件名 -> [(fs_block, seq, inode)]
  lookup <parent_ino> <name>      在指定父目录的历史版本中查找被删条目
  stat <ino>                      列出该 inode 的所有历史版本（含删除版本）
  ls <ino|path>                   列目录条目（含被删条目）
  recover <ino|path> --out DIR    递归恢复目录树/单个文件
  verify <ino>                    映射自检：对比日志最新版本与磁盘内容

示例
  python3 ext4recover.py /dev/sdb1 info
  python3 ext4recover.py /dev/sdb1 scan
  python3 ext4recover.py /dev/sdb1 find some_deleted_dir
  python3 ext4recover.py /dev/sdb1 ls 2
  python3 ext4recover.py /dev/sdb1 recover 131075 --out /mnt/backup/

安全约束：本工具只读打开设备，绝不挂载、绝不写入目标设备。
输出目录必须位于**另一个**文件系统上，否则会覆盖待恢复数据。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ext4journal as E   # noqa: E402

USAGE = __doc__


def die(msg):
    print("错误: %s" % msg, file=sys.stderr)
    sys.exit(1)


def human(n):
    for u in ("B", "KiB", "MiB", "GiB", "TiB"):
        if n < 1024 or u == "TiB":
            return "%.1f %s" % (n, u) if u != "B" else "%d B" % n
        n /= 1024.0


def typestr(mode):
    return {E.S_IFDIR: "dir", E.S_IFREG: "file", E.S_IFLNK: "link"}.get(
        mode & E.S_IFMT, "other")


# ---------------------------------------------------------------- 路径解析
def split_path(p):
    return [c for c in p.strip("/").split("/") if c]


def resolve_path(js, path):
    """解析路径；中间分量必须仍存在，最后一段允许已被删除"""
    cur = 2
    parts = split_path(path)
    if not parts:
        return 2
    for i, comp in enumerate(parts):
        last = (i == len(parts) - 1)
        _s, _r, info, _src = js.best_inode(cur)
        if info is None:
            return None
        nxt = None
        ents = js.dir_entries(info)
        if ents:
            for (ino, nm, _ft) in ents:
                if nm == comp.encode():
                    nxt = ino
                    break
        if nxt is None and last:
            hits = js.lookup_deleted(cur, comp)
            if hits:
                nxt = hits[-1][1]
        if nxt is None:
            return None
        cur = nxt
    return cur


# ---------------------------------------------------------------- 遍历
class Walker:
    def __init__(self, js, limit_bytes=None):
        self.js = js
        self.limit_bytes = limit_bytes
        self.stats = {"files": 0, "bytes": 0, "missing_inode": 0,
                      "no_data": 0, "unreadable_dir": 0, "skipped_too_large": 0,
                      "skipped_bytes": 0}

    def walk(self, ino, path, outdir=None, depth=0, maxdepth=24, quiet=False):
        if depth > maxdepth:
            return 0, 0
        js = self.js
        seq, raw, info, src = js.best_inode(ino)
        if info is None:
            self.stats["missing_inode"] += 1
            if not quiet:
                print("  %s%s  !! 无 inode 版本 (ino=%d)" % ("  " * depth, path, ino))
            return 0, 0
        typ = info["mode"] & E.S_IFMT
        if typ == E.S_IFDIR:
            ents = js.dir_entries(info)
            if ents is None:
                self.stats["unreadable_dir"] += 1
                if not quiet:
                    print("  %s%s/  !! 目录数据不可读 (ino=%d)" % ("  " * depth, path, ino))
                return 0, 0
            if outdir:
                os.makedirs(outdir, exist_ok=True)
            nf = nb = 0
            for (cino, name, ft) in sorted(ents, key=lambda x: x[1]):
                if name in (b".", b".."):
                    continue
                nm = name.decode("utf-8", "replace")
                sub, sb = self.walk(cino, nm, os.path.join(outdir, nm) if outdir else None,
                                    depth + 1, maxdepth, quiet)
                nf += sub
                nb += sb
                if not quiet and depth < 2:
                    print("  %s%-32s ino=%-10d %s" % ("  " * depth, nm, cino,
                                                      "dir" if ft == 2 else human(sb)))
            return nf, nb
        if typ in (E.S_IFREG, E.S_IFLNK):
            if self.limit_bytes and info["size"] > self.limit_bytes:
                self.stats["skipped_too_large"] += 1
                self.stats["skipped_bytes"] += info["size"]
                if not quiet:
                    print("  %s%s  跳过：size=%d 超过 --limit-mb" % ("  " * depth, path, info["size"]))
                return 0, info["size"]
            data = js.read_inode_data(info)
            if data is None:
                self.stats["no_data"] += 1
                if not quiet:
                    print("  %s%s  !! 无数据块 (size=%d links=%d dtime=%s)"
                          % ("  " * depth, path, info["size"], info["links"],
                             E.fmt_ts(info["dtime"]) if info["dtime"] else "-"))
                return 0, info["size"]
            self.stats["files"] += 1
            self.stats["bytes"] += len(data)
            if outdir:
                d = os.path.dirname(outdir)
                if d:
                    os.makedirs(d, exist_ok=True)
                with open(outdir, "wb") as fh:
                    fh.write(data)
            return 1, len(data)
        return 0, 0


# ---------------------------------------------------------------- 子命令
def cmd_info(dev):
    fs = E.Ext4FS(dev)
    print("=== 文件系统 ===")
    for k, v in fs.info_lines():
        print("  %-16s = %s" % (k, v))
    try:
        segs = fs.journal_map()
        total = sum(c for _j, c, _f in segs)
        size = total * fs.block_size
        print("\n=== 日志 ===")
        print("  %-16s = %d 块 = %s" % ("日志总大小", total, human(size)))
        print("  %-16s = 默认 128MiB 的 %.1f 倍" % ("相对常见默认值", size / (128 * 2**20)))
        print("  %-16s = %s" % ("日志分段(逻辑块,块数,物理块)", segs[:6]))
        print("  说明：日志越大，删除前的 inode 元数据留存概率越高。")
    except Exception as exc:      # noqa: BLE001
        print("\n日志定位失败: %s" % exc)


def cmd_scan(dev):
    fs = E.Ext4FS(dev)
    js = E.JournalScanner(fs).build()
    lo, hi = js.seq_time_hint()
    print("\n=== 覆盖范围估计 ===")
    if lo:
        print("  日志中 inode 时间戳范围 = %s .. %s" % (E.fmt_ts(lo), E.fmt_ts(hi)))
    print("  可将各目录的删除时间(dtime)与上述范围比对，判断是否仍在覆盖窗口内")
    return js


def cmd_find(dev, name):
    fs = E.Ext4FS(dev)
    js = E.JournalScanner(fs).build()
    hits = js.search_name(name)
    print("\n=== 名字 '%s' 在日志中的记录 (共 %d 条) ===" % (name, len(hits)))
    seen = set()
    for (blk, seq, ino) in hits:
        key = (blk, ino)
        if key in seen:
            continue
        seen.add(key)
        d, src = js.block_data(blk)
        ents = E.parse_dir_block(d) or []
        others = [e[1].decode("utf-8", "replace") for e in ents
                  if e[1] not in (b".", b"..") and e[1] != name.encode()][:8]
        print("  fs_block=%-10d seq=%-6d inode=%-10d 同目录其它项: %s"
              % (blk, seq, ino, ", ".join(others)))


def cmd_lookup(dev, parent_ino, name):
    fs = E.Ext4FS(dev)
    js = E.JournalScanner(fs).build()
    hits = js.lookup_deleted(int(parent_ino), name)
    print("\n=== 在父目录 %s 中查找 '%s' ===" % (parent_ino, name))
    if not hits:
        print("  未找到（可能该目录块的历史版本不在日志环内）")
    for (seq, ino, blk) in hits:
        print("  seq=%-6d inode=%-10d (目录数据块 %d)" % (seq, ino, blk))
    if hits:
        print("  => 最新记录 inode=%d（可用它继续 stat / ls / recover）" % hits[-1][1])


def cmd_stat(dev, ino):
    fs = E.Ext4FS(dev)
    js = E.JournalScanner(fs).build()
    ino = int(ino)
    _blk, off = fs.inode_location(ino)
    print("\n=== inode %d (表块 %s 偏移 %s) 的历史版本 ===" % (ino, _blk, off))
    vers = js.inode_versions(ino)
    print("  日志版本数 = %d" % len(vers))
    for (seq, _raw, info) in sorted(vers):
        exts = E.resolve_extents(info, fs, js.block_data)
        print("  seq=%-6d %-5s mode=%06o size=%-12d links=%-2d dtime=%-11s extents=%d"
              % (seq, typestr(info["mode"]), info["mode"], info["size"], info["links"],
                 E.fmt_ts(info["dtime"]) if info["dtime"] else "-", len(exts)))
    _s, _r, dinfo, _src = js.best_inode(ino)
    if dinfo:
        print("  磁盘现状: %-5s mode=%06o size=%-12d links=%-2d dtime=%s"
              % (typestr(dinfo["mode"]), dinfo["mode"], dinfo["size"], dinfo["links"],
                 E.fmt_ts(dinfo["dtime"]) if dinfo["dtime"] else "-"))
    print("\n  links=0 且 dtime 非 0 => 已被删除；size 被清零说明 extent 已被回收，"
          "需要更早的历史版本")


def cmd_ls(dev, target):
    fs = E.Ext4FS(dev)
    js = E.JournalScanner(fs).build()
    if target.isdigit():
        ino = int(target)
    else:
        ino = resolve_path(js, target)
        if ino is None:
            die("路径解析失败: %s" % target)
    seq, _raw, info, src = js.best_inode(ino)
    print("\n=== inode %d (%s, 来源 %s) ===" % (ino, typestr(info["mode"]), src))
    if (info["mode"] & E.S_IFMT) != E.S_IFDIR:
        print("  不是目录")
        return
    ents = js.dir_entries(info)
    if ents is None:
        print("  目录数据不可读")
        return
    for (cino, name, ft) in sorted(ents, key=lambda x: x[1]):
        if name in (b".", b".."):
            continue
        _s, _r, cinfo, csrc = js.best_inode(cino)
        if cinfo:
            print("  %-40s ino=%-10d %-5s size=%-12d links=%-2d dtime=%s"
                  % (name.decode("utf-8", "replace"), cino, typestr(cinfo["mode"]),
                     cinfo["size"], cinfo["links"],
                     E.fmt_ts(cinfo["dtime"]) if cinfo["dtime"] else "-"))
        else:
            print("  %-40s ino=%-10d (无 inode)" % (name.decode("utf-8", "replace"), cino))


def cmd_recover(dev, target, outdir, limit_mb=None, quiet=False):
    fs = E.Ext4FS(dev)
    js = E.JournalScanner(fs).build()
    if target.isdigit():
        ino = int(target)
    else:
        ino = resolve_path(js, target)
        if ino is None:
            die("路径解析失败: %s" % target)
    if not outdir:
        die("必须用 --out 指定输出目录（且必须在另一个文件系统上）")
    print("\n=== 恢复 inode %d -> %s ===" % (ino, outdir))
    w = Walker(js, limit_mb * 2**20 if limit_mb else None)
    nf, nb = w.walk(ino, str(ino), outdir, quiet=quiet)
    print("\n=== 统计 ===")
    print("  文件数 = %d" % nf)
    print("  总字节 = %d (%s)" % (nb, human(nb)))
    for k, v in sorted(w.stats.items()):
        if k in ("files", "bytes"):
            continue
        if k == "skipped_bytes":
            print("  %-20s = %s" % (k, human(v)))
        else:
            print("  %-20s = %d" % (k, v))


def cmd_verify(dev, ino):
    """映射自检：日志中最新版本若与磁盘块完全一致，说明块->数据映射正确"""
    fs = E.Ext4FS(dev)
    js = E.JournalScanner(fs).build()
    ino = int(ino)
    blk, off = fs.inode_location(ino)
    print("\n=== 自检 inode %d (表块 %d 偏移 %d) ===" % (ino, blk, off))
    vers = js.block_versions(blk)
    print("  该 inode 表块的历史版本数 = %d" % len(vers))
    if not vers:
        print("  该表块不在日志中，无法自检（换一个近期被访问过的 inode）")
        return
    disk = fs.read_block(blk)
    for (seq, jpos) in vers[-3:]:
        d = js.jbytes(jpos, 1)
        same = (d == disk)
        print("  seq=%-6d journal块=%-8d 与磁盘内容%s"
              % (seq, jpos, "完全一致 (映射正确)" if same else "不同 (历史版本，预期如此)"))
    print("\n  判读方法: 取一个「确定近期没被改动」的文件 inode，其日志最新版本应与磁盘一致；")
    print("  若一致，说明 tag->数据块 的映射与解析全部正确，可放心恢复。")


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)
    dev = sys.argv[1]
    cmd = sys.argv[2]
    args = sys.argv[3:]
    quiet = "--quiet" in args
    if cmd == "info":
        cmd_info(dev)
    elif cmd == "scan":
        cmd_scan(dev)
    elif cmd == "find":
        cmd_find(dev, args[0])
    elif cmd == "lookup":
        cmd_lookup(dev, args[0], args[1])
    elif cmd == "stat":
        cmd_stat(dev, args[0])
    elif cmd == "ls":
        cmd_ls(dev, args[0])
    elif cmd == "verify":
        cmd_verify(dev, args[0])
    elif cmd == "recover":
        out = None
        lim = None
        if "--out" in args:
            out = args[args.index("--out") + 1]
        if "--limit-mb" in args:
            lim = int(args[args.index("--limit-mb") + 1])
        cmd_recover(dev, args[0], out, lim, quiet)
    else:
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
