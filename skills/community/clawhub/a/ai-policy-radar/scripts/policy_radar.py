# -*- coding: utf-8 -*-
"""法规动态雷达：扫目录(.md)抽取监管关键词，按主题归类并留痕。零依赖。"""
import argparse, pathlib, re

THEMES = {
    "风险分级": re.compile(r"high-?risk|高风险|风险分级|风险分类", re.I),
    "透明度": re.compile(r"透明|披露|标识|transparen|disclos", re.I),
    "数据": re.compile(r"训练数据|数据(集|保护)|隐私|GDPR|personal data", re.I),
    "准入": re.compile(r"上市|备案|登记|准入|market access|conformity|ce 标志", re.I),
}
REG = re.compile(r"EU AI Act|NMPA|FDA|GDPR|人工智能法|AI Act|脆监会|网信办", re.I)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--since", default="")
    a = ap.parse_args()
    d = pathlib.Path(a.dir)
    hits = []
    for p in sorted(d.glob("*.md")):
        txt = p.read_text(encoding="utf-8-sig")
        if a.since and a.since not in txt:
            # 简单按 since 过滤（如 2026-09）
            if not re.search(a.since, txt):
                continue
        for line in txt.splitlines():
            if REG.search(line):
                themes = [name for name, pat in THEMES.items() if pat.search(line)]
                if themes:
                    hits.append((p.name, line.strip()[:60], themes))
    if not hits:
        print("本月无新增法规相关条目")
        return
    print(f"法规动态（{len(hits)} 条）：\n" + "=" * 40)
    for f, line, themes in hits:
        print(f"  [{','.join(themes)}] {f}: {line}")

if __name__ == "__main__":
    main()
