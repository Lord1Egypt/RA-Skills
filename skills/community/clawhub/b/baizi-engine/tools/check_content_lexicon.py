#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""门禁⑦：断语内容合规词表（绝对化 / 恐吓性 / 健康越界 / 性别刻板）

背景：v1.3.9 用人工方式清了一遍「必有 / 血光 / 克妻」等表述，但没有任何门禁阻止以后新增规则又写回去。
本门禁把那次的判据固化为可复跑脚本，CI 每次提交都跑。

判定（任一命中即失败）：
  1. 绝对化表述（必有 / 必然 / 必定 / 注定 / 绝对 / 一定会）—— 「并非必然…」这类否定用法豁免
  2. 恐吓性表述（血光 / 自杀 / 轻生 / 死亡 / 致死 / 夭折 / 短命 / 残疾 / 残废 / 牢狱 / 绝后 / 横死 / 凶死 / 大凶 / 癌症 / 精神病）
  3. 健康类断语三字段（conclusion/suggestion/source）必须出现就医/医学/遵医嘱/心理/体检/专业帮助等兜底提示
  4. 使用「克夫 / 克妻」等传统表述的规则，必须同时出现「古称 / 传统 / 现代」做出时代对冲
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "kb/04-rules-db/rules.json"

ABSOLUTE = re.compile(r"必有|必然|必定|注定|绝对|一定会")
NEGATION = re.compile(r"并非|不是|非必然|未必|不一定|不会|避免|不宜|勿|忌|防止|难以|未必")
DARK = re.compile(r"血光|自杀|轻生|死亡|致死|夭折|短命|残疾|残废|牢狱|绝后|横死|凶死|大凶|癌症|精神病")
HEALTH_FALLBACK = re.compile(r"医学|就医|医师|医嘱|心理|体检|专业帮助|遵医嘱")
HEDGE = re.compile(r"古称|传统|现代")
GENDERED = re.compile(r"克夫|克妻")

FIELDS = ("conclusion", "suggestion", "source")


def main() -> int:
    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))["rules"]
    problems = []

    for r in rules:
        rid = r.get("id", "?")
        text = " ".join(str(r.get(f, "")) for f in FIELDS)

        for m in ABSOLUTE.finditer(text):
            if NEGATION.search(text[max(0, m.start() - 10):m.start()]):
                continue  # 「并非必然」「未必…」等否定用法
            problems.append(f"[绝对化] {rid}: ……{text[max(0, m.start() - 12):m.end() + 12]}……")

        for m in DARK.finditer(text):
            problems.append(f"[恐吓性] {rid}: ……{text[max(0, m.start() - 12):m.end() + 12]}……")

        if r.get("category") == "健康" and not HEALTH_FALLBACK.search(text):
            problems.append(f"[健康兜底缺失] {rid}: 三字段均无就医/医学/遵医嘱类提示")

        if GENDERED.search(text) and not HEDGE.search(text):
            problems.append(f"[性别刻板无对冲] {rid}: 使用「克夫/克妻」但无「古称/传统/现代」对冲")

    print(f"内容合规词表扫描：{len(rules)} 条规则（字段：{'/'.join(FIELDS)}）")
    if problems:
        print(f"\n❌ 命中 {len(problems)} 处：")
        for p in problems[:60]:
            print("   " + p)
        if len(problems) > 60:
            print(f"   …… 另有 {len(problems) - 60} 处")
        print("\n处置：软化表述（加时代对冲/免责）、或改成非绝对语气；健康类必须给就医提示。")
        return 1
    print("✅ 无绝对化 / 无恐吓性表述；健康类兜底齐全；传统性别表述均有时代对冲")
    return 0


if __name__ == "__main__":
    sys.exit(main())
