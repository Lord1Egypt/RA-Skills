#!/usr/bin/env python3
"""suggest_card.py — 评测资产段：bad case → 修订建议卡片（ai-data-delivery v0.0.4）

RULE-LOOP-01 的出口：登记卡 triage 出归因层之后，自动生成一张"修订建议卡片"，
把证据、建议动作（精确到命令）、影响面、回归占位写成一页，FDE 评审照单执行即可。

用法：
  python suggest_card.py --card badcases/BC001.yaml --out suggest.md
归因层 → 建议动作映射：
  词表层 → patch_model.py syn 补同义词（指标/数据集/概念三目标）
  引擎层 → 检索/生成链路排查；修完 run_eval.py 定向回归
  口径层 → patch_model.py struct 落地口径 + --db 物理库验算（--expect 对拍）；ratio 类检查分子分母
登记卡 layer 未定时：依据证据自动推断归因候选并在卡片标注"推断·待确认"，不阻断流水线。
证据兼容：retrieval 兼容 list/dict 两种存储；reasoning 兼容 list/str。
退出码：0 成功；2 登记卡不存在或不可解析。
"""
import os
import argparse
import sys

import yaml
from _contract import load

LAYER_ACTIONS = {
    "词表层": [
        "确认问句中的业务黑话/别名未命中模型同义词",
        "patch_model.py syn --metric/--dataset/--concept 补同义词（幂等，可反复执行）",
        "补完跑 run_eval.py 定向回归该问句"],
    "引擎层": [
        "保留证据三件套（应答/检索/模型快照），复现检索命中偏差",
        "排查检索打分与生成链路；必要时升级引擎版本",
        "plan_stability.py 抽查同句多次执行的计划一致性"],
    "口径层": [
        "确认指标口径缺失或错误（expr/分子分母/extra_where/time_field）",
        "patch_model.py struct 落地口径，必须 --db 直连物理库验算（--expect 对拍金标准值）",
        "reconcile_paths.py 双路径对账，确认指标路径与问数路径一致"],
}


def infer_layer(hits, ans, reasoning):
    """依据证据推断归因候选层。返回 (layer, 推断理由)。"""
    if ans.get("rejected"):
        r = str(ans.get("reason") or "") + str(reasoning or "")
        if "守卫" in r or "越界" in r or "超出" in r:
            return "引擎层", f"引擎拒答（{ans.get('reason') or '守卫拦截'}），拒绝判定归引擎层"
        return "引擎层", "引擎拒答，拒绝判定归引擎层"
    if not hits:
        return "词表层", "检索零命中——问句中的实体/指标未进模型词表"
    top = hits[0]
    if (top.get("score") or 0) < 5:
        return "词表层", f"检索最高分仅 {top.get('score')}（{top.get('name')}），疑似弱命中"
    return "口径层", f"检索命中 {top.get('name')}（score={top.get('score')}）且引擎已答，" \
                     "若数值不对则口径优先"


def evidence_hints(layer, hits, ans, reasoning):
    """结合本案证据的针对性建议（补在通用动作之后）。"""
    out = []
    if hits:
        top = hits[0]
        out.append(f"检索 Top1：{top.get('name')}（{top.get('id')}，score={top.get('score')}）"
                   f"——{'命中合理，问题在下游' if (top.get('score') or 0) >= 10 else '分数偏低，先查词表'}")
    if ans.get("sql"):
        out.append("抓到的实际 SQL 可直接在物理库重跑，与期望对拍定位差异行")
    if reasoning:
        out.append("推理链已附在证据区——逐环对照意图识别/路由/过滤/守卫，断在哪环修哪环")
    return out


def main():
    ap = argparse.ArgumentParser(description="bad case → 修订建议卡片")
    ap.add_argument("--card", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    c = load(args.card)
    ev = c.get("evidence") or {}

    # 证据归一：retrieval 兼容 list / dict{hits}；reasoning 兼容 list / str
    retr = ev.get("retrieval") or {}
    if isinstance(retr, list):
        retr = {"hits": retr}
    hits = retr.get("hits") or []
    ans = ev.get("answer") or {}
    reasoning = ans.get("reasoning")
    if isinstance(reasoning, list):
        reasoning = "；".join(str(x) for x in reasoning)

    layer = c.get("layer")
    inferred = False
    if not layer or layer not in LAYER_ACTIONS:
        # 依据证据推断归因候选，标注"待确认"照常出卡（不阻断流水线）
        layer, why_infer = infer_layer(hits, ans, reasoning)
        inferred = True
        print(f"提示：登记卡 layer 未定，依据证据推断为「{layer}」（{why_infer}）——"
              f"请人工确认后回填", file=sys.stderr)

    L = []
    L.append(f"# 修订建议卡片：{c.get('id')}")
    L.append("")
    L.append(f"- 问句：{c.get('question')}")
    mark = "（推断·待确认）" if inferred else ""
    L.append(f"- 归因层：**{layer}**{mark}　症状：{c.get('symptom', '—')}")
    L.append(f"- 取证时间：{c.get('captured_at', '—')}　来源：{c.get('source', 'capture_case')}")
    L.append("")
    L.append("## 证据")
    L.append("")
    if ev:
        ms = ev.get("model_snapshot") or {}
        L.append(f"- 模型快照：version={ms.get('modelVersion', '?')} 指标数={ms.get('total', '?')}")
        L.append(f"- 检索命中：{[(h.get('name'), h.get('score')) for h in hits] or '无'}")
        L.append(f"- 引擎应答：value={ans.get('value')} rejected={ans.get('rejected')}")
        if ans.get("reason"):
            L.append(f"- 拒答理由：{ans['reason']}")
        if reasoning:
            L.append(f"- 推理链：{str(reasoning)[:200]}")
        if ans.get("sql"):
            L.append(f"- 实际 SQL：`{ans['sql']}`")
    else:
        L.append("- （无活引擎证据——建议先跑 capture_case.py 补取证）")
    L.append("")
    L.append("## 建议动作")
    L.append("")
    for i, a in enumerate(LAYER_ACTIONS[layer]):
        L.append(f"{i}. {a}")
    # 证据相关的针对性补充
    extra = evidence_hints(layer, hits, ans, reasoning)
    if extra:
        L.append("")
        L.append("结合本案证据：")
        L.append("")
        for a in extra:
            L.append(f"- {a}")
    L.append("")
    L.append("## 影响面")
    L.append("")
    L.append("对修复对象（指标/字段/数据集）执行：")
    L.append("")
    L.append("```")
    L.append("python impact_analysis.py --model <semantic.yaml> --target <修复对象>")
    L.append("```")
    L.append("")
    L.append("## 回归占位")
    L.append("")
    L.append("- [ ] 修复已落地，verify 证据已回填登记卡")
    L.append("- [ ] promote_gold.py 回流评测集（expect 已填）")
    L.append("- [ ] run_eval.py 定向回归通过（附前后对比）")
    L.append("- [ ] 回归 gold_lint.py 无新增 ERROR")
    L.append("")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"修订建议卡片 → {args.out}（归因层：{layer}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
