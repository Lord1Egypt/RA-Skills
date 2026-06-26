#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
common.py — Common utility functions
通用工具函数
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


SAFE_ION_STRATEGIES = {"regex", "exact", "base_state", "base_num_best_state"}


@dataclass
class IonMatchResult:
    """
    电离室透过率匹配结果。
    Ionchamber transmission matching result.
    """

    sample_path: str
    sample_name: str
    ion_path: Optional[str]
    strategy: str
    score: float
    state_similarity: float
    transmission_percent: Optional[float]
    sample_intensity: Optional[float]
    background_intensity: Optional[float]
    success: bool
    error_message: Optional[str] = None


def format_size(n_bytes: int) -> str:
    """
    Format byte size to human readable string.
    格式化字节大小为人类可读字符串。

    Parameters
    ----------
    n_bytes : int
        Number of bytes / 字节数

    Returns
    -------
    str
        Formatted string like '1.5 MB' / 格式化字符串
    """
    size = float(n_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(size) < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def format_array_info(arr: np.ndarray) -> str:
    """
    Format numpy array info as a readable string.
    格式化 numpy 数组信息为可读字符串。

    Parameters
    ----------
    arr : np.ndarray
        Input array / 输入数组

    Returns
    -------
    str
        Formatted string with shape, dtype, etc. / 包含形状、数据类型等的格式化字符串
    """
    if arr is None:
        return "None"

    info = f"shape={arr.shape}, dtype={arr.dtype.name}"
    if arr.ndim > 0:
        finite = arr[np.isfinite(arr)]
        if len(finite) > 0:
            info += f", min={finite.min():.3g}, max={finite.max():.3g}"
    return info


def find_common_shape(shapes: List[Tuple[int, ...]]) -> Optional[Tuple[Optional[int], ...]]:
    """
    Find the common shape among multiple shapes (broadcasting compatible).
    找出多个形状的公共形状（广播兼容）。

    Parameters
    ----------
    shapes : List[Tuple[int, ...]]
        List of shapes / 形状列表

    Returns
    -------
    Tuple[int, ...] or None
        Common shape or None if incompatible / 公共形状或不兼容时返回 None
    """
    if not shapes:
        return None

    max_ndim = max(len(s) for s in shapes)
    aligned = []
    for s in shapes:
        diff = max_ndim - len(s)
        aligned.append((1,) * diff + s)

    result = []
    for dims in zip(*aligned):
        non_one = [d for d in dims if d != 1]
        if not non_one:
            result.append(1)
        elif len(set(non_one)) == 1:
            result.append(non_one[0])
        else:
            return None
    return tuple(result)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value between min and max.
    将值限制在最小和最大之间。

    Parameters
    ----------
    value : float
        Input value / 输入值
    min_val : float
        Minimum value / 最小值
    max_val : float
        Maximum value / 最大值

    Returns
    -------
    float
        Clamped value / 限制后的值
    """
    return max(min_val, min(max_val, value))


def load_ionchamber_table(path: str) -> Optional[pd.DataFrame]:
    """
    加载 SSRF 电离室文本文件。
    Load an SSRF ionchamber text file.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            content = handle.read()
        lines = [line for line in content.strip().splitlines() if line and not line.startswith("#")]
        rows = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                rows.append([" ".join(parts[:2])] + [float(value) for value in parts[2:5]])
        if not rows:
            return None
        return pd.DataFrame.from_records(
            rows,
            columns=pd.Index(["Time", "Ionchamber0", "Ionchamber1", "Ionchamber2"]),
        )
    except Exception:
        return None


def calc_ion_intensity(df: pd.DataFrame, channel: str, method: str) -> Optional[float]:
    """
    计算电离室强度统计值。
    Calculate a summary intensity from one ionchamber channel.
    """
    try:
        values = df[channel].to_numpy(dtype=float)
        if method == "median":
            return float(np.median(values))
        if method == "trimmed_mean":
            sorted_values = np.sort(values)
            if len(sorted_values) > 2:
                return float(np.mean(sorted_values[1:-1]))
            return float(np.mean(sorted_values))
        return float(np.mean(values))
    except Exception:
        return None


def _split_name(stem: str) -> Tuple[str, Optional[str], Optional[int]]:
    """
    解析文件名，提取主名字、状态段与末尾编号。
    Split a stem into base token, state token, and trailing number.
    """
    normalized = stem.replace("_", "-")
    parts = [part for part in normalized.split("-") if part]
    if not parts:
        return stem.lower(), None, None

    base = parts[0].lower()
    if len(parts) >= 2 and re.fullmatch(r"\d+", parts[-1]):
        number = int(parts[-1])
        middle = parts[1:-1]
    else:
        number = None
        middle = parts[1:]
    state = "-".join(part.lower() for part in middle) if middle else None
    return base, state, number


def _state_similarity(left: Optional[str], right: Optional[str]) -> float:
    """
    计算状态片段相似度。
    Calculate similarity between state fragments.
    """
    if left is None and right is None:
        return 1.0
    if left is None or right is None:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def match_ionchamber_detail(
    data_name: str,
    ion_paths: List[str],
    user_regex: Optional[str] = None,
) -> Tuple[Optional[str], str, float, float]:
    """
    使用与 2D GUI 相近的规则匹配电离室文件。
    Match an ionchamber file with rules aligned to the 2D GUI.
    """
    data_stem = re.sub(r"\.[^.]+$", "", data_name)
    data_base, data_state, data_number = _split_name(data_stem)

    ion_info: List[Tuple[str, str, Optional[str], Optional[int]]] = []
    for path in ion_paths:
        ion_stem = re.sub(r"\.[^.]+$", "", path.split("\\")[-1].split("/")[-1])
        ion_info.append((path, *_split_name(ion_stem)))

    if user_regex:
        try:
            pattern = re.compile(user_regex)
            for path, ion_base, ion_state, ion_number in ion_info:
                if pattern.search(ion_base):
                    return path, "regex", 1.0, _state_similarity(data_state, ion_state)
        except re.error:
            pass

    for path, ion_base, ion_state, ion_number in ion_info:
        if ion_base == data_base and ion_state == data_state and ion_number == data_number:
            return path, "exact", 1.0, _state_similarity(data_state, ion_state)

    same_base_state = [
        (path, ion_state, ion_number)
        for path, ion_base, ion_state, ion_number in ion_info
        if ion_base == data_base and ion_state == data_state
    ]
    if data_state is not None and same_base_state:
        chosen = min(
            same_base_state,
            key=lambda item: item[2] if item[2] is not None else float("inf"),
        )
        score = 1.0 if len(same_base_state) == 1 else 0.95
        return chosen[0], "base_state", score, _state_similarity(data_state, chosen[1])

    if data_number is not None:
        same_base_number = [
            (path, ion_state, ion_number)
            for path, ion_base, ion_state, ion_number in ion_info
            if ion_base == data_base and ion_number == data_number
        ]
        if same_base_number:
            chosen = max(same_base_number, key=lambda item: _state_similarity(data_state, item[1]))
            similarity = _state_similarity(data_state, chosen[1])
            return chosen[0], "base_num_best_state", 0.80 + similarity * 0.2, similarity

    same_base = [
        (path, ion_state)
        for path, ion_base, ion_state, ion_number in ion_info
        if ion_base == data_base
    ]
    if same_base:
        chosen = max(same_base, key=lambda item: _state_similarity(data_state, item[1]))
        similarity = _state_similarity(data_state, chosen[1])
        return chosen[0], "base_only_best_state", 0.65 + similarity * 0.1, similarity

    best_path: Optional[str] = None
    best_score = 0.0
    best_similarity = 0.0
    for path, ion_base, ion_state, ion_number in ion_info:
        score = SequenceMatcher(None, data_base, ion_base).ratio()
        if ion_state is not None and data_state is not None and ion_state == data_state:
            score += 0.25
        if ion_number is not None and data_number is not None and ion_number == data_number:
            score += 0.25
        if ion_base.startswith(data_base) or data_base.startswith(ion_base):
            score += 0.10
        if score > best_score:
            best_path = path
            best_score = score
            best_similarity = _state_similarity(data_state, ion_state)

    if best_path is not None and best_score >= 0.4:
        return best_path, "fuzzy", best_score, best_similarity
    return None, "none", 0.0, 0.0


def build_transmission_map(
    sample_paths: List[str],
    background_path: str,
    ion_paths: List[str],
    background_channel: str = "Ionchamber1",
    background_method: str = "median",
    sample_channel: str = "Ionchamber1",
    sample_method: str = "median",
    user_regex: Optional[str] = None,
    min_score: float = 0.60,
) -> Tuple[Dict[str, float], List[IonMatchResult], Optional[IonMatchResult]]:
    """
    根据样品/背景曲线与电离室文件计算逐文件透过率。
    Build per-file transmission values from sample/background curves and ionchamber files.
    """
    background_name = background_path.split("\\")[-1].split("/")[-1]
    bg_ion_path, bg_strategy, bg_score, bg_state_similarity = match_ionchamber_detail(
        background_name,
        ion_paths,
        user_regex=user_regex,
    )
    bg_table = load_ionchamber_table(bg_ion_path) if bg_ion_path else None
    background_intensity = (
        calc_ion_intensity(bg_table, background_channel, background_method)
        if bg_table is not None
        else None
    )
    background_result = IonMatchResult(
        sample_path=background_path,
        sample_name=background_name,
        ion_path=bg_ion_path,
        strategy=bg_strategy,
        score=bg_score,
        state_similarity=bg_state_similarity,
        transmission_percent=None,
        sample_intensity=background_intensity,
        background_intensity=None,
        success=bg_ion_path is not None
        and background_intensity is not None
        and background_intensity != 0
        and bg_strategy in SAFE_ION_STRATEGIES
        and bg_score >= min_score,
        error_message=(
            None
            if bg_ion_path is not None
            and background_intensity is not None
            and background_intensity != 0
            and bg_strategy in SAFE_ION_STRATEGIES
            and bg_score >= min_score
            else (
                "无匹配背景电离室文件"
                if not bg_ion_path
                else (
                    "背景电离室匹配策略过宽"
                    if bg_strategy not in SAFE_ION_STRATEGIES
                    else (
                        "背景电离室匹配分数过低" if bg_score < min_score else "背景电离室强度无效"
                    )
                )
            )
        ),
    )

    transmissions: Dict[str, float] = {}
    match_results: List[IonMatchResult] = []
    if not background_result.success:
        return transmissions, match_results, background_result

    assert background_intensity is not None
    for sample_path in sample_paths:
        sample_name = sample_path.split("\\")[-1].split("/")[-1]
        ion_path, strategy, score, state_similarity = match_ionchamber_detail(
            sample_name,
            ion_paths,
            user_regex=user_regex,
        )
        sample_table = load_ionchamber_table(ion_path) if ion_path else None
        sample_intensity = (
            calc_ion_intensity(sample_table, sample_channel, sample_method)
            if sample_table is not None
            else None
        )
        transmission_percent = None
        success = False
        error_message = None
        if ion_path is None:
            error_message = "无匹配电离室文件"
        elif strategy not in SAFE_ION_STRATEGIES:
            error_message = f"电离室匹配策略过宽 ({strategy})"
        elif score < min_score:
            error_message = f"电离室匹配分数过低 ({score:.3f} < {min_score:.2f})"
        elif sample_intensity is None:
            error_message = "样品电离室强度无效"
        elif background_intensity == 0:
            error_message = "背景电离室强度为 0"
        else:
            transmission_percent = sample_intensity / background_intensity * 100.0
            transmissions[sample_path] = transmission_percent
            success = True

        match_results.append(
            IonMatchResult(
                sample_path=sample_path,
                sample_name=sample_name,
                ion_path=ion_path,
                strategy=strategy,
                score=score,
                state_similarity=state_similarity,
                transmission_percent=transmission_percent,
                sample_intensity=sample_intensity,
                background_intensity=background_intensity,
                success=success,
                error_message=error_message,
            )
        )

    return transmissions, match_results, background_result
