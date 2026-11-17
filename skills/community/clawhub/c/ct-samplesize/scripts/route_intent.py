#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""route_intent.py — 能力发现：方案段落/自然语言 → 建议的检验类型（P2-7，2026-11-15）。

背景（近 30 天飞书实证）：
  · 契约登记 67 种检验，窗口内只用到 16 种（24%），52 种零调用；
  · 同期 ct-advisor 317 条问答中 75 条（23.7%、44 个去重问题）涉及样本量/效能，
    且大量是「III 期 OS 生存 / 非劣效 / 方案审查」——恰好对应零调用的
    non_inferiority / survival_equivalence / group_sequential / cluster。
  → 能力存在但没被发现/没被路由。本模块提供零依赖的关键词打分建议，
    供 ct-advisor 交接、CLI「--suggest」与工作台菜单排序复用。

零第三方依赖；数据来自 publishable config/log_contract.json。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_CONTRACT = None

# 近 30 天真实使用频次（2026-10-17 ~ 11-12，252 行 ct-samplesize searchlog）
# 仅用于「同分时按热度排序」，不改变统计计算口径。
USAGE_FREQ = {
    "meta_planning": 149, "ci_prop": 16, "ttest_ind": 15, "survival": 10,
    "ni_survival": 6, "proportion_one": 5, "correlation": 5,
    "superiority_margin": 4, "ttest_paired": 4, "survival_exact": 3,
    "ci_mean": 3, "poisson": 2, "survival_superiority": 2,
    "cox_covariate": 1, "dose_escalation": 1, "proportion_two": 3,
}


def _load():
    global _CONTRACT
    if _CONTRACT is None:
        p = ROOT / "config" / "log_contract.json"
        _CONTRACT = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return _CONTRACT


def known_tests():
    return sorted((_load().get("tests") or {}).keys())


def suggest_tests(query, top_k=3):
    """按关键词命中打分，返回 [(test, score, hit_keywords), ...]。"""
    q = str(query or "").lower()
    hints = _load().get("intent_hints") or {}
    scored = []
    for test, words in hints.items():
        hits = [w for w in words if w.lower() in q]
        if not hits:
            continue
        score = len(hits) * 10 + sum(len(w) for w in hits) / 10.0
        scored.append((test, round(score, 2), hits))
    if not scored:
        return []
    # 同分按真实使用频次排序（高频能力优先曝光）
    scored.sort(key=lambda x: (-x[1], -USAGE_FREQ.get(x[0], 0), x[0]))
    return scored[:top_k]


def handoff_hint(query):
    """给 ct-advisor 的交接提示：命中样本量类意图时建议转 ct-samplesize 计算。"""
    q = str(query or "").lower()
    size_words = ("样本量", "样本含量", "把握度", "检验效能", "power",
                  "sample size", "效能计算", "例数")
    if not any(w.lower() in q for w in size_words):
        return ""
    s = suggest_tests(query, top_k=3)
    if not s:
        return ("检测到样本量/效能类问题：如需数值计算，建议转 ct-samplesize；"
                "本技能可先协助梳理设计与假设。")
    names = "、".join(t for t, _, _ in s)
    return ("检测到样本量/效能类问题：建议转 ct-samplesize 做数值计算，"
            "候选检验类型：%s。请补充 α、把握度、效应量/率、单双侧与脱落率。" % names)


def menu_order():
    """按真实使用频次 + 契约全量排序的菜单顺序（高频前置，长尾折叠）。"""
    tests = known_tests()
    return sorted(tests, key=lambda t: (-USAGE_FREQ.get(t, 0), t))


def usage_coverage():
    used = set(USAGE_FREQ)
    total = len(known_tests())
    return {"used": len(used & set(known_tests())), "total": total,
            "unused": sorted(set(known_tests()) - used)}


if __name__ == "__main__":
    import sys
    text = " ".join(sys.argv[1:]) or "III期非小细胞肺癌，主要终点OS，非劣效设计，样本量怎么估算？"
    print("query:", text)
    print("suggest:", suggest_tests(text))
    print("handoff:", handoff_hint(text))
    print("coverage:", usage_coverage()["used"], "/", usage_coverage()["total"])
