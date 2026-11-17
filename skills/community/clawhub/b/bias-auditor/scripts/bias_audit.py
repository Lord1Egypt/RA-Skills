# -*- coding: utf-8 -*-
"""偏见审计：扫群体泛化/刻板归因/单边视角，标信号 + 去偏建议。零依赖。"""
import argparse, json, pathlib, re

GENERIC = ["都适合", "都不适合", "天生", "本来就该", "普遍不如", "普遍更强",
           "naturally", "born to"]
GROUP_TERMS = ["男", "女", "女生", "男生", "男性", "女性", "老人", "年轻人", "某地", "北方人", "南方人",
               "women", "men", "old", "young", "region"]
STEREOTYPE_BIND = [("技术", "男"), ("沟通", "女"), ("理性", "男"), ("细心", "女"),
                   ("护士", "女"), ("程序员", "男"), ("幼师", "女"), ("司机", "男"), ("领导", "男")]
# 地域/群体整体化句式：「X人都(是|会|爱|很|不)…」
REGION_STEREOTYPE = re.compile(r"[\u4e00-\u9fff]{1,4}(?:人都|人全都|人一般都)(?:是|会|爱|很|不)")

def audit(text):
    findings = []
    sents = [s for s in re.split(r"(?<=[。！？!?\n])", text) if s.strip()]
    # 群体泛化：仅在「同句同时出现群体词 + 泛化词」时才判，避免普通祈使句误报
    for sent in sents:
        low = sent.lower()
        if not any(g in sent for g in GROUP_TERMS):
            continue
        for g in GENERIC:
            if g.lower() in low:
                findings.append(("群体泛化", g, "改为个体表述，避免全称判断"))
    # 刻板归因：能力词与群体词需同句共现（跨句各自出现不判）
    for sent in sents:
        for ability, grp in STEREOTYPE_BIND:
            if ability in sent and grp in sent:
                findings.append(("刻板归因", f"{ability}↔{grp}", "能力与群体无必然绑定，去绑"))
    # 地域/群体整体化句式
    m = REGION_STEREOTYPE.search(text)
    if m:
        findings.append(("地域刻板", m.group(0), "整体化判断改为个体表述"))
    if len(findings) == 0:
        findings.append(("无显著信号", "", "未发现明显群体泛化/刻板归因"))
    return findings

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = a.text if a.text else pathlib.Path(a.file).read_text(encoding="utf-8-sig")
    fs = audit(text)
    if a.json:
        print(json.dumps({"findings": [{"type": t, "hit": h, "fix": fx} for t, h, fx in fs]}, ensure_ascii=False, indent=2))
    else:
        for t, h, fx in fs:
            icon = "✅" if t == "无显著信号" else "⚠️"
            print(f"  {icon} [{t}] 命中：{h}  建议：{fx}")

if __name__ == "__main__":
    main()
