#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L3 结果解读：脱敏数值摘要外发解释（2026-11-09，用户拍板的增强版）。

与 `stitch_results.py`（纯本地、零网络 import）**刻意分模块**：本文件是唯一
允许在 `--stitch interpret=true` 下发起 Coze 出站的地方，且外发内容被严格
限制为「代码构造的纯方法学问题 + 字段白名单内的纯数值」。

🔴 F33 出域边界（全部由代码强制，非模型自觉）：
  * 出站 `original_question` 由 `interpret_question()` **代码构造**，
    **绝不复用用户原问题**（可能含药名 / 方案名 / 受试者信息）；
  * 外发数值来自 `stitch_results.build_numeric_summary()`：只认白名单键、
    只取有限数值、最多 12 个；md/csv/xlsx 正文、`text` 自由文本、
    文件名 / 路径 / 任何字符串 / ID 一律不出域；
  * `draft_answer` / `doc_context` / `conversation_history` / 附件全部为空；
  * 出站前显式过 `_check_outbound_authorization`（config.json 端点白名单）；
  * 云端若返回 `need_tool` / 空答案 / 任何错误字段 → **不采用**解释，
    只交付本地机械汇总并说明原因，绝不伪造。

HARD GATE 不变：本模块只由 `entry.py --stitch` 调用，答案经 `_emit_plain`
单一出口输出；本地 LLM 不参与判断、不改写答案。
"""
from __future__ import annotations

import sys


def _local_only(local_summary: str, note: str, reason: str, zh: bool) -> str:
    """未外发 / 外发失败时的降级：本地汇总照常交付 + 明确标注原因。"""
    if zh:
        return (local_summary + "\n\n---\n\n## L3 方法学解释（未生成）\n\n"
                "⚠️ " + reason + "。**未发生任何出站**；上方本地机械汇总照常交付。\n\n"
                "脱敏摘要状态：" + note + "。")
    return (local_summary + "\n\n---\n\n## L3 methodology interpretation (not generated)\n\n"
            "⚠️ " + reason + " **No egress occurred**; the local mechanical summary "
            "above is delivered as usual.\n\nSanitized summary status: " + note + ".")


def run_interpret(spec: dict, local_summary: str, config_path: str) -> str:
    """`--stitch` 的 interpret 分支入口。永不抛异常，永远返回可交付文本。"""
    from stitch_results import build_numeric_summary, interpret_question, _zh

    question = str(spec.get("question") or "")
    zh = _zh(question) or not question
    summary, note = build_numeric_summary(spec)

    if not summary:
        return _local_only(
            local_summary, note,
            "产物中没有字段白名单内的可外发数值（或非 JSON 产物），已跳过云端解释"
            if zh else "No allowlisted numeric values were found in the outputs, "
                       "so the cloud interpretation was skipped", zh)

    # ── 出站授权（显式检查，不依赖下游隐式行为）─────────────────────────
    try:
        from refine_answer import _check_outbound_authorization, _get_endpoint_from_config
        endpoint = _get_endpoint_from_config(config_path)
        if not endpoint or not _check_outbound_authorization(endpoint, config_path):
            return _local_only(
                local_summary, note,
                "Coze 端点不在 auto_approve_endpoints 授权白名单中，已拦截出站"
                if zh else "The Coze endpoint is not in auto_approve_endpoints; "
                           "outbound was blocked", zh)
    except Exception as e:  # noqa: BLE001
        return _local_only(
            local_summary, note,
            "出站授权检查失败（%s），已拦截出站" % type(e).__name__
            if zh else "Authorization check failed (%s); outbound was blocked" % type(e).__name__,
            zh)

    # ── 构造请求：纯方法学问题 + 脱敏数值，绝不带用户原问题 ──────────────
    prompt = interpret_question(summary, zh)
    try:
        from adapters import RefineRequest
        from orchestrate import _fire_coze
        req = RefineRequest(
            query_meta={"difficulty": "forwarded", "output_format": "l3_interpret",
                        "domain_hint": "methodology"},
            original_question=prompt,
            draft_answer="",
        )
        sys.stderr.write(
            "[entry] L3 interpret: 出站仅含 %d 个白名单数值键（%s），"
            "原始产物/用户原问题未出域\n" % (len(summary), ",".join(sorted(summary))))
        res = _fire_coze(req, config_path)
    except Exception as e:  # noqa: BLE001
        return _local_only(
            local_summary, note,
            "云端解释请求失败（%s），已回退本地汇总" % type(e).__name__
            if zh else "Cloud interpretation request failed (%s); fell back to "
                       "the local summary" % type(e).__name__, zh)

    problems = []
    for attr in ("dependency_error", "connection_error", "internal_error"):
        v = getattr(res, attr, None)
        if v:
            problems.append(str(v)[:200])
    if getattr(res, "need_tool", None):
        problems.append("云端返回 need_tool=%s" % res.need_tool
                        if zh else "cloud returned need_tool=%s" % res.need_tool)
    ans = str(getattr(res, "final_answer", "") or "").strip()
    if not ans or ans == prompt.strip():
        problems.append("云端未返回有效解释" if zh else "cloud returned no usable interpretation")

    if problems:
        reason = ("云端解释未采用：" + "；".join(problems[:3])) if zh else \
                 ("Cloud interpretation not used: " + "; ".join(problems[:3]))
        return _local_only(local_summary, note, reason, zh)

    # ── 缝合：本地机械汇总 + 云端方法学解释 + 明确的出域标注 ──────────────
    sent = "; ".join("%s=%s" % (k, v) for k, v in sorted(summary.items()))
    if zh:
        section = (
            "\n\n---\n\n## L3 方法学解释（脱敏数值摘要已出站）\n\n"
            + ans + "\n\n---\n\n"
            "🔒 **出域说明**：本次仅向 Coze 端点发送了由代码构造的纯方法学问题，"
            "以及下列**字段白名单内的纯数值**：\n\n`" + sent + "`\n\n"
            "原始产物文本、文件名、路径、药名、方案名、试验编号、受试者数据与"
            "**用户原问题**均未出域。" + note + "。\n\n"
            "⚠️ 上述解释是方法学说明，**非取数结果**，不得据此改写、推断或补齐"
            "原始数值；结论一律以各技能原始产物为准，不得用于注册申报、信号判定"
            "或临床决策。")
    else:
        section = (
            "\n\n---\n\n## L3 methodology interpretation (sanitized numerics sent)\n\n"
            + ans + "\n\n---\n\n"
            "🔒 **Egress notice**: only a code-built methodology question and the "
            "following allowlisted numeric values were sent to the Coze endpoint:\n\n`"
            + sent + "`\n\n"
            "Original output text, file names, paths, drug/protocol names, trial IDs, "
            "subject data and the **user's original question** never left this machine. "
            + note + ".\n\n"
            "⚠️ The interpretation above is a methodology explanation, **not a data "
            "result**; do not use it to rewrite, infer or complete the original "
            "values. Rely on each skill's original output; not audit-grade and not "
            "for regulatory submissions, signal decisions or clinical decisions.")
    return local_summary + section
