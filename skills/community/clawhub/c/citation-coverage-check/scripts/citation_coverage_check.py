# -*- coding: utf-8 -*-
"""引用覆盖率检查器：扫描文章的引用覆盖率。零依赖。

对含数字/日期/百分比/强论断的句子，检查是否带来源标注
（据/来源/source/链接/《》/参考文献/https）。低于阈值 rc=1，逐句列缺口。
三律映射：LGD-II 有证 —— 论断要带出处。

用法：
  python citation_coverage_check.py --file report.md --threshold 0.6
  python citation_coverage_check.py --text "..." --json
"""
import argparse, json, pathlib, re, sys

HAS_NUM = re.compile(r"(\d+(\.\d+)?%?|\d{4}年|\d+月\d+日)")
HAS_SRC = re.compile(r"(据|来源|source|参考|文献|《[^》]{2,40}》|https?://)", re.I)


def main():
    ap = argparse.ArgumentParser(description="引用覆盖率检查器 · 论断要带出处")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="文件")
    src.add_argument("--text", help="文本（内联 / @文件 / 纯路径）")
    ap.add_argument("--threshold", type=float, default=0.6, help="覆盖率阈值（默认 0.6）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        if a.file:
            text = pathlib.Path(a.file).read_text(encoding="utf-8-sig")
        else:
            q = a.text[1:] if a.text.startswith("@") else a.text
            text = pathlib.Path(q).read_text(encoding="utf-8-sig") if pathlib.Path(q).is_file() else q
    except OSError as e:
        print(f"输入不可读：{e}", file=sys.stderr)
        sys.exit(2)

    claim_sents, uncovered = [], []
    for s in re.split(r"[。！？!?\n]", text):
        s = s.strip()
        if len(s) < 8 or not HAS_NUM.search(s):
            continue
        claim_sents.append(s)
        if not HAS_SRC.search(s):
            uncovered.append(s[:40] + ("…" if len(s) > 40 else ""))
    total = len(claim_sents)
    cov = (1 - len(uncovered) / total) if total else 1.0
    ok = cov >= a.threshold
    result = {"claims": total, "covered": total - len(uncovered),
              "coverage": round(cov, 2), "threshold": a.threshold, "pass": ok,
              "uncovered": uncovered,
              "note": "引用覆盖率过低，缺出处清单见上（rc=1）" if not ok
              else ("覆盖达标" if total else "无论断句，无需检查")}
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"论断句：{total}  有来源：{result['covered']}  覆盖率：{cov:.0%}（阈值 {a.threshold:.0%}）")
        if uncovered:
            print("缺出处清单：")
            for u in uncovered[:10]:
                print("  - " + u)
        print(("⛔ " if not ok else "✅ ") + result["note"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
