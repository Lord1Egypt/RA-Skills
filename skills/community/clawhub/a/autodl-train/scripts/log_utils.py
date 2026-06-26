#!/usr/bin/env python3
"""Heuristic log parsing for training metrics and failures."""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Optional, Tuple

RUN_START_MARKER = "=== AutoDL train operator start ==="

METRIC_PATTERNS: Dict[str, List[re.Pattern[str]]] = {
    "epoch": [re.compile(r"\bepoch\s*[:=/\[]\s*(\d+(?:\.\d+)?)", re.IGNORECASE)],
    "step": [re.compile(r"\b(?:global_)?step\s*[:=/\[]\s*(\d+(?:\.\d+)?)", re.IGNORECASE)],
    "loss": [re.compile(r"\bloss\s*[:=]\s*(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)", re.IGNORECASE)],
    "lr": [re.compile(r"\blr\s*[:=]\s*(\d+(?:\.\d+)?(?:e[+-]?\d+)?)", re.IGNORECASE)],
    "grad_norm": [re.compile(r"\bgrad(?:ient)?_?norm\s*[:=]\s*(\d+(?:\.\d+)?(?:e[+-]?\d+)?)", re.IGNORECASE)],
    "val_loss": [re.compile(r"\bval(?:idation)?[_\s-]*loss\s*[:=]\s*(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)", re.IGNORECASE)],
    "accuracy": [re.compile(r"\b(?:acc|accuracy)\s*[:=]\s*(\d+(?:\.\d+)?%?)", re.IGNORECASE)],
    "mAP": [re.compile(r"\bmap(?:@\d+)?\s*[:=]\s*(\d+(?:\.\d+)?%?)", re.IGNORECASE)],
    "F1": [re.compile(r"\bf1\s*[:=]\s*(\d+(?:\.\d+)?%?)", re.IGNORECASE)],
}

FAILURE_PATTERNS: List[Tuple[str, re.Pattern[str], str, str, bool]] = [
    (
        "cuda_oom",
        re.compile(r"cuda out of memory|outofmemoryerror|cublas_status_alloc_failed", re.IGNORECASE),
        "GPU 显存不足或显存碎片过多。",
        "减小 batch size、启用梯度累积或混合精度，必要时缩短序列长度/分辨率后再恢复训练。",
        True,
    ),
    (
        "nccl_error",
        re.compile(r"nccl.*error|unhandled system error|socket timeout", re.IGNORECASE),
        "分布式通信异常，可能来自网络抖动、端口占用或进程不同步退出。",
        "检查多卡启动参数、主从地址端口和残留进程；若 checkpoint 完整，通常适合恢复训练。",
        True,
    ),
    (
        "runtime_error",
        re.compile(r"runtimeerror", re.IGNORECASE),
        "运行时异常，可能来自张量形状、设备放置、数据格式或自定义代码。",
        "先定位首个 RuntimeError 栈，再决定是否修复代码后从最近 checkpoint 恢复。",
        True,
    ),
    (
        "nan",
        re.compile(r"\bnan\b|loss\s*[:=]\s*nan|grad(?:ient)?_?norm\s*[:=]\s*nan", re.IGNORECASE),
        "数值不稳定，通常与学习率过高、混合精度、数据异常或梯度爆炸有关。",
        "降低学习率、启用梯度裁剪、检查数据与标签，再从较早的稳定 checkpoint 恢复。",
        True,
    ),
    (
        "disk_full",
        re.compile(r"no space left on device|disk full", re.IGNORECASE),
        "磁盘空间不足，通常发生在 checkpoint 或日志持续增长时。",
        "手动清理旧产物或更换输出目录；确认空间恢复后再从最近 checkpoint 恢复。",
        True,
    ),
    (
        "killed",
        re.compile(r"\bkilled\b|oom-kill|oom killer", re.IGNORECASE),
        "进程被系统杀死，常见原因是 CPU 内存不足或平台策略终止。",
        "检查内存峰值、数据加载缓存和系统日志；若 checkpoint 存在，通常可恢复训练。",
        True,
    ),
    (
        "segfault",
        re.compile(r"segmentation fault|core dumped", re.IGNORECASE),
        "底层库、驱动或扩展模块发生崩溃。",
        "优先检查 CUDA、PyTorch、驱动和自定义扩展兼容性；修复后再尝试恢复训练。",
        False,
    ),
    (
        "connection_reset",
        re.compile(r"connection reset|broken pipe", re.IGNORECASE),
        "远程连接或分布式通信链路中断。",
        "确认 SSH/网络稳定性与分布式端口配置；若训练状态未损坏，可从最近 checkpoint 恢复。",
        True,
    ),
    (
        "timeout",
        re.compile(r"\btimeout\b|timed out", re.IGNORECASE),
        "任务或通信发生超时，可能与数据读取、评估阶段或多卡同步有关。",
        "检查数据源、I/O 和分布式超时参数；若模型状态完好，通常可以恢复训练。",
        True,
    ),
]

STOP_PATTERNS = [
    re.compile(r"training complete|finished training|done training", re.IGNORECASE),
    re.compile(r"saving checkpoint", re.IGNORECASE),
    re.compile(r"validation", re.IGNORECASE),
]


def isolate_latest_run(log_text: str) -> str:
    marker_index = log_text.rfind(RUN_START_MARKER)
    if marker_index == -1:
        return log_text
    return log_text[marker_index:]


def safe_float(raw: str) -> Optional[float]:
    value = raw.strip().rstrip(",")
    if value.endswith("%"):
        value = value[:-1]
    try:
        number = float(value)
    except ValueError:
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def extract_metrics(log_text: str) -> Dict[str, Any]:
    latest: Dict[str, float] = {}
    series: Dict[str, List[float]] = {key: [] for key in METRIC_PATTERNS}
    matched_lines: List[str] = []

    for line in log_text.splitlines():
        line_hit = False
        for metric_name, patterns in METRIC_PATTERNS.items():
            for pattern in patterns:
                match = pattern.search(line)
                if not match:
                    continue
                value = safe_float(match.group(1))
                if value is None:
                    continue
                latest[metric_name] = value
                series[metric_name].append(value)
                line_hit = True
                break
        if line_hit:
            matched_lines.append(line)

    compact_series = {key: values[-8:] for key, values in series.items() if values}
    trends = {}
    for key, values in compact_series.items():
        if len(values) >= 2:
            delta = values[-1] - values[0]
            if key in {"loss", "val_loss"}:
                if delta < -1e-8:
                    trends[key] = "down"
                elif delta > 1e-8:
                    trends[key] = "up"
                else:
                    trends[key] = "flat"
            else:
                if delta > 1e-8:
                    trends[key] = "up"
                elif delta < -1e-8:
                    trends[key] = "down"
                else:
                    trends[key] = "flat"
        else:
            trends[key] = "single-point"

    return {
        "latest": latest,
        "series": compact_series,
        "trends": trends,
        "matched_lines": matched_lines[-20:],
    }


def detect_failures(log_text: str) -> List[Dict[str, Any]]:
    failures: List[Dict[str, Any]] = []
    lines = log_text.splitlines()
    for failure_type, pattern, reason, suggestion, resumable in FAILURE_PATTERNS:
        for index, line in enumerate(lines):
            if not pattern.search(line):
                continue
            start = max(0, index - 2)
            end = min(len(lines), index + 3)
            failures.append(
                {
                    "type": failure_type,
                    "line": line.strip(),
                    "context": lines[start:end],
                    "possible_cause": reason,
                    "suggestion": suggestion,
                    "resume_recommended": resumable,
                }
            )
            break
    return failures


def infer_phase(log_text: str, metrics: Dict[str, Any]) -> str:
    lower = log_text.lower()
    if "validation" in lower or "evaluating" in lower:
        return "validation or evaluation"
    if "saving checkpoint" in lower or "checkpoint saved" in lower:
        return "checkpointing"
    if any(pattern.search(log_text) for pattern in STOP_PATTERNS):
        return "finishing or post-training"
    latest = metrics.get("latest", {})
    if "epoch" in latest or "step" in latest:
        return "active training"
    return "unknown"


def assess_convergence(metrics: Dict[str, Any], failures: List[Dict[str, Any]]) -> str:
    if failures:
        return "训练出现异常，当前不能认为正常收敛。"
    trends = metrics.get("trends", {})
    latest = metrics.get("latest", {})
    if "loss" in trends and trends["loss"] == "down":
        if "val_loss" in trends and trends["val_loss"] == "up":
            return "训练损失下降但验证损失上升，可能开始过拟合。"
        return "主要损失指标在下降，整体看起来在正常收敛。"
    if "loss" in trends and trends["loss"] == "up":
        return "最近 loss 有上升趋势，建议检查学习率、数据质量或梯度稳定性。"
    if any(key in latest for key in ("accuracy", "mAP", "F1")):
        return "日志中出现评估指标，但趋势信息有限，需结合更多轮次判断。"
    return "日志中可用指标较少，当前只能做启发式判断。"


def build_next_steps(metrics: Dict[str, Any], failures: List[Dict[str, Any]]) -> List[str]:
    latest = metrics.get("latest", {})
    trends = metrics.get("trends", {})
    steps: List[str] = []

    if failures:
        first = failures[0]
        steps.append(first["suggestion"])
        if first.get("resume_recommended"):
            steps.append("优先确认最近 checkpoint 是否完整可用，再决定是否恢复训练。")
        else:
            steps.append("先修复底层环境或代码问题，再考虑重新启动训练。")
        return steps

    if trends.get("loss") == "down" and trends.get("val_loss") in {"down", "flat", None}:
        steps.append("当前训练值得继续，建议保持监控并关注后续验证集表现。")
    if trends.get("val_loss") == "up":
        steps.append("验证损失在上升，建议考虑早停、正则化或降低学习率。")
    if latest.get("grad_norm", 0.0) and latest["grad_norm"] > 10:
        steps.append("梯度范数偏高，建议启用或加强梯度裁剪。")
    if latest.get("lr", 0.0) and latest["lr"] > 1e-3 and trends.get("loss") == "up":
        steps.append("学习率可能偏大，建议尝试更小的学习率或更平滑的调度器。")
    if not steps:
        steps.append("继续收集更多日志片段，再判断是否需要调参或恢复训练。")
    return steps


def summarize_metrics(metrics: Dict[str, Any]) -> str:
    latest = metrics.get("latest", {})
    if not latest:
        return "未能从最近日志中稳定提取结构化指标，以下总结基于启发式判断。"
    parts = []
    for key in ["epoch", "step", "loss", "val_loss", "accuracy", "mAP", "F1", "lr", "grad_norm"]:
        if key in latest:
            parts.append(f"{key}={latest[key]:g}")
    return "最近提取到的关键指标：" + ", ".join(parts)


def summarize_log(log_text: str) -> Dict[str, Any]:
    metrics = extract_metrics(log_text)
    failures = detect_failures(log_text)
    phase = infer_phase(log_text, metrics)
    convergence = assess_convergence(metrics, failures)
    next_steps = build_next_steps(metrics, failures)
    anomaly = failures[0]["type"] if failures else None

    summary_lines = [
        f"当前阶段：{phase}",
        summarize_metrics(metrics),
        f"收敛判断：{convergence}",
    ]
    if anomaly:
        summary_lines.append(f"异常情况：检测到 {anomaly}。")
    else:
        summary_lines.append("异常情况：最近日志中未发现典型致命错误关键词。")
    summary_lines.append(f"是否值得继续：{'否，先处理异常。' if failures else '是，若资源正常可继续观察。'}")
    summary_lines.append("下一步建议：" + "；".join(next_steps))

    return {
        "phase": phase,
        "metrics": metrics,
        "failures": failures,
        "convergence": convergence,
        "next_steps": next_steps,
        "human_summary": "\n".join(summary_lines),
    }
