# -*- coding: utf-8 -*-
"""评测基准生成器：读 spec(能力+边界用例)，产出 JSONL 评测集。零依赖。"""
import argparse, json, pathlib, re

def parse_spec(txt):
    cases = []
    # 支持 Markdown 列表： - [能力] 输入 => 期望 (judge)
    for m in re.finditer(r"-\s*\[([^\]]+)\]\s*(.+?)\s*=>\s*(.+?)(?:\(([^)]*)\))?$", txt, re.M):
        cap, inp, exp, judge = m.group(1), m.group(2), m.group(3), m.group(4) or "包含"
        cases.append({"capability": cap.strip(), "input": inp.strip(),
                      "expect": exp.strip(), "judge": judge.strip()})
    return cases

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec_p = pathlib.Path(a.spec)
    if not spec_p.exists():
        ap.error(f"spec 文件不存在: {a.spec}")
    txt = spec_p.read_text(encoding="utf-8-sig")
    cases = parse_spec(txt)
    if not cases:
        print("spec 未解析出用例（格式：- [能力] 输入 => 期望 (judge)）")
        return
    out_p = pathlib.Path(a.out)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in cases), encoding="utf-8")
    print(f"已生成 {len(cases)} 条评测样本 → {a.out}")

if __name__ == "__main__":
    main()
