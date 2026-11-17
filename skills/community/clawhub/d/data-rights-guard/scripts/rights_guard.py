# -*- coding: utf-8 -*-
"""数据版权护栏：读数据集清单(manifest.json)，按许可证/商用/署名/来源给可训练评级。零依赖。"""
import argparse, json, pathlib

def rate(entry):
    lic = (entry.get("license") or "").strip().lower()
    commercial = entry.get("commercial", True)
    attr = entry.get("attribution", False)
    source = (entry.get("source") or "").strip()
    problems = []
    if not lic:
        problems.append("无许可证(高危)")
    if commercial is False or "non-commercial" in lic or "nc" == lic:
        problems.append("非商用锁(不可商用)")
    if attr is True and not entry.get("attributed", False):
        problems.append("需署名但未标")
    if not source:
        problems.append("来源不可溯(隔离待核)")
    if any("高危" in p or "非商用" in p for p in problems):
        return "排除", problems
    if problems:
        return "需处理", problems
    return "可训练", problems

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    items = json.loads(pathlib.Path(a.manifest).read_text(encoding="utf-8-sig"))
    if isinstance(items, dict):
        items = items.get("items", [])
    out = []
    excl = 0
    for e in items:
        st, probs = rate(e)
        if st == "排除":
            excl += 1
        out.append({"id": e.get("id", "?"), "status": st, "problems": probs})
    if a.json:
        print(json.dumps({"items": out, "excluded": excl, "advice": "排除项不出训练集；需处理项补全后再进"}, ensure_ascii=False, indent=2))
    else:
        for o in out:
            icon = "✅" if o["status"] == "可训练" else "⚠️" if o["status"] == "需处理" else "🔒"
            print(f"  {icon} [{o['status']}] {o['id']}  {o['problems'] or ''}")
        print(f"\n排除出训练集：{excl}  建议：排除项不出集，需处理项补全后再进")

if __name__ == "__main__":
    main()
