#!/bin/bash
# ext4 删除恢复 —— 第一阶段只读体检
#
# 用法: bash diag.sh /dev/sdb1 [输出目录]
#
# 严格只读：不写入目标设备、不挂载该分区。若发现分区已挂载会立即中止。
# 需要能读设备节点（root，或先 `sudo chown $USER:disk <dev>`）。

DEV="${1:?用法: bash diag.sh /dev/sdbX [输出目录]}"
OUT="${2:-$PWD/ext4-recovery-diag}"
LOG="$OUT/diag.log"

mkdir -p "$OUT"
exec > >(tee "$LOG") 2>&1

echo "=== ext4 恢复体检: $(date '+%F %T') ==="
echo "设备: $DEV   输出: $OUT"

if [ ! -r "$DEV" ]; then
  echo "!! 无读取 $DEV 的权限。请用 root 运行，或执行:"
  echo "   sudo chown \$USER:disk $DEV && sudo chmod 660 $DEV"
  exit 1
fi

echo
echo "=== [1] 安全闸门：挂载状态 ==="
if findmnt -no TARGET "$DEV" 2>/dev/null; then
  echo "!! 致命：$DEV 已挂载。请先 umount，恢复期间绝不要挂载。"
  exit 1
fi
echo "OK: $DEV 未挂载（这是恢复能成功的前提）"
mount | grep -i "$(basename "$DEV")" && echo "!! 注意上面出现了相关挂载点"

echo
echo "=== [2] 设备概况 ==="
lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT "$DEV" 2>/dev/null || lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT
if [ -w "$DEV" ]; then
  echo "提示：当前用户对该设备有写权限。恢复期间请勿执行任何写操作。"
fi

echo
echo "=== [3] 超级块摘要（关键项）==="
dumpe2fs -h "$DEV" 2>/dev/null | egrep -i \
  'Filesystem volume|Filesystem UUID|Filesystem features|Filesystem state|Last mount|Last write|Last checked|Mount count|Inode count|Block count|Free blocks|Free inodes|Block size|Inode size|Journal inode|Total journal size|Total journal blocks|Journal sequence|Journal start|Checksum type|Default mount|Errors behavior'

echo
echo "=== [4] 日志大小判读 ==="
JSIZE=$(dumpe2fs -h "$DEV" 2>/dev/null | grep -i 'Total journal size' | awk '{print $NF}')
echo "日志总大小 = ${JSIZE:-未知}"
echo "说明：日志越大，被删 inode 的元数据留存概率越高；128MiB 为常见默认值，"
echo "      1GiB 级别意味着覆盖窗口长，若删除发生在窗口内则恢复希望很大。"

echo
echo "=== [5] 只读一致性检查 e2fsck -fn（不会写入）==="
e2fsck -fn "$DEV" 2>&1 | tail -30

echo
echo "=== [6] 根目录与关键目录（debugfs 直接读，不挂载）==="
debugfs -R 'ls -l /' "$DEV" 2>&1 | head -40

echo
echo "=== [7] 日志超级块（s_start=0 表示已被 checkpoint 复位）==="
debugfs -R 'logdump -a' "$DEV" 2>&1 | head -8

echo
echo "=== [8] 日志区原始扫描（判断旧事务是否残留）==="
python3 - "$DEV" <<'PY'
import struct, sys, mmap, os
dev = sys.argv[1]
fd = os.open(dev, os.O_RDONLY)
mm = mmap.mmap(fd, 0, prot=mmap.PROT_READ)
sb = mm[1024:2048]
log_bs = struct.unpack("<I", sb[0x18:0x1C])[0]
bs = 1024 << log_bs
# 读 inode 8（日志 inode）的 extent，定位日志数据块
ino_off = 1024
def u32(o):
    return struct.unpack("<I", sb[o:o+4])[0]
# 通过 debugfs 更简单，这里用超级块给出的 journal inode 数 = 8，故需 GDT；
# 简化处理：直接按 inode 表推导（组0 的 inode 表位置）
groups = (u32(0x00) + u32(0x28) - 1) // u32(0x28)
dsz = 64 if (u32(0x60) & 0x80) else 32
gdt_off = 2 * bs if bs == 1024 else bs
tbl = struct.unpack("<I", mm[gdt_off + 8: gdt_off + 12])[0]
inode_size = u32(0x58) or 128
raw = mm[tbl * bs + (8 - 1) * inode_size: tbl * bs + 8 * inode_size]
magic, entries, mx, depth, gen = struct.unpack("<HHHHI", raw[0x28:0x34])
if magic != 0xF30A:
    print("  日志 inode 非 extent 格式，跳过自动扫描")
    sys.exit(0)
segs = []
j = 0
for k in range(entries):
    e = raw[0x28 + 12 + k * 12: 0x28 + 24 + k * 12]
    lblk, llen, hi, lo = struct.unpack("<IHHI", e)
    segs.append((lo | (hi << 32), llen))
total = sum(l for _p, l in segs)
print("  日志数据块 = %d 块 (%d MiB)，起始 fs 块 = %s" % (total, total * bs // 2**20, segs[0][0]))
blob = bytearray()
for (p, l) in segs:
    blob.extend(mm[p * bs:(p + l) * bs])
blob = bytes(blob)
print("  jbd2 事务魔数出现次数 = %d" % blob.count(b"\xc0\x3b\x39\x98"))
print("  日志区全零字节占比     = %.2f%%" % (blob.count(b"\x00") * 100.0 / max(len(blob), 1)))
print("  判读：魔数数量多且全零占比低 => 物理日志里仍保留大量历史事务，可继续恢复；")
print("        魔数几乎为 0 或全零占比极高 => 日志已被覆盖/清零，恢复希望渺茫。")
PY

echo
echo "=== [9] 若需要，进一步用 ext4recover.py ==="
echo "  python3 $(dirname "$0")/ext4recover.py $DEV info"
echo "  python3 $(dirname "$0")/ext4recover.py $DEV scan"
echo "  python3 $(dirname "$0")/ext4recover.py $DEV find <被删文件名>"
echo
echo "=== 完成: $(date '+%F %T') ==="
echo "日志: $LOG"
