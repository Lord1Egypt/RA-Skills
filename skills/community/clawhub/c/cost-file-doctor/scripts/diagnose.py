#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
造价文件诊断器：判断一个工程计价文件能否本地解析。

用法: python3 diagnose.py "<文件路径>"

核心逻辑（顺序不能反）：
  1. 先看是不是容器（ZIP/OLE）—— 是容器就先解包，再检测内部文件
  2. 熵值只对「非容器的裸文件」有判定意义
     （ZIP 压缩后熵本来就 >7.9，但解包后是明文 —— 只看熵会误判）
  3. 中文串必须二次过滤：随机字节高字节落 0x4e-0x9f 概率 32%，
     连续 6 组即约 0.1%，2MB 仍会产生上千条假阳性
"""
import sys, os, math, collections, zlib, re, zipfile, tempfile

SIGS = {
    b'PK\x03\x04': 'ZIP', b'\xd0\xcf\x11\xe0': 'OLE',
    b'SQLite format 3': 'SQLite', b'7z\xbc\xaf': '7z',
    b'Rar!': 'RAR', b'\x1f\x8b': 'GZIP', b'\xfd7zXZ': 'XZ',
    b'\x28\xb5\x2f\xfd': 'ZSTD', b'\x04\x22\x4d\x18': 'LZ4',
    b'BZh': 'BZIP2',
}
CJK = re.compile(r'[\u4e00-\u9fa5]')
CN_BYTES = re.compile(rb'(?:[\x00-\xff][\x4e-\x9f]){8,}')
KEYWORDS = ['工程', '清单', '合价', '单价', '项目', '定额', '措施',
            '暂列', '材料', '单位', '合计', '取费', '税金', '规费']


def entropy(d):
    c = collections.Counter(d)
    return -sum(v / len(d) * math.log2(v / len(d)) for v in c.values())


def cn_count(d):
    n = 0
    for m in CN_BYTES.finditer(d):
        try:
            s = m.group().decode('utf-16-le')
        except Exception:
            continue
        if len(s) >= 4 and sum(1 for c in s if CJK.match(c)) / len(s) >= 0.9:
            n += 1
    return n


def kw_hits(d):
    return {k for k in KEYWORDS if d.count(k.encode('utf-16-le'))}


def probe(d, label, indent=''):
    e = entropy(d); cn = cn_count(d); kw = kw_hits(d)
    print(f"{indent}[{label}] {len(d):,} B")
    print(f"{indent}  熵    : {e:.4f}")
    print(f"{indent}  中文串: {cn} 条")
    print(f"{indent}  关键词: {len(kw)} 个 {sorted(kw)[:10] if kw else ''}")
    return e, cn, kw


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    p = sys.argv[1]
    if not os.path.exists(p):
        print("文件不存在:", p); sys.exit(1)
    d = open(p, 'rb').read()
    print(f"文件: {os.path.basename(p)}   {len(d):,} 字节 ({len(d)/1024/1024:.2f} MB)")

    print("\n[1] 容器检测")
    is_zip = d[:4] == b'PK\x03\x04'
    hits = [(n, d[:262144].find(s)) for s, n in SIGS.items() if d[:262144].find(s) >= 0]
    for n, i in hits:
        print(f"    {n:<14} 命中 @{i}")
    if not hits:
        print("    未命中任何已知容器签名")

    if is_zip:
        print("\n[2] ZIP 容器 → 解包后检测内部（熵对压缩包无判定意义）")
        probe(d, "外层(压缩)", "    ")
        with tempfile.TemporaryDirectory() as td:
            try:
                z = zipfile.ZipFile(p); z.extractall(td); names = z.namelist()
            except Exception as ex:
                print("    解包失败:", ex); return
            print(f"    解出 {len(names)} 个内部文件")
            files = []
            for root, _, fs in os.walk(td):
                for f in fs:
                    fp = os.path.join(root, f)
                    try:
                        files.append((os.path.getsize(fp), fp))
                    except Exception:
                        pass
            files.sort(reverse=True)
            inner_cn = 0; inner_kw = set()
            for sz, fp in files[:5]:
                try:
                    dd = open(fp, 'rb').read()
                except Exception:
                    continue
                _, c, k = probe(dd, os.path.basename(fp)[:22], "      ")
                inner_cn += c; inner_kw |= k
            print(f"\n    内部合计: 中文串 {inner_cn} 条，关键词 {len(inner_kw)} 个")
        print("\n" + "=" * 62)
        if inner_cn > 50 or len(inner_kw) >= 3:
            print("判定: OK 可本地解析（容器 + 内部明文）")
            print("  下一步: 解包 → 找字段名区([长度][UTF-16LE]) → 定位数据区")
            print("  宏业 SGCFX 可直接用 sgcfx-hongye-parse 技能")
        else:
            print("判定: NO 内部也是密文")
        return

    print("\n[2] 非容器 → 直接检测")
    e, cn, kw = probe(d, "整体", "    ")
    seg = len(d) // 8
    vals = [entropy(d[i * seg:(i + 1) * seg]) for i in range(8) if seg]
    if vals:
        print(f"    分块熵: {min(vals):.4f} ~ {max(vals):.4f} "
              f"(极差 {max(vals)-min(vals):.4f})")

    print("\n[3] 压缩流实测（验证是否假阳性）")
    found = 0
    for off in range(0, min(len(d) - 8, 300000)):
        if d[off] == 0x78:
            try:
                r = zlib.decompressobj().decompress(d[off:off + 400000])
                if len(r) > 500:
                    print(f"    ZLIB @{off}: 成功 {len(r):,} 字节 头: {r[:50]!r}")
                    found += 1
                    if found >= 3: break
            except Exception:
                pass
    if not found:
        print("    无有效 zlib 流")

    print("\n" + "=" * 62)
    print("判定:")
    # 决定性证据是「造价专业关键词」：随机数据不可能同时命中这些词。
    # 中文串条数在高熵文件里仍有随机残留（实测 2MB 加密文件约 130 条），不能单独采信。
    if e > 7.9 and not kw:
        print("  NO 整体加密，无法本地解析")
        print(f"     证据: 熵 {e:.4f} > 7.9，专业关键词命中 0 个"
              f"（中文串 {cn} 条属随机残留，密度 {cn/(len(d)/1048576):.0f} 条/MB）")
        print("  建议: ① 先在该文件所在目录找已导出的 Excel/PDF  <- 最省事")
        print("        ② 装原软件导出  ③ 找发件人要导出件")
        print("        ④ 不要再尝试破解，性价比极低")
    elif e > 7.0 and not kw:
        print("  WARN 可能是强压缩，先找到正确解压算法再判断")
    else:
        print(f"  OK 含可读文本，可尝试本地解析（关键词 {len(kw)} 个）")


if __name__ == '__main__':
    main()
