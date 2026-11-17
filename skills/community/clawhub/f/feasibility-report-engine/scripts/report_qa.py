#!/usr/bin/env python3
"""长文档 QA 工具 —— 让「改动快、验收稳」有据可依。

用法:
    python3 report_qa.py cache <docx> [--out DIR]      # 建纯文本缓存（比 python-docx 提取快 ~14x）
    python3 report_qa.py check <docx> [--baseline J]    # 跑固化验收断言（JSON 基线）
    python3 report_qa.py grep  <docx> <regex>           # 在缓存上查（缺缓存自动建）
    python3 report_qa.py stats <docx>                   # 规模体检：页量/段落/字符/内嵌图片

设计要点:
    - 段落边界靠 </w:p> 切分保留；表格文字一并取出（漏扫表格 = 漏扫一半内容）
    - 验收断言写进 baseline JSON：禁用词 / 必须出现 / 必须消失，改完一条命令自证
    - 空断言会显式告警，避免「0/0 全绿」的假阳性
基线 JSON 示例:
    {"禁用词（必须 0 命中）": ["某某旧口径", "敏感企业名"],
     "必须出现（≥1 命中）": ["总投资约100亿元"]}

仅用标准库，无第三方依赖。
"""
import json
import os
import re
import sys
import tempfile
import time
import zipfile

CACHE_DIR = os.path.join(tempfile.gettempdir(), "report_cache")


def _strip(xml_frag: str) -> str:
    txt = re.sub(r"<w:tab[^>]*/>", "\t", xml_frag)
    txt = re.sub(r"<w:br[^>]*/>", "\n", txt)
    txt = re.sub(r"<[^>]+>", "", txt)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'")):
        txt = txt.replace(a, b)
    return txt


def extract_paragraphs(path: str):
    """zip 直读 → 段落文本列表（含表格单元格文字，按 xml 顺序）。"""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    return [_strip(p) for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)]


def cache_path(docx: str, out: str = CACHE_DIR) -> str:
    os.makedirs(out, exist_ok=True)
    return os.path.join(out, os.path.basename(docx).rsplit(".", 1)[0] + ".txt")


def build_cache(docx: str, out: str = CACHE_DIR) -> str:
    t0 = time.time()
    paras = extract_paragraphs(docx)
    cp = cache_path(docx, out)
    with open(cp, "w", encoding="utf-8") as f:
        f.write("\n".join(paras))
    print(f"✅ 缓存已建：{cp}\n   段落 {len(paras)} 行 / {sum(len(p) for p in paras)} 字符 / 耗时 {time.time()-t0:.2f}s")
    return cp


def load_text(docx: str) -> str:
    cp = cache_path(docx)
    if not os.path.exists(cp) or os.path.getmtime(cp) < os.path.getmtime(docx):
        with open(cp, "w", encoding="utf-8") as f:
            f.write("\n".join(extract_paragraphs(docx)))
    return open(cp, encoding="utf-8").read()


def check(docx: str, baseline_file: str = None):
    txt = load_text(docx)
    if baseline_file:
        if not os.path.exists(baseline_file):
            print(f"❌ 基线文件不存在：{baseline_file}")
            return False
        bl = json.load(open(baseline_file, encoding="utf-8"))
        print(f"基线：{baseline_file}")
    else:
        bl = {"禁用词（必须 0 命中）": [], "必须出现（≥1 命中）": [], "必须消失（0 命中）": []}
    results = []
    for cat, words in bl.items():
        if not isinstance(words, list):
            continue
        for word in words:
            n = len(re.findall(re.escape(word), txt))
            if "禁用" in cat or "必须消失" in cat:
                results.append((f"{cat}｜{word}", n == 0, f"{n} 处"))
            else:
                results.append((f"{cat}｜{word}", n >= 1, f"{n} 处"))
    print(f"\n=== 验收：{os.path.basename(docx)} ===")
    if not results:
        print("⚠️ 基线里没有任何断言被执行 —— 检查 JSON 键名（值须为 list）")
        return False
    for name, passed, detail in results:
        print(f"  {'✅' if passed else '❌'} {name}  ({detail})")
    ok = sum(1 for _, p, _ in results if p)
    print(f"\n结果：{ok}/{len(results)} 通过" + ("  🎉 全绿，可交付" if ok == len(results) else "  ⚠️ 有未通过项"))
    return ok == len(results)


def grep(docx: str, pattern: str, limit: int = 40):
    txt = load_text(docx)
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(txt.split("\n")) if re.search(pattern, ln)]
    print(f"命中 {len(hits)} 行（显示前 {limit}）：")
    for i, ln in hits[:limit]:
        print(f"  L{i}: {ln[:160]}")
    return hits


def stats(docx: str):
    paras = extract_paragraphs(docx)
    nonempty = [p for p in paras if p.strip()]
    print(f"文件：{docx}")
    print(f"大小：{os.path.getsize(docx)/1e6:.2f} MB")
    print(f"段落：{len(paras)}（非空 {len(nonempty)}）")
    print(f"字符：{sum(len(p) for p in paras)}")
    with zipfile.ZipFile(docx) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
    print(f"内嵌图片：{len(media)} 个")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(0)
    cmd, docx = sys.argv[1], sys.argv[2]
    if cmd == "cache":
        build_cache(docx, sys.argv[3] if len(sys.argv) > 3 else CACHE_DIR)
    elif cmd == "check":
        sys.exit(0 if check(docx, sys.argv[3] if len(sys.argv) > 3 else None) else 1)
    elif cmd == "grep":
        grep(docx, sys.argv[3])
    elif cmd == "stats":
        stats(docx)
    else:
        print(__doc__)
