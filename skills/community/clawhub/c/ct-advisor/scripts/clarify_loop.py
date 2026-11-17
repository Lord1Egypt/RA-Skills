#!/usr/bin/env python3
"""ct-advisor 本地澄清循环（Step 0 Triage 之后、进入 local/Coze 分支之前）。

纯本地、零网络出域，仅依赖 Python 标准库（json / re / argparse / sys）。
用于替代旁路的 grill-me 逐分支追问：当问题歧义到会改变结论时，每轮仅生成
**1–3 个**高价值澄清问题，并维护 ``question_profile``（问题画像）与
``confirmation``（确认摘要）。设**硬上限轮次**（默认 3 轮），到达上限仍不可判
则带着 ``question_profile`` 进入后续分支，**绝不无限循环**。

设计原则（与 refine_answer.py 一致，内存流水线、零临时文件）：
  - 无状态：每轮由 agent 传入 ``original_question`` + ``previous_answers`` +
    累积的 ``question_profile`` / ``confirmation``，脚本重算并返回本轮结果；
    agent 持有跨轮状态，脚本永不自己循环。
  - 容错：任何异常都回退为 ``{"status": "decidable"}`` 让下游照常继续，
    绝不因脚本崩溃中断对话。

调用方式：
  echo '{...}' | python scripts/clarify_loop.py
  python scripts/clarify_loop.py --payload-inline '{...}'
  python scripts/clarify_loop.py --self-test      # 最小内联自测，不落临时文件

输入 JSON 字段（可选）：
  original_question : str   原始问题
  previous_answers  : list  本轮之前用户已给出的澄清回答（按轮顺序）
  question_profile  : dict  上一轮累积的问题画像（多轮累积）
  confirmation      : dict  上一轮确认摘要
  round             : int   当前轮次（默认 0）
  max_rounds        : int   硬上限轮次（默认 3）
  lang              : str   强制 'zh-CN' / 'en'；缺省按问题自动检测

输出 JSON 字段：
  status            : 'need_clarify' | 'decidable' | 'forced_decide'
  ambiguous         : bool  本轮是否仍存在会改变结论的歧义
  round             : int   当前轮次
  max_rounds        : int   硬上限
  questions         : list  本轮要问的 1–3 个高价值问题（status='need_clarify' 时有值）
  question_profile  : dict  累积问题画像
  confirmation      : dict  累积确认摘要（含 summary / answered / status）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# 编码修复：与 refine_answer.py 一致，强制三流 UTF-8，避免中文/emoji 在 Windows
# 控制台（cp936）下被错误解码/编码。
# ---------------------------------------------------------------------------
for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass


# ---------------------------------------------------------------------------
# 歧义信号定义
# ---------------------------------------------------------------------------
# 每个信号：type 作为去重/画像 slot 键；rank 表示"对结论的影响权重"（越大越优先）；
# ask_zh / ask_en 是该信号对应的高价值澄清问题模板；answer_hints 用于判定某条
# previous_answer 是否已回答该信号（命中任一关键词即视为已解决）。
SIGNALS = [
    {
        "type": "multi_intent",
        "rank": 100,
        "ask_zh": "您的问题似乎包含多个独立诉求，请告诉我要优先解决哪一个（或明确它们的关系）？",
        "ask_en": "Your question seems to bundle several independent asks — which one should I prioritise (or how do they relate)?",
        "answer_hints": [],  # 由 agent 收敛意图，不靠关键词命中
    },
    {
        "type": "missing_population",
        "rank": 80,
        "ask_zh": "请明确目标人群/受试者（如疾病、分期、线数、年龄层），这会改变结论的适用性。",
        "ask_en": "Please specify the target population/subjects (disease, stage, line of therapy, age) — it changes applicability.",
        "answer_hints": ["患者", "受试者", "人群", "病人", "participant", "patient", "population", "cohort", "subjects"],
    },
    {
        "type": "missing_comparator",
        "rank": 75,
        "ask_zh": "您希望与什么对照/比较（如标准治疗、安慰剂、另一药物）？",
        "ask_en": "What comparator do you want to compare against (e.g. standard of care, placebo, another drug)?",
        "answer_hints": ["对照", "比较", "对比", "优于", "vs", "versus", "placebo", "标准治疗", "soc", "comparator", "compare", "against"],
    },
    {
        "type": "missing_outcome",
        "rank": 70,
        "ask_zh": "请明确关注的终点/结局指标（如 OS、PFS、ORR、AE 发生率）。",
        "ask_en": "Which endpoint/outcome are you interested in (e.g. OS, PFS, ORR, AE rate)?",
        "answer_hints": ["终点", "结局", "指标", "os", "pfs", "orr", "ae", "endpoint", "outcome", "survival", "response"],
    },
    {
        "type": "missing_sample_size_params",
        "rank": 85,
        "ask_zh": "样本量计算需要关键参数：预期效应量（HR/OR/均值差）、α、把握度(power)、组间分配。目前已缺哪几项？",
        "ask_en": "Sample-size needs: effect size (HR/OR/mean diff), α, power, allocation. Which are still missing?",
        "answer_hints": ["hr", "or", "效应", "效应量", "均值差", "alpha", "α", "把握度", "power", "分配", "组间", "effect size"],
    },
    {
        "type": "vague_entity",
        "rank": 50,
        "ask_zh": "问题里的「这个/相关/某方面」指代不明确，能否给出具体对象或场景？",
        "ask_en": "The reference ('this / related / some aspect') is ambiguous — can you name the concrete object or scenario?",
        "answer_hints": ["具体", "指", "是", "指", "即", "namely", "specifically", "concrete", "scenario"],
    },
    {
        "type": "overly_broad",
        "rank": 40,
        "ask_zh": "这个问题范围较大，能否收窄到具体环节（设计/统计/法规/执行）或具体场景？",
        "ask_en": "This is broad — can you narrow it to a specific aspect (design/statistics/regulatory/operations) or scenario?",
        "answer_hints": ["设计", "统计", "法规", "执行", "环节", "场景", "design", "statistic", "regulatory", "operation"],
    },
]

_SIGNAL_BY_TYPE = {s["type"]: s for s in SIGNALS}

# 用于"多意图"检测的连词 / 标点（临床语境下连接不同诉求）
_MULTI_INTENT_PAT = re.compile(
    r"(和|以及|与|及|、|或|还是|或者|另外|同时|并且|并且|；|;)", re.UNICODE
)
_QUESTION_MARKS = re.compile(r"(\?|？)+")
_CJK = re.compile(r"[\u4e00-\u9fff]")


def _detect_lang(text: str) -> str:
    """按 CJK 占比自动检测语言；缺省 en。"""
    if not text:
        return "en"
    cjk = len(_CJK.findall(text))
    return "zh-CN" if cjk >= max(1, len(text) * 0.15) else "en"


def _detect_signals(text: str) -> List[Dict[str, Any]]:
    """基于启发式检测"会改变结论"的歧义信号。纯本地、无 LLM。"""
    signals: List[Dict[str, Any]] = []
    t = (text or "").strip()
    low = t.lower()

    # 1) 多意图：多个问号，或连词连接了不同临床概念
    qmarks = len(_QUESTION_MARKS.findall(t))
    if qmarks >= 2 or (len(_MULTI_INTENT_PAT.findall(t)) >= 2):
        signals.append(_SIGNAL_BY_TYPE["multi_intent"])

    # 2) 样本量缺参数：仅在「真正要求计算」时触发（含计算动词），
    #    方法论问法（如何/怎么估算）可直接回答，不视为歧义。
    if re.search(
        r"计算|算一下|算样本|需要多少|样本量.*多少|估计.*样本|"
        r"estimate the sample|calculate.*sample|compute.*sample|how many (subjects|patients)",
        low,
    ):
        param_hits = sum(
            1 for h in _SIGNAL_BY_TYPE["missing_sample_size_params"]["answer_hints"]
            if h in low
        )
        # 命中 < 3 个关键参数视为信息不足
        if param_hits < 3:
            signals.append(_SIGNAL_BY_TYPE["missing_sample_size_params"])

    # 3) 缺失人群 / 对照 / 终点：治疗或比较类问题缺核心 PICO 要素
    is_treatment = bool(re.search(r"治疗|用药|药物|方案|干预|therapy|treat|drug|regimen|intervention", low))
    is_compare = bool(re.search(r"比较|对比|优于|vs|versus|还是.*还是|compare|better than", low))
    has_pop = any(h in low for h in _SIGNAL_BY_TYPE["missing_population"]["answer_hints"])
    has_comp = any(h in low for h in _SIGNAL_BY_TYPE["missing_comparator"]["answer_hints"])
    has_out = any(h in low for h in _SIGNAL_BY_TYPE["missing_outcome"]["answer_hints"])
    if is_treatment and not has_pop:
        signals.append(_SIGNAL_BY_TYPE["missing_population"])
    if is_compare and not has_comp:
        signals.append(_SIGNAL_BY_TYPE["missing_comparator"])
    if (is_treatment or is_compare) and not has_out:
        signals.append(_SIGNAL_BY_TYPE["missing_outcome"])

    # 4) 模糊指代：极短问题或含模糊代词而无具体对象
    vague_pron = bool(re.search(r"这个|那个|它|相关|等等|等一下|某些|某个|方面|问题|this|that|it|related|some aspect", low))
    if vague_pron and len(t) < 40:
        signals.append(_SIGNAL_BY_TYPE["vague_entity"])

    # 5) 范围过宽：含"怎么做/如何/最好"且未收窄
    if re.search(r"怎么做|如何|怎样|什么最好|最好的|怎么弄|how to|how do|best way|what is the best", low) and len(t) < 50:
        signals.append(_SIGNAL_BY_TYPE["overly_broad"])

    # 6) 通用不确定性兜底（2026-08-21）：vague 但未命中任何具体信号时，
    #    仍问出 PICO 三要素——README 示例 5（"I'm not sure what I actually need…"）
    #    实测返回 0 问题的根因：既无多意图/样本量/治疗比较关键词，又非短句模糊指代。
    UNCERTAIN = re.compile(
        r"not sure|unsure|don'?t know|do not know|not certain|no idea|"
        r"half[- ]written|where (?:to )?start|what (?:i|we) (?:actually )?need|"
        r"不确定|不知道|不清楚|没想好|想不清楚|半成品|需要什么|帮我理理")
    if not signals and UNCERTAIN.search(low):
        for _t in ("missing_population", "missing_comparator", "missing_outcome"):
            if _t in _SIGNAL_BY_TYPE:
                signals.append(_SIGNAL_BY_TYPE[_t])

    # 去重（同一 type 只保留一次），保留出现顺序
    seen = set()
    unique = []
    for s in signals:
        if s["type"] not in seen:
            seen.add(s["type"])
            unique.append(s)
    return unique


def _is_resolved(sig_type: str, previous_answers: List[str]) -> bool:
    """判定某信号是否已被 previous_answers 中的任一条回答覆盖（启发式）。"""
    sig = _SIGNAL_BY_TYPE.get(sig_type)
    if not sig:
        return False
    hints = sig.get("answer_hints") or []
    if not hints:
        # 无关键词信号的"已解决"由画像 slot 显式标记，这里不直接判定
        return False
    for ans in previous_answers or []:
        a = (ans or "").lower()
        if any(h in a for h in hints):
            return True
    return False


def _build_profile(
    original_question: str,
    previous_answers: List[str],
    prior: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """累积问题画像：保留已收敛的 slot，重算仍开放的信号。"""
    qp: Dict[str, Any] = {
        "intent": (prior or {}).get("intent"),
        "population": (prior or {}).get("population"),
        "intervention": (prior or {}).get("intervention"),
        "comparator": (prior or {}).get("comparator"),
        "outcome": (prior or {}).get("outcome"),
        "scope": (prior or {}).get("scope"),
        "resolved_slots": list((prior or {}).get("resolved_slots", []) or []),
        "open_signals": [],
    }
    # 多意图：若已有回答且 prior 标记 resolved，则保持不变；否则保持开放
    sigs = _detect_signals(original_question + " " + " ".join(previous_answers or []))
    open_types = []
    for s in sigs:
        if s["type"] in ("multi_intent",) and s["type"] in qp["resolved_slots"]:
            continue
        if _is_resolved(s["type"], previous_answers or []):
            if s["type"] not in qp["resolved_slots"]:
                qp["resolved_slots"].append(s["type"])
            continue
        open_types.append(s["type"])
    qp["open_signals"] = open_types
    return qp


def _build_confirmation(
    qp: Dict[str, Any],
    answered: List[str],
    status: str,
    lang: str,
) -> Dict[str, Any]:
    """生成确认摘要（人类可读 + 结构化）。"""
    parts: List[str] = []
    if qp.get("population"):
        parts.append(("人群=" + qp["population"]) if lang == "zh-CN" else ("population=" + qp["population"]))
    if qp.get("comparator"):
        parts.append(("对照=" + qp["comparator"]) if lang == "zh-CN" else ("comparator=" + qp["comparator"]))
    if qp.get("outcome"):
        parts.append(("终点=" + qp["outcome"]) if lang == "zh-CN" else ("outcome=" + qp["outcome"]))
    if not parts:
        summary = (
            "已确认信息不足，将基于现有输入给出范围性结论。"
            if lang == "zh-CN" else
            "Insufficient confirmed detail; will give a scoped answer from current input."
        )
    else:
        summary = ("已确认：" + "；".join(parts)) if lang == "zh-CN" else ("Confirmed: " + "; ".join(parts))
    return {
        "summary": summary,
        "answered": answered,
        "resolved_slots": qp.get("resolved_slots", []),
        "status": status,
    }


def run_clarify(payload: Dict[str, Any]) -> Dict[str, Any]:
    """核心：执行一轮澄清评估，返回结果 JSON dict。"""
    original_question = str(payload.get("original_question", "") or "")
    previous_answers = [str(a) for a in (payload.get("previous_answers", []) or []) if str(a).strip()]
    prior_qp = payload.get("question_profile") or {}
    prior_conf = payload.get("confirmation") or {}
    round_no = int(payload.get("round", 0) or 0)
    max_rounds = int(payload.get("max_rounds", 3) or 3)
    if max_rounds < 1:
        max_rounds = 1
    lang = str(payload.get("lang") or "")
    if lang not in ("zh-CN", "en"):
        lang = _detect_lang(original_question + " " + " ".join(previous_answers))

    qp = _build_profile(original_question, previous_answers, prior_qp)
    open_types = qp.get("open_signals", [])

    # 已收敛的回答也累加到 confirmation.answered
    answered_history = list((prior_conf.get("answered") if isinstance(prior_conf, dict) else []) or [])
    answered_history.extend(previous_answers)

    # 判定状态：无开放信号 → 可判；轮次达上限 → 强制可判（带画像进入后续）
    if not open_types:
        status = "decidable"
        ambiguous = False
        questions: List[str] = []
    elif round_no >= max_rounds:
        status = "forced_decide"
        ambiguous = True
        questions = []
    else:
        status = "need_clarify"
        ambiguous = True
        # 每轮仅取影响权重最高的 1–3 个未解决信号
        open_sigs = sorted(
            (_SIGNAL_BY_TYPE[t] for t in open_types if t in _SIGNAL_BY_TYPE),
            key=lambda s: s["rank"],
            reverse=True,
        )
        questions = [(s["ask_zh"] if lang == "zh-CN" else s["ask_en"]) for s in open_sigs[:3]]

    confirmation = _build_confirmation(qp, answered_history, status, lang)
    return {
        "status": status,
        "ambiguous": ambiguous,
        "round": round_no,
        "max_rounds": max_rounds,
        "questions": questions,
        "question_profile": qp,
        "confirmation": confirmation,
    }


def _read_payload(args) -> Dict[str, Any]:
    if args.payload_inline:
        raw = args.payload_inline
    else:
        raw = sys.stdin.read()
    try:
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            obj = {}
    except Exception:
        obj = {}
    return obj


def _self_test() -> int:
    """最小内联自测：验证澄清循环可调用、不死循环、能收敛。不落临时文件。"""
    ok = True

    # 场景 1：歧义问题 → 应给出 1–3 个问题且 status=need_clarify
    r1 = run_clarify({
        "original_question": "这个药和那个方案比较哪个好？",
        "previous_answers": [],
        "round": 0, "max_rounds": 3,
    })
    cond1 = (
        r1["status"] == "need_clarify"
        and 1 <= len(r1["questions"]) <= 3
        and r1["ambiguous"] is True
        and "question_profile" in r1 and "confirmation" in r1
    )
    print(f"[self-test] scenario1 ambiguous -> {r1['status']}, questions={len(r1['questions'])} : {'PASS' if cond1 else 'FAIL'}")
    ok = ok and cond1

    # 场景 2：连跑到硬上限 → 必须 forced_decide，绝不无限循环
    state = {
        "original_question": "这个药和那个方案比较哪个好？",
        "previous_answers": ["我不知道", "随便", "你定吧"],
        "round": 0, "max_rounds": 3,
    }
    last = None
    for i in range(10):  # 远超上限，验证循环被强制截断
        last = run_clarify({**state, "round": i})
        if last["status"] in ("forced_decide", "decidable"):
            break
    cond2 = last is not None and last["status"] == "forced_decide" and last["round"] == 3
    print(f"[self-test] scenario2 cap-hit -> {last['status']} @round={last['round']} : {'PASS' if cond2 else 'FAIL'}")
    ok = ok and cond2

    # 场景 3：清晰问题 → 直接 decidable，无问题
    r3 = run_clarify({
        "original_question": "在 III 期 NSCLC 患者中，对比 pembrolizumab 与化疗，主要终点 OS 的样本量如何估算？",
        "previous_answers": [],
        "round": 0, "max_rounds": 3,
    })
    cond3 = r3["status"] == "decidable" and len(r3["questions"]) == 0
    print(f"[self-test] scenario3 clear -> {r3['status']}, questions={len(r3['questions'])} : {'PASS' if cond3 else 'FAIL'}")
    ok = ok and cond3

    # 场景 4：跨轮收敛 → 提供关键回答后 decidable
    r4 = run_clarify({
        "original_question": "样本量怎么算？",
        "previous_answers": ["HR=0.7，α=0.05，power=0.9，两组 1:1"],
        "round": 1, "max_rounds": 3,
    })
    cond4 = r4["status"] == "decidable"
    print(f"[self-test] scenario4 converge -> {r4['status']} : {'PASS' if cond4 else 'FAIL'}")
    ok = ok and cond4

    print(f"[self-test] overall: {'ALL PASS' if ok else 'FAILED'}")
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(description="ct-advisor local clarification loop (pure-local, no network call)")
    ap.add_argument("--payload-inline", help="inline JSON payload string (highest priority)")
    ap.add_argument("--self-test", action="store_true", help="run minimal inline self-test, no temp files")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(_self_test())

    payload = _read_payload(args)
    try:
        result = run_clarify(payload)
    except Exception as e:  # noqa: BLE001
        # 容错：任何异常都回退为可判，绝不中断下游
        result = {
            "status": "decidable",
            "ambiguous": False,
            "round": int(payload.get("round", 0) or 0),
            "max_rounds": int(payload.get("max_rounds", 3) or 3),
            "questions": [],
            "question_profile": payload.get("question_profile") or {},
            "confirmation": payload.get("confirmation") or {},
            "error": f"{type(e).__name__}: {e}",
        }
    sys.stdout.write(json.dumps(result, ensure_ascii=False))
    sys.stdout.write("\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
