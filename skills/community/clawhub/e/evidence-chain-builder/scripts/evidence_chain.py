# -*- coding: utf-8 -*-
"""evidence-chain-builder · AI 论断有证证据链 v1.0（LGD-II 有证实例化）
============================================================================
痛点：AI 张口就来、论断不可信、幻觉无法举证。
解法：把"论断 → 证据"拆成可验证的证据链。每条证据标注来源类型、是否可独立验证、可信度；
      输出「证成度」与**未支撑论断清单**。对齐 EIFP 不编造原教旨：本工具不判定论断真假，
      只评估证据质量；缺可验证证据的论断，明确标"勿作结论"。

用法：
  build --claim "论断" --evidences "证据1||证据2||证据3"
        （每条证据可带来源标记，用 @类型:来源 后缀，如 "2024年报@官方:统计局"）
  build --from file.json   # {claim, evidences:[{text, source, type}]}
  --json                   # 机器输出

证据类型 type ∈ official(官方) / paper(文献) / data(数据) / internal(内部) / assertion(主张)
可验证 verifiable：official/paper/data → 可独立核验；internal/assertion → 不可独立核验（降权）

零依赖（纯 stdlib）。© SynomosAI · LGD-Powered
"""
import argparse, json, sys, re

TYPES = ["official", "paper", "data", "internal", "assertion"]
VERIFIABLE = {"official": True, "paper": True, "data": True, "internal": False, "assertion": False}
TYPE_CN = {"official": "官方", "paper": "文献", "data": "数据", "internal": "内部", "assertion": "主张"}


def parse_evidence(text):
    """text 可含 @类型:来源 后缀，如 '2024年报@official:统计局'。"""
    src_type, source = "assertion", ""
    m = re.search(r"@(\w+):(.+)$", text)
    if m:
        t = m.group(1).lower()
        if t in TYPES:
            src_type, source = t, m.group(2).strip()
            text = text[:m.start()].strip()
    else:
        m2 = re.search(r"@(\w+)$", text)
        if m2 and m2.group(1).lower() in TYPES:
            src_type = m2.group(1).lower()
            text = text[:m2.start()].strip()
    return {"text": text, "type": src_type, "source": source}


def build(claim, evs):
    parsed = [parse_evidence(e) for e in evs if e.strip()]
    strong = [e for e in parsed if VERIFIABLE.get(e["type"])]
    score = round(100 * len(strong) / len(parsed)) if parsed else 0
    unsupported = score < 50
    return parsed, score, unsupported


def fmt(claim, parsed, score, unsupported, src):
    L = ["# AI 论断有证证据链（LGD-II 有证）", f"> 来源：{src}\n"]
    L.append(f"## 论断\n{claim}\n")
    L.append(f"## 证成度：**{score}/100**  （可独立验证证据 {sum(1 for e in parsed if VERIFIABLE[e['type']])}/{len(parsed)}）\n")
    L.append("## 证据链\n")
    for i, e in enumerate(parsed, 1):
        v = "可独立验证" if VERIFIABLE[e["type"]] else "不可独立验证(降权)"
        L.append(f"{i}. [{TYPE_CN[e['type']]}] {e['text']}  — 来源：{e['source'] or '未声明'}（{v}）")
    L.append("\n## 结论\n")
    if unsupported:
        L.append("⚠️ 该论断**缺少足够可验证证据**，按 EIFP 不编造原教旨：**勿将其作为确定结论使用**。")
        L.append("   补齐 official/paper/data 类可核验证据后再下结论。")
    else:
        L.append("✓ 证据链以可验证证据为主，论断具备基本证成度；最终判断仍须人工复核原始来源。")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="AI 论断有证证据链（LGD-II）")
    ap.add_argument("--claim", help="待证论断")
    ap.add_argument("--evidences", nargs="+", help="证据（可多条，或用 || 分隔）；可带 @类型:来源 后缀")
    ap.add_argument("--from", dest="from_file", help="JSON：{claim, evidences:[{text,source,type}]}")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.from_file:
        try:
            d = json.load(open(a.from_file, encoding="utf-8-sig"))
        except Exception as e:
            print(f"[!] 读取失败：{e}", file=sys.stderr); sys.exit(2)
        claim = d.get("claim", "")
        evs = [f"{e.get('text','')}@{e.get('type','assertion')}:{e.get('source','')}" if e.get("source") else f"{e.get('text','')}@{e.get('type','assertion')}" for e in d.get("evidences", [])]
    elif a.claim:
        claim = a.claim
        raw = a.evidences or []
        evs = []
        for r in raw:
            evs += r.split("||")
    else:
        print("[!] 用法：--claim \"论断\" --evidences \"e1||e2\" ｜ --from file.json", file=sys.stderr); sys.exit(1)

    if not claim.strip():
        print("[!] 论断不能为空", file=sys.stderr); sys.exit(2)
    parsed, score, unsupported = build(claim, evs)
    if a.json:
        print(json.dumps({"claim": claim, "score": score, "unsupported": unsupported,
                          "evidences": parsed}, ensure_ascii=False, indent=2))
    else:
        print(fmt(claim, parsed, score, unsupported, "evidence-chain-builder"))


if __name__ == "__main__":
    main()
