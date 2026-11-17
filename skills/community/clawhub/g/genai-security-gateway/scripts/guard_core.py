from __future__ import annotations

import json
import multiprocessing as mp
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np


DEFAULT_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_THRESHOLD = 0.78
DEFAULT_MAX_INPUT_CHARS = 20000
DEFAULT_SEMANTIC_TIMEOUT_SECONDS = 30.0
DEFAULT_TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "references" / "jailbreak_templates.json"

SECRET_PATTERNS = [
    r"sk-[a-zA-Z0-9]{48}",
    r"sk-proj-[a-zA-Z0-9_-]{20,}",
    r"sk-ant-[a-zA-Z0-9_-]{20,}",
    r"AIzaSy[a-zA-Z0-9_-]{33}",
    r"AKIA[0-9A-Z]{16}",
    r"ghp_[a-zA-Z0-9]{36}",
    r"github_pat_[a-zA-Z0-9_]{20,}",
]


def _threshold() -> float:
    raw_threshold = os.getenv("GENAI_SECURITY_THRESHOLD")
    if raw_threshold is None:
        return DEFAULT_THRESHOLD
    try:
        threshold = float(raw_threshold)
    except ValueError:
        return DEFAULT_THRESHOLD
    if not 0.0 < threshold <= 1.0:
        return DEFAULT_THRESHOLD
    return threshold


def _max_input_chars() -> int:
    raw_limit = os.getenv("GENAI_SECURITY_MAX_INPUT_CHARS")
    if raw_limit is None:
        return DEFAULT_MAX_INPUT_CHARS
    try:
        limit = int(raw_limit)
    except ValueError:
        return DEFAULT_MAX_INPUT_CHARS
    return max(1000, limit)


def _semantic_timeout_seconds() -> float:
    raw_timeout = os.getenv("GENAI_SECURITY_SEMANTIC_TIMEOUT_SECONDS")
    if raw_timeout is None:
        return DEFAULT_SEMANTIC_TIMEOUT_SECONDS
    try:
        timeout = float(raw_timeout)
    except ValueError:
        return DEFAULT_SEMANTIC_TIMEOUT_SECONDS
    return max(1.0, timeout)


def _template_path() -> Path:
    return Path(os.getenv("GENAI_SECURITY_TEMPLATES", str(DEFAULT_TEMPLATE_PATH))).expanduser()


@lru_cache(maxsize=1)
def load_jailbreak_templates() -> list[str]:
    with _template_path().open("r", encoding="utf-8") as f:
        templates = json.load(f)
    if not isinstance(templates, list) or not all(isinstance(item, str) for item in templates):
        raise ValueError("Jailbreak templates must be a JSON list of strings.")
    if not templates:
        raise ValueError("Jailbreak templates must not be empty.")
    return templates


@lru_cache(maxsize=1)
def _load_sentence_transformers() -> tuple[Any, Any]:
    local_only = os.getenv("GENAI_SECURITY_LOCAL_ONLY", "").lower() in {"1", "true", "yes"}
    if local_only:
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

    from sentence_transformers import SentenceTransformer, util

    model_name = os.getenv("GENAI_SECURITY_MODEL", DEFAULT_MODEL_NAME)
    model = SentenceTransformer(model_name, local_files_only=local_only)
    return model, util


@lru_cache(maxsize=1)
def _jailbreak_embeddings() -> Any:
    model, _ = _load_sentence_transformers()
    return model.encode(load_jailbreak_templates(), convert_to_tensor=True)


def _semantic_score(user_input: str) -> tuple[float, str]:
    model, util = _load_sentence_transformers()
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    cosine_scores = util.cos_sim(user_embedding, _jailbreak_embeddings())[0]
    scores = cosine_scores.cpu().numpy()

    max_score = float(np.max(scores))
    max_index = int(np.argmax(scores))
    return max_score, load_jailbreak_templates()[max_index]


def _semantic_worker(user_input: str, queue: mp.Queue) -> None:
    try:
        score, template = _semantic_score(user_input)
        queue.put({"ok": True, "score": score, "template": template})
    except Exception as exc:
        queue.put({"ok": False, "error": str(exc)})


def _semantic_score_with_timeout(user_input: str) -> tuple[float, str]:
    timeout = _semantic_timeout_seconds()
    context = mp.get_context("spawn")
    queue = context.Queue(maxsize=1)
    process = context.Process(target=_semantic_worker, args=(user_input, queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join(2)
        raise TimeoutError(f"Semantic detector exceeded cold-start timeout ({timeout:.1f}s).")

    if queue.empty():
        raise RuntimeError("Semantic detector exited without returning a result.")

    payload = queue.get()
    if not payload.get("ok"):
        raise RuntimeError(payload.get("error", "Semantic detector failed."))
    return float(payload["score"]), str(payload["template"])


def _result(
    *,
    is_safe: bool,
    risk_level: str,
    reason: str,
    detector: str,
    semantic_score: float | None = None,
    matched_template: str | None = None,
) -> dict[str, Any]:
    return {
        "is_safe": is_safe,
        "risk_level": risk_level,
        "reason": reason,
        "suggested_action": "PASS" if is_safe else "BLOCK",
        "detector": detector,
        "semantic_score": None if semantic_score is None else round(semantic_score, 4),
        "semantic_threshold": _threshold(),
        "semantic_timeout_seconds": _semantic_timeout_seconds(),
        "matched_template": matched_template,
    }


def check_security_v2(user_input: str, *, enable_semantic: bool = True) -> dict[str, Any]:
    if not isinstance(user_input, str):
        return _result(
            is_safe=False,
            risk_level="INVALID",
            reason="输入无效：message 必须是字符串。",
            detector="input_validation",
        )

    if not user_input.strip():
        return _result(
            is_safe=True,
            risk_level="NONE",
            reason="安全通过：输入为空或仅包含空白字符。",
            detector="input_validation",
        )

    if len(user_input) > _max_input_chars():
        return _result(
            is_safe=False,
            risk_level="HIGH (高危/输入过长)",
            reason=f"输入长度超过安全审计上限（{_max_input_chars()} 字符），已阻断以避免资源滥用。",
            detector="input_limits",
        )

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, user_input, flags=re.IGNORECASE):
            return _result(
                is_safe=False,
                risk_level="CRITICAL (严重)",
                reason="检测到敏感 API 密钥泄露风险！",
                detector="regex_secret",
            )

    lowered = user_input.lower()
    if "忘记" in user_input and "提示词" in user_input:
        return _result(
            is_safe=False,
            risk_level="HIGH (高危)",
            reason="检测到试图规避限制的行为（命中关键词组合：[忘记 + 提示词]）",
            detector="static_combo",
        )

    static_english_patterns = [
        ("ignore", "previous", "instructions"),
        ("disregard", "prior", "instructions"),
        ("forget", "previous", "instructions"),
        ("developer", "mode"),
        ("reveal", "system", "prompt"),
        ("extract", "system", "prompt"),
        ("show", "system", "prompt"),
        ("hidden", "system", "prompt"),
        ("unrestricted", "ai"),
        ("no", "ethical", "constraints"),
        ("do anything now",),
    ]
    for phrase_parts in static_english_patterns:
        if all(part in lowered for part in phrase_parts):
            return _result(
                is_safe=False,
                risk_level="HIGH (高危)",
                reason=f"检测到英文越狱静态组合：{', '.join(phrase_parts)}",
                detector="static_combo",
            )

    if not enable_semantic:
        return _result(
            is_safe=True,
            risk_level="NONE",
            reason="安全通过：静态层未检测到明显安全缺陷；语义层已跳过。",
            detector="static_only",
        )

    try:
        max_score, matched_template = _semantic_score_with_timeout(user_input)
    except TimeoutError as exc:
        return _result(
            is_safe=False,
            risk_level="HIGH (高危/语义层超时)",
            reason=f"{exc} 已保守阻断，避免冷启动或模型下载导致网关长时间挂起。",
            detector="semantic_timeout",
        )
    except Exception as exc:
        return _result(
            is_safe=False,
            risk_level="HIGH (高危/语义层异常)",
            reason=f"语义检测执行失败：{exc} 已保守阻断。",
            detector="semantic_error",
        )

    if max_score >= _threshold():
        return _result(
            is_safe=False,
            risk_level="HIGH (高危/动态语义)",
            reason=f"动态拦截：检测到高风险绕过意图。与已知越狱变体相似度过高 ({max_score:.2f})。",
            detector="semantic_vector",
            semantic_score=max_score,
            matched_template=matched_template,
        )

    return _result(
        is_safe=True,
        risk_level="NONE",
        reason="安全通过：未检测到明显安全缺陷。",
        detector="semantic_vector",
        semantic_score=max_score,
        matched_template=matched_template,
    )


def optimize_prompt_v1(raw_input: str) -> dict[str, Any]:
    """
    Reserved module: prompt dehydration and structured translation.
    Future goal: map vague natural-language multimedia requests into deterministic API parameters.
    """
    return {
        "optimized": False,
        "implemented": False,
        "status": "stub",
        "transferred_prompt": raw_input,
        "token_saved_estimate": 0,
        "reason": "Optimization module is reserved for a future release.",
    }
