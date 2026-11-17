#!/usr/bin/env python3
"""
lesson_plan_guard.py - 瑙勫垯灞傚閿欙紙8 椤圭‖瑙勫垯锛?

V7-AIPC 瑙勫垯灞傦細鍦?plan 杩涘叆 SDK/浜戠涔嬪墠鍋氱‖鏍獙锛圴7.3 鍗囩骇鐗?+ 涓?work_summary 鑱斿姩锛夈?
8 椤圭‖瑙勫垯 (G001 ~ G008)锛?
  G001 plan 寮曠敤 鈮?min_unique_knowledge_points 涓笉鍚?knowledge_point
  G002 鐩搁偦 clip 闅惧害绛夌骇宸?鈮?max_difficulty_jump
  G003 plan 涓嫢鍚?abstract_data锛屽簭鍒楀寲瀛楄妭鏁?< abstract_data_max_bytes (10KB)
  G004 plan 涓?assessment.questions 鏁伴噺 鈮?min_assessment_questions 涓旀瘡棰樻湁 answer
  G005 姣忎釜 clip 鏃堕暱 鈭?[min_clip_duration_sec, max_clip_duration_sec]
  G006 plan 涓?pedagogy_method 鈭?valid_pedagogy_methods
  G007 plan 涓?learning_objectives 鑷冲皯 1 涓紝涓旀瘡鏉'互 valid verb 寮澶?
  G008 cost_monitor 宸茶鍙戠啍鏂?鈫?鐩存帴鎷掔粷

CLI:
    python lesson_plan_guard.py --plan plan.json [--candidates cand.json] [--json]
"""
from __future__ import annotations
__version__ = "8.1.0-aipc"  # V8.1-AIPC: 每次工作自动输出本地/云端对比 + 全互动控件完整性门控


# --- UTF-8 stdout/stderr (Windows 涓枃杈撳嚭闃蹭贡鐮? -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple
import uuid


# ---------------------------------------------------------------------------
# 瑙勫垯閰嶇疆
# ---------------------------------------------------------------------------

@dataclass
class RuleConfig:
    """8 椤圭‖瑙勫垯鐨勯厤缃泦鍚堛?"""
    # G001: 鑷冲皯寮曠敤鐨勪笉鍚?knowledge_point 鏁伴噺锛堝幓閲嶅悗锛?
    min_unique_knowledge_points: int = 3
    # G002: 鐩搁偦 clip 闅惧害绛夌骇鏈澶樊
    max_difficulty_jump: int = 2
    # G003: abstract_data 搴忓垪鍖栧悗鏈澶瓧鑺傛暟锛堥粯璁?10KB = 10240B锛?
    abstract_data_max_bytes: int = 10240
    # G004: 璇勪及闂鏈灏戦鏁?
    min_assessment_questions: int = 3
    # G005: clip 鏃堕暱涓婁笅闄愶紙绉掞級
    min_clip_duration_sec: float = 60.0
    max_clip_duration_sec: float = 600.0
    # G006: 教法学白名单
    valid_pedagogy_methods: FrozenSet[str] = frozenset(
        {"5E", "PBL", "讲授法", "翻转课堂"}
    )
    # G007: 学习目标动词白名单（布鲁姆分类法中文版的高频动词）
    valid_learning_objective_verbs: FrozenSet[str] = frozenset(
        {"记忆", "理解", "掌握", "应用", "分析", "评价", "创造"}
    )
    # G002 辅助：合法难度等级 (1~5)
    valid_difficulty_levels: FrozenSet[int] = frozenset({1, 2, 3, 4, 5})


# ---------------------------------------------------------------------------
# 杈呭姪鍑芥暟
# ---------------------------------------------------------------------------

def normalize_kp(raw: Any) -> str:
    """知识点归一化: 去空白 + 统一小写, 便于去重比较."""
    if raw is None:
        return ""
    return str(raw).strip().lower()


_WS_PATTERN = re.compile(r"\s+")


def _norm_obj_text(raw: Any) -> str:
    """鏇存縺杩涚殑鏂囨湰褰掍竴鍖栵細鍘绘墍鏈夌鐧斤紙灏忓啓鍓?鍚庯級銆?"""
    if raw is None:
        return ""
    return _WS_PATTERN.sub("", str(raw)).strip().lower()


def _is_circuit_breaker_triggered(cost_monitor: Any) -> bool:
    """鍏煎澶氱 cost_monitor 鐔旀柇妫娴嬫帴鍙n紙duck-typing锛夈?"""
    if cost_monitor is None:
        return False
    # 1) 鏂规硶锛歩s_circuit_breaker_triggered()
    fn = getattr(cost_monitor, "is_circuit_breaker_triggered", None)
    if callable(fn):
        try:
            return bool(fn())
        except Exception:
            return False
    # 2) 灞炴細circuit_breaker_triggered / triggered / circuit_breaker_open
    for attr in (
        "circuit_breaker_triggered",
        "circuit_breaker_open",
        "triggered",
        "is_open",
    ):
        if hasattr(cost_monitor, attr):
            try:
                return bool(getattr(cost_monitor, attr))
            except Exception:
                return False
    # 3) 鍏滃簳锛歝umulative_cost_usd >= monthly_budget_usd
    cum = _get_cumulative_cost(cost_monitor)
    budget = _get_monthly_budget(cost_monitor)
    if budget is not None and budget > 0:
        return cum >= budget
    return False


def _get_cumulative_cost(cost_monitor: Any) -> float:
    if cost_monitor is None:
        return 0.0
    for attr in ("cumulative_cost_usd", "cumulative_cost", "total_cost_usd", "cost_usd"):
        if hasattr(cost_monitor, attr):
            try:
                return float(getattr(cost_monitor, attr))
            except Exception:
                continue
    return 0.0


def _get_monthly_budget(cost_monitor: Any) -> Optional[float]:
    if cost_monitor is None:
        return None
    for attr in ("monthly_budget_usd", "monthly_budget", "budget_usd", "budget"):
        if hasattr(cost_monitor, attr):
            try:
                v = float(getattr(cost_monitor, attr))
                return v
            except Exception:
                continue
    return None


# ---------------------------------------------------------------------------
# plan 缁撴瀯瑙e瀽
# ---------------------------------------------------------------------------

def _get_clips(plan: Any) -> List[dict]:
    """从 plan 中提取 clip 列表 (兼容 clips / lessons[].clips / segments)."""
    if not isinstance(plan, dict):
        return []
    clips = plan.get("clips")
    if isinstance(clips, list):
        return [c for c in clips if isinstance(c, dict)]
    lessons = plan.get("lessons")
    if isinstance(lessons, list):
        out: List[dict] = []
        for l in lessons:
            if isinstance(l, dict):
                cs = l.get("clips")
                if isinstance(cs, list):
                    out.extend(c for c in cs if isinstance(c, dict))
        return out
    segments = plan.get("segments")
    if isinstance(segments, list):
        return [s for s in segments if isinstance(s, dict)]
    return []


def _collect_unique_kps(plan: Any) -> Set[str]:
    """浠?plan 鏀堕泦鎵鏈?knowledge_point锛屽綊涓鍖栧悗鍘婚噸銆?"""
    kps: Set[str] = set()
    if not isinstance(plan, dict):
        return kps

    def _walk(value: Any) -> None:
        if value is None:
            return
        if isinstance(value, str):
            n = normalize_kp(value)
            if n:
                kps.add(n)
            return
        if isinstance(value, (int, float)):
            # 鏁板瓧鐭瘑鐐癸紙濡傜紪鍙凤級杞瓧绗覆
            n = normalize_kp(value)
            if n:
                kps.add(n)
            return
        if isinstance(value, list):
            for x in value:
                _walk(x)
            return
        if isinstance(value, dict):
            # 鍙栧嚭鍏抽敭瀛楁
            for key in ("knowledge_point", "knowledge_points", "kps", "kp",
                        "topic", "topics", "name", "label"):
                if key in value:
                    _walk(value[key])

    # 椤跺眰瀛楁
    for key in ("knowledge_points", "knowledge_point", "kps", "topics"):
        if key in plan:
            _walk(plan[key])

    # clips 鍐呴儴
    for c in _get_clips(plan):
        for key in ("knowledge_point", "knowledge_points", "kps", "topic", "topics"):
            if key in c:
                _walk(c[key])

    # lessons 鍐呴儴
    lessons = plan.get("lessons")
    if isinstance(lessons, list):
        for l in lessons:
            if not isinstance(l, dict):
                continue
            for key in ("knowledge_point", "knowledge_points", "kps", "topic", "topics"):
                if key in l:
                    _walk(l[key])
            for c in l.get("clips", []) or []:
                if isinstance(c, dict):
                    for key in ("knowledge_point", "knowledge_points", "kps", "topic", "topics"):
                        if key in c:
                            _walk(c[key])

    kps.discard("")
    return kps


def _get_clip_difficulty(clip: Any) -> Optional[int]:
    """浠?clip 涓幏鍙栭毦搴瓑绾紙1~5锛夈?"""
    if not isinstance(clip, dict):
        return None
    for key in ("difficulty", "difficulty_level", "level"):
        if key in clip and clip[key] is not None:
            try:
                return int(clip[key])
            except (TypeError, ValueError):
                return None
    meta = clip.get("metadata") or {}
    if isinstance(meta, dict):
        for key in ("difficulty", "difficulty_level", "level"):
            if key in meta and meta[key] is not None:
                try:
                    return int(meta[key])
                except (TypeError, ValueError):
                    return None
    return None


def _get_clip_duration_sec(clip: Any) -> Optional[float]:
    """浠?clip 涓幏鍙栨椂闀匡紙绉掞級銆?"""
    if not isinstance(clip, dict):
        return None
    # 1) 椤跺眰鏄惧紡 duration 瀛楁
    for key in ("duration_sec", "duration_seconds", "duration"):
        if key in clip and clip[key] is not None:
            try:
                v = float(clip[key])
                if v >= 0:
                    return v
            except (TypeError, ValueError):
                pass
    # 2) timecode 宓屽
    tc = clip.get("timecode") or {}
    if isinstance(tc, dict):
        for key in ("duration", "duration_sec", "duration_seconds"):
            if key in tc and tc[key] is not None:
                try:
                    v = float(tc[key])
                    if v >= 0:
                        return v
                except (TypeError, ValueError):
                    pass
        try:
            ip = tc.get("in_point")
            op = tc.get("out_point")
            if ip is not None and op is not None:
                v = float(op) - float(ip)
                return v if v >= 0 else None
        except (TypeError, ValueError):
            pass
    return None


def _abstract_data_size(abstract_data: Any) -> int:
    """璁#畻 abstract_data 搴忓垪鍖栧悗鐨勫瓧鑺傛暟锛圲TF-8锛夈?"""
    if abstract_data is None:
        return 0
    if isinstance(abstract_data, bytes):
        return len(abstract_data)
    if isinstance(abstract_data, str):
        try:
            return len(abstract_data.encode("utf-8"))
        except Exception:
            return len(abstract_data)
    try:
        return len(json.dumps(abstract_data, ensure_ascii=False).encode("utf-8"))
    except Exception:
        try:
            return len(str(abstract_data).encode("utf-8"))
        except Exception:
            return 0


def _get_assessment(plan: Any) -> dict:
    if not isinstance(plan, dict):
        return {}
    a = plan.get("assessment")
    if isinstance(a, dict):
        return a
    return {}


def _get_assessment_questions(plan: Any) -> List[Any]:
    a = _get_assessment(plan)
    qs = a.get("questions") if isinstance(a, dict) else None
    if isinstance(qs, list):
        return qs
    return []


def _get_pedagogy_method(plan: Any) -> Optional[str]:
    if not isinstance(plan, dict):
        return None
    for key in ("pedagogy_method", "teaching_method", "pedagogy", "method"):
        if key in plan and plan[key] is not None and str(plan[key]).strip():
            return str(plan[key]).strip()
    meta = plan.get("lesson_metadata") or plan.get("metadata") or {}
    if isinstance(meta, dict):
        for key in ("pedagogy_method", "teaching_method", "pedagogy", "method"):
            if key in meta and meta[key] is not None and str(meta[key]).strip():
                return str(meta[key]).strip()
    return None


def _get_learning_objectives(plan: Any) -> List[str]:
    out: List[str] = []
    if not isinstance(plan, dict):
        return out
    for key in ("learning_objectives", "objectives", "goals", "鏁欏鐩爣"):
        v = plan.get(key)
        if isinstance(v, list):
            for x in v:
                if x is not None and str(x).strip():
                    out.append(str(x).strip())
        elif isinstance(v, str) and v.strip():
            # 鍗曟潯瀛楃涓诧紝鎸夊彞鍙?鎹鎷嗗垎
            for chunk in re.split(r"[銆俓n;锛沒+", v):
                if chunk.strip():
                    out.append(chunk.strip())
    return out


def _objective_starts_with_verb(text: str, verbs: FrozenSet[str]) -> bool:
    """鍒柇鐩爣鏂囨湰鏄惁浠櫧鍚嶅崟鍔瘝寮澶达紙鍏佽鍔瘝鍚庤窡绌烘牸/鏍囩偣/浠绘剰鍐呭锛夈?"""
    s = str(text or "").strip()
    if not s:
        return False
    for verb in verbs:
        if not verb:
            continue
        if s == verb:
            return True
        if s.startswith(verb):
            # 鍔瘝鍚庡繀椤绘槸闈炲瓧姣嶏紙涓枃/鏍囩偣/鏁板瓧/绌烘牸/鑻辨枃瀛楁瘝锛夋墠绠椾互鍔瘝寮澶?
            tail = s[len(verb):]
            if not tail:
                return True
            first = tail[0]
            # 涓枃琛剰鏂囧瓧锛歕u4e00-\u9fff
            if "\u4e00" <= first <= "\u9fff":
                return True
            if first in " \t,锛屻?;锛?锛?锛?锛熴?)锛堬級銆娿嬨愩慬]":
                return True
            # 鏁板瓧
            if first.isdigit():
                return True
            # 鑻辨枃瀛楁瘝锛堝厑璁?鐞嗚 CNN 鍘熺悊"绛夊惈鑻辨枃鏈鐨勫涔犵洰鏍囷級
            if ("a" <= first <= "z") or ("A" <= first <= "Z"):
                return True
    return False


# ---------------------------------------------------------------------------
# 鏍獙涓诲叆鍙?
# ---------------------------------------------------------------------------

def validate_lesson_plan(
    plan: Any,
    candidates: Optional[dict],
    cost_monitor: Any,
    config: Optional[RuleConfig] = None,
) -> Tuple[bool, List[dict]]:
    """鎵 8 椤圭‖瑙勫垯鏍獙銆?"

    Args:
        plan: lesson_plan dict锛堝繀濉級
        candidates: 鍊欓夌煡璇嗙偣/绱犳潗 dict锛堝彲閫夛紱褰撳墠涓哄墠鍚戝吋瀹逛繚鐣欙級
        cost_monitor: 鎴愭湰鐩戞帶瀵硅薄锛坉uck-typing锛歩s_circuit_breaker_triggered / 灞炴級
        config: RuleConfig锛圢one 鏃朵娇鐢粯璁級

    Returns:
        (passed, errors)锛歟rrors 姣忛]褰 {"code": "G001", "message": "...", "suggestion": "..."}
    """
    cfg = config or RuleConfig()
    errors: List[dict] = []

    if not isinstance(plan, dict):
        return False, [
            {
                "code": "G000",
                "message": "plan 蹇呴}涓?dict 绫诲瀷",
                "suggestion": "传入合法 lesson_plan dict (顶层 JSON 对象)",
            }
        ]

    # ---------------- G008: 鎴愭湰鐩戞帶鐔旀柇妫娴嬶紙鏈鍏堟鏌紝閬垮厤鏃犳晥宸綔锛?----------------
    if _is_circuit_breaker_triggered(cost_monitor):
        cum = _get_cumulative_cost(cost_monitor)
        budget = _get_monthly_budget(cost_monitor)
        budget_txt = f"{budget:.2f}" if budget is not None else "鏈煡"
        errors.append(
            {
                "code": "G008",
                "message": (
                    f"成本监控已触发熔断 (cumulative_cost_usd={cum:.4f} >= "
                    f"monthly_budget_usd={budget_txt}), 当前 lesson_plan 直接拒绝"
                ),
                "suggestion": (
                    "建议等待配额刷新或上调月度预算后重试。"
                    "熔断期间系统已自动切换到 Level 5 (完全本地) 模式"
                ),
            }
        )
        # 熔断触发时直接拒绝，跳过其他检查
        return False, errors

    # ---------------- G001: 至少 N 个不同 knowledge_point ----------------
    unique_kps = _collect_unique_kps(plan)
    if len(unique_kps) < cfg.min_unique_knowledge_points:
        errors.append(
            {
                "code": "G001",
                "message": (
                    f"知识点数量不足：当前 {len(unique_kps)} 个不同 knowledge_point "
                    f"（归一化去重后），要求至少 {cfg.min_unique_knowledge_points} 个"
                ),
                "suggestion": (
                    "在 plan['knowledge_points'] 或各 clip['knowledge_point'] 中补充更多"
                    f"不同的 knowledge_point，使归一化去重后数量 >= {cfg.min_unique_knowledge_points}。"
                    "避免同义/近义词（归一化按小写+去空白）"
                ),
            }
        )

    # ---------------- G002: 鐩搁偦 clip 闅惧害绛夌骇宸?鈮?max_difficulty_jump ----------------
    clips = _get_clips(plan)
    if not clips:
        # 娌湁 clips 涔熶笉鍏佽锛堝叾瀹冭鍒欏彲鑳芥棤娉曟牎楠岋級鈥斺旂粰涓涓蒋鎻愮浣嗕笉寮哄埗
        pass
    else:
        prev_difficulty: Optional[int] = None
        prev_idx: int = -1
        for i, c in enumerate(clips):
            d = _get_clip_difficulty(c)
            if d is None:
                # 缂洪毦搴俊鎭細閲嶇疆 prev锛岄伩鍏嶆妸 None 涓庢暟瀛楄姣旇緝
                prev_difficulty = None
                prev_idx = -1
                continue
            if d not in cfg.valid_difficulty_levels:
                errors.append(
                    {
                        "code": "G002",
                        "message": (
                            f"clip#{i+1}: 难度等级 {d} 不在合法集合 "
                            f"{sorted(cfg.valid_difficulty_levels)} 中"
                        ),
                        "suggestion": (
                            f"将难度调整为 1~5 之间的整数；建议起始难度 1-2，循序渐进，"
                            f"且相邻跨度 <= {cfg.max_difficulty_jump}"
                        ),
                    }
                )
            if prev_difficulty is not None and prev_idx >= 0:
                try:
                    jump = abs(int(d) - int(prev_difficulty))
                except (TypeError, ValueError):
                    jump = 0
                if jump > cfg.max_difficulty_jump:
                    errors.append(
                        {
                            "code": "G002",
                            "message": (
                                f"clip#{prev_idx+1}→clip#{i+1}: 难度跳跃 {jump} "
                                f"（{prev_difficulty} → {d}），"
                                f"超过阈值 {cfg.max_difficulty_jump}"
                            ),
                            "suggestion": (
                                f"调整中间 clip 的难度，使相邻跨度 <= {cfg.max_difficulty_jump}。"
                                "教学建议按螺旋式上升排列（差值 0~1）"
                            ),
                        }
                    )
            prev_difficulty = d
            prev_idx = i

    # ---------------- G003: abstract_data 浣撶 < 10KB ----------------
    if "abstract_data" in plan:
        size = _abstract_data_size(plan["abstract_data"])
        if size >= cfg.abstract_data_max_bytes:
            errors.append(
                {
                    "code": "G003",
                    "message": (
                        f"abstract_data 体积过大：{size} bytes，"
                        f"必须 < {cfg.abstract_data_max_bytes} bytes (10KB)"
                    ),
                    "suggestion": (
                        "绔晶鎴柇鎴栧帇缂?abstract_data锛屼粎淇濈暀涓庡喅绛栫浉鍏崇殑鍏抽敭瀛楁锛?"
                        "閬靛惊绔簯鍗忚 搂4.1 鏁版嵁澶皬绾潫"
                    ),
                }
            )

    # ---------------- G004: assessment.questions 鏁伴噺 鈮?N 涓旀瘡棰樻湁 answer ----------------
    questions = _get_assessment_questions(plan)
    if len(questions) < cfg.min_assessment_questions:
        errors.append(
            {
                "code": "G004",
                "message": (
                    f"璇勪及闂鏁伴噺涓嶈冻锛氬綋鍓?{len(questions)} 棰橈紝"
                    f"要求至少 {cfg.min_assessment_questions} 题"
                ),
                "suggestion": (
                    f"在 plan['assessment']['questions'] 中补充至 "
                    f">= {cfg.min_assessment_questions} 题（建议覆盖 记忆/理解/掌握 3 个层级）"
                ),
            }
        )
    else:
        missing_idx: List[int] = []
        for i, q in enumerate(questions):
            if not isinstance(q, dict):
                missing_idx.append(i)
                continue
            ans = q.get("answer")
            if ans is None:
                missing_idx.append(i)
                continue
            if isinstance(ans, str) and not ans.strip():
                missing_idx.append(i)
                continue
            if isinstance(ans, (list, dict)) and len(ans) == 0:
                missing_idx.append(i)
        if missing_idx:
            errors.append(
                {
                    "code": "G004",
                    "message": (
                        f"评估题缺少 answer：共 {len(missing_idx)} 题"
                        f"（索引 {missing_idx[:10]}{'…' if len(missing_idx) > 10 else ''}）"
                    ),
                    "suggestion": (
                        "涓烘瘡棰樿鍏?answer 瀛楁锛堟爣鍑嗙瓟妗堟垨绛旀瑕佺偣锛夛紱"
                        "answer 绫诲瀷鍙负 string / list / dict锛屼絾涓嶈兘涓虹"
                    ),
                }
            )

    # ---------------- G005: clip 鏃堕暱 鈭?[min, max] ----------------
    if clips:
        bad_clips: List[str] = []
        missing_dur: List[int] = []
        for i, c in enumerate(clips):
            d = _get_clip_duration_sec(c)
            if d is None:
                missing_dur.append(i + 1)
                continue
            if d < cfg.min_clip_duration_sec or d > cfg.max_clip_duration_sec:
                bad_clips.append(
                    f"clip#{i+1}:{d:.1f}s（要求"
                    f"{cfg.min_clip_duration_sec:.0f}~{cfg.max_clip_duration_sec:.0f}s）"
                )
        if missing_dur:
            errors.append(
                {
                    "code": "G005",
                    "message": (
                        f"以下 clip 缺少 duration 字段: clip# {missing_dur[:10]}"
                        f"{'…' if len(missing_dur) > 10 else ''}"
                    ),
                    "suggestion": (
                        "在 clip['duration_sec'] 或 clip['timecode']['in_point/out_point'] "
                        "中补齐时长（秒）"
                    ),
                }
            )
        if bad_clips:
            errors.append(
                {
                    "code": "G005",
                    "message": (
                        f"存在 {len(bad_clips)} 个 clip 时长不合规: "
                        + "; ".join(bad_clips[:5])
                        + ("…" if len(bad_clips) > 5 else "")
                    ),
                    "suggestion": (
                        f"调整每个 clip 时长至{cfg.min_clip_duration_sec:.0f}~"
                        f"{cfg.max_clip_duration_sec:.0f} 秒之间"
                    ),
                }
            )

    # ---------------- G006: pedagogy_method 鐧藉悕鍗?----------------
    method = _get_pedagogy_method(plan)
    if method is None:
        errors.append(
            {
                "code": "G006",
                "message": "plan 涓己灏?pedagogy_method / teaching_method 瀛楁",
                "suggestion": (
                    f"鍦?plan 椤跺眰濉叆 pedagogy_method锛屽彇鍊?鈭?"
                    f"{sorted(cfg.valid_pedagogy_methods)}"
                ),
            }
        )
    elif method not in cfg.valid_pedagogy_methods:
        errors.append(
            {
                "code": "G006",
                "message": f"pedagogy_method 非法：'{method}' 不在白名单内",
                "suggestion": (
                    f"改为白名单内的教法之一: {sorted(cfg.valid_pedagogy_methods)}"
                ),
            }
        )

    # ---------------- G007: learning_objectives 鑷冲皯 1 涓紝姣忔潯浠悎娉?verb 寮澶?----------------
    objectives = _get_learning_objectives(plan)
    if not objectives:
        errors.append(
            {
                "code": "G007",
                "message": "plan 中缺少 learning_objectives（至少 1 条）",
                "suggestion": (
                    "在 plan['learning_objectives'] 中补目标，每条以合法动词开头，"
                    f"如 {sorted(cfg.valid_learning_objective_verbs)} 等"
                ),
            }
        )
    else:
        bad_objs: List[int] = []
        for i, obj in enumerate(objectives):
            if not _objective_starts_with_verb(obj, cfg.valid_learning_objective_verbs):
                bad_objs.append(i)
        if bad_objs:
            sample_lines: List[str] = []
            for i in bad_objs[:3]:
                txt = objectives[i]
                if len(txt) > 24:
                    txt = txt[:24] + "鈥?"
                sample_lines.append(f"#{i+1}:'{txt}'")
            errors.append(
                {
                    "code": "G007",
                    "message": (
                        f"瀛範鐩爣鏈互鍚堟硶鍔瘝寮澶达細{len(bad_objs)} 鏉紝"
                        f"鏍蜂緥 {'; '.join(sample_lines)}"
                    ),
                    "suggestion": (
                        f"灏嗘瘡鏉#洰鏍囪皟鏁翠负浠?{sorted(cfg.valid_learning_objective_verbs)} "
                        "涔嬩竴寮澶达紙鍙傝冨竷椴佸鍒嗙被娉曪級锛?"
                        "鍔瘝鍚庡彲璺熶腑鏂?鑻辨枃/鏁板瓧/鏍囩偣/绌烘牸"
                    ),
                }
            )

    passed = len(errors) == 0
    return passed, errors


# ---------------------------------------------------------------------------
# 閿欒鎶憡
# ---------------------------------------------------------------------------

def render_error_report(errors: List[dict]) -> str:
    """灏嗛敊璇垪琛覆鏌撲负浜虹被鍙鎶憡銆?"""
    if not errors:
        return "[lesson_plan_guard] 鍏儴 8 椤圭‖瑙勫垯閫氳繃 鉁?"

    lines: List[str] = []
    lines.append(f"[lesson_plan_guard] 鍙戠幇 {len(errors)} 椤硅鍒欒繚鍙嶏細")
    # 鎸?code 鎺掑簭
    sorted_errors = sorted(
        errors,
        key=lambda e: (str(e.get("code", "G???")),),
    )
    for i, err in enumerate(sorted_errors, start=1):
        code = err.get("code", "G???")
        msg = err.get("message", "")
        sug = err.get("suggestion", "")
        lines.append(f"  {i}. [{code}] {msg}")
        if sug:
            lines.append(f"     寤鸿: {sug}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 绠鏄?CostMonitor锛圕LI 榛樿锛?
# ---------------------------------------------------------------------------

class CostMonitor:
    """榛樿鎴愭湰鐩戞帶锛圕LI 鍏彛浣跨敤锛夈?"

    鎺彛锛?
        is_circuit_breaker_triggered() -> bool
        cumulative_cost_usd: float
        monthly_budget_usd: float
    """

    def __init__(
        self,
        monthly_budget_usd: float = 10.0,
        cumulative_cost_usd: float = 0.0,
    ) -> None:
        self.monthly_budget_usd = float(monthly_budget_usd)
        self.cumulative_cost_usd = float(cumulative_cost_usd)
        self.circuit_breaker_triggered: bool = (
            self.cumulative_cost_usd >= self.monthly_budget_usd
            if self.monthly_budget_usd > 0
            else False
        )

    def is_circuit_breaker_triggered(self) -> bool:
        return bool(self.circuit_breaker_triggered)


def get_default_monitor() -> CostMonitor:
    """鑾峰彇 CLI 浣跨敤鐨勯粯璁?CostMonitor銆?"""
    return CostMonitor(monthly_budget_usd=10.0, cumulative_cost_usd=0.0)


# ---------------------------------------------------------------------------
# CLI 鍏彛
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    log = get_logger("guard")
    import argparse

    p = argparse.ArgumentParser(
        prog="lesson_plan_guard",
        description="Validate lesson_plan.json against 8 hard rules (V7.3 规则层守卫).",
    )
    p.add_argument("--plan", required=True, help="Path to lesson_plan.json")
    p.add_argument(
        "--candidates",
        default=None,
        help="Optional path to candidates.json锛堝欓夌煡璇嗙偣/绱犳潗锛屽墠鍚戝吋瀹癸級",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="杈撳嚭 JSON 鎶憡锛堥粯璁汉绫诲彲璇伙級",
    )
    p.add_argument(
        "--monthly-budget-usd",
        type=float,
        default=10.0,
        help="内置 CostMonitor 的月预算（默认 10.0）",
    )
    p.add_argument(
        "--cumulative-cost-usd",
        type=float,
        default=0.0,
        help="内置 CostMonitor 的初始累计成本（默认 0.0）",
    )

    args = p.parse_args(argv)

    plan_path = Path(args.plan)
    if not plan_path.exists():
        log.error(f"ERROR: plan file not found: {plan_path}")
        return 2
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        log.error(f"ERROR: invalid plan JSON ({plan_path}): {e}")
        return 2

    candidates: Optional[dict] = None
    if args.candidates:
        cand_path = Path(args.candidates)
        if not cand_path.exists():
            log.error(f"ERROR: candidates file not found: {cand_path}")
            return 2
        try:
            candidates = json.loads(cand_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            log.error(f"ERROR: invalid candidates JSON ({cand_path}): {e}")
            return 2

    monitor = CostMonitor(
        monthly_budget_usd=args.monthly_budget_usd,
        cumulative_cost_usd=args.cumulative_cost_usd,
    )

    passed, errors = validate_lesson_plan(plan, candidates, monitor)

    if args.json:
        report = {
            "passed": bool(passed),
            "errors": errors,
            "error_count": len(errors),
            "report_id": f"lpg-{uuid.uuid4().hex[:12]}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "config": {
                "min_unique_knowledge_points": 3,
                "max_difficulty_jump": 2,
                "abstract_data_max_bytes": 10240,
                "min_assessment_questions": 3,
                "min_clip_duration_sec": 60.0,
                "max_clip_duration_sec": 600.0,
            },
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        log.info(render_error_report(errors))

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

