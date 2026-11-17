# -*- coding: utf-8 -*-
"""事实核查：声明列表对照来源文本，逐条标 已支撑/存疑/无来源。零依赖。"""
import argparse, json, pathlib, re

def load_lines(p):
    """支持三种输入：@文件路径 / 已存在的纯文件路径 / 内联文本(按行拆分)。"""
    if p.startswith("@"):
        p = p[1:]
    if pathlib.Path(p).is_file():
        raw = pathlib.Path(p).read_text(encoding="utf-8-sig")
    else:
        raw = p
    return [l.strip() for l in raw.splitlines() if l.strip()]

def support(claim, sources):
    c = claim.lower()
    # 抽取声明里的实体词（>=2字中文 或 >=4英文字母）
    ents = set(re.findall(r"[一-鿿]{2,}|[a-z]{4,}", c))
    if not ents:
        return "存疑", "无可比对实体"
    hits = 0
    for s in sources:
        sl = s.lower()
        if sum(1 for e in ents if e in sl) >= max(1, len(ents) // 2):
            hits += 1
    if hits >= 1:
        return "已支撑", f"来源命中 {hits} 处"
    return "无来源", "检索无实质支撑"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", required=True)
    ap.add_argument("--sources", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    claims = load_lines(a.claims)
    sources = load_lines(a.sources)
    out = []
    for c in claims:
        st, why = support(c, sources)
        out.append({"claim": c, "status": st, "why": why})
    if a.json:
        print(json.dumps({"results": out}, ensure_ascii=False, indent=2))
    else:
        for o in out:
            icon = "✅" if o["status"] == "已支撑" else "⚠️" if o["status"] == "存疑" else "🔒"
            print(f"  {icon} [{o['status']}] {o['claim']}  ({o['why']})")

if __name__ == "__main__":
    main()
