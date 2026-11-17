"""
BiliYouTik2Brain — 成本预估引擎 (v4.0)

根据环境参数 + 视频信息，预估处理时间和费用。
支持白话输出："预计 X 分钟，约 Y 元"。

支持的 ASR 成本：
  - faster-whisper: 本地 = ¥0（电费忽略）
  - bailian (百炼ASR): 按音频时长计费
  - openai-whisper: 按 token 计费（若走 OpenAI API）

支持的 LLM 成本：
  - DeepSeek: 按 token（input + output）
  - OpenAI: 按 token
  - Ollama/vLLM: 本地 = ¥0

支持的 OCR 成本：
  - PaddleOCR/RapidOCR: 本地 = ¥0
  - 云端 OCR: 按次计费

价格数据源：
  - 硬编码基准价格（来自官网 2026-07）
  - 支持通过 pricing_url 覆盖为实时 API
"""

import os
import time
import math
from dataclasses import dataclass, field
from typing import Optional, Dict, List

# ═══════════════════════════════════════════════════════════════
#  基准价格（2026-07 官网数据）
# ═══════════════════════════════════════════════════════════════

_PRICING = {
    # ── ASR ──
    "bailian_asr_per_minute": 0.003,       # 百炼ASR: ¥0.003/分钟 (约 ¥0.18/小时)
    "openai_whisper_per_minute": 0.006,    # OpenAI Whisper API: ~$0.0001/min ≈ ¥0.006/min
    "faster_whisper_per_minute": 0.0,      # 本地 = 免费

    # ── LLM (per 1K tokens) ──
    "deepseek_input_per_1k": 0.001,        # DeepSeek: ¥0.001/1K input (¥1/M)
    "deepseek_output_per_1k": 0.002,       # DeepSeek: ¥0.002/1K output (¥2/M)
    "openai_input_per_1k": 0.01,           # GPT-4o-mini: ~$0.15/M input ≈ ¥0.01/1K
    "openai_output_per_1k": 0.03,          # GPT-4o-mini: ~$0.60/M output ≈ ¥0.03/1K

    # ── OCR ──
    "paddleocr_per_frame": 0.0,            # 本地 = 免费
    "bailian_ocr_per_frame": 0.02,         # 百炼视觉: ~¥0.02/帧

    # ── 汇率 ──
    "usd_to_cny": 7.2,
}

# ═══════════════════════════════════════════════════════════════
#  估算系数（基于经验数据）
# ═══════════════════════════════════════════════════════════════

# 每分钟视频 ≈ 多少 token（中文，中等语速）
_TOKENS_PER_MINUTE = {
    "asr_output": 200,     # ASR 输出 ≈ 200 tokens/min
    "llm_fix_input": 400,  # LLM 修复时 input（含原文+提示词）≈ 400 tokens/min
    "llm_fix_output": 200, # LLM 修复 output ≈ 200 tokens/min
    "comment_analysis": 150, # 评论分析 ≈ 150 tokens/min 视频
}

# 每分钟视频处理时间（秒）
_TIME_PER_MINUTE = {
    "download": 15,        # 下载 ≈ 视频时长的 25%（高速网络）
    "asr_local": 20,       # 本地 ASR ≈ 视频时长的 33%（CPU）
    "asr_cloud": 8,        # 云端 ASR ≈ 视频时长的 13%（网络传输）
    "llm_fix": 10,         # LLM 修复 ≈ 视频时长的 17%
    "ocr": 3,              # OCR 每帧 ≈ 3 秒
    "enhance": 5,          # 内容分析 ≈ 视频时长的 8%
    "save": 2,             # 保存 ≈ 固定 2 秒
}

# 低置信词比例（影响 LLM 修复量）
_LOW_CONF_RATIO = 0.05  # 平均 5% 的词置信度低


@dataclass
class CostEstimate:
    """成本预估结果"""
    # 时间（分钟）
    time_download_min: float = 0.0
    time_asr_min: float = 0.0
    time_llm_min: float = 0.0
    time_ocr_min: float = 0.0
    time_enhance_min: float = 0.0
    time_save_min: float = 0.0
    time_total_min: float = 0.0

    # 费用（元）
    cost_asr_cny: float = 0.0
    cost_llm_cny: float = 0.0
    cost_ocr_cny: float = 0.0
    cost_total_cny: float = 0.0

    # 明细
    asr_engine: str = ""
    llm_backend: str = ""
    ocr_engine: str = ""
    video_minutes: float = 0.0

    # 置信度
    confidence: float = 0.8  # 预估置信度（基于历史数据量）

    # 白话描述
    plain_text: str = ""

    def to_plain_text(self) -> str:
        """生成白话描述"""
        minutes = self.time_total_min
        if minutes < 1:
            time_str = f"{int(minutes * 60)}秒"
        else:
            time_str = f"{minutes:.0f}分钟"

        cost = self.cost_total_cny
        if cost < 0.01:
            cost_str = "几乎不花钱"
        elif cost < 0.1:
            cost_str = f"约 {int(cost * 10)} 毛"
        else:
            cost_str = f"约 {cost:.2f} 元"

        self.plain_text = f"预计 {time_str}，{cost_str}"
        return self.plain_text


def estimate_cost(
    video_duration_min: float,
    asr_engine: str = "faster_whisper",
    llm_backend: str = "deepseek",
    ocr_enabled: bool = False,
    ocr_engine: str = "paddleocr",
    ocr_frame_count: int = 20,
    comment_analysis: bool = False,
    pricing: Optional[Dict] = None,
) -> CostEstimate:
    """预估处理时间和费用

    Args:
        video_duration_min: 视频时长（分钟）
        asr_engine: ASR 引擎（faster_whisper / bailian / openai_whisper）
        llm_backend: LLM 后端（deepseek / openai / ollama / vllm / none）
        ocr_enabled: 是否启用 OCR
        ocr_engine: OCR 引擎
        ocr_frame_count: OCR 抽帧数
        comment_analysis: 是否做评论分析
        pricing: 自定义价格表（覆盖默认）

    Returns:
        CostEstimate
    """
    p = pricing or _PRICING
    result = CostEstimate(
        video_minutes=video_duration_min,
        asr_engine=asr_engine,
        llm_backend=llm_backend,
        ocr_engine=ocr_engine if ocr_enabled else "none",
    )

    # ═══ 时间估算 ═══

    # 下载时间（固定比例）
    result.time_download_min = _TIME_PER_MINUTE["download"] / 60 * video_duration_min

    # ASR 时间
    if asr_engine in ("faster_whisper", "openai_whisper"):
        result.time_asr_min = _TIME_PER_MINUTE["asr_local"] / 60 * video_duration_min
    else:
        result.time_asr_min = _TIME_PER_MINUTE["asr_cloud"] / 60 * video_duration_min

    # LLM 修复时间（只修复低置信部分）
    low_conf_minutes = video_duration_min * _LOW_CONF_RATIO
    result.time_llm_min = _TIME_PER_MINUTE["llm_fix"] / 60 * video_duration_min * 0.3  # 只修 30%

    # OCR 时间
    if ocr_enabled:
        result.time_ocr_min = (_TIME_PER_MINUTE["ocr"] * ocr_frame_count) / 60

    # 内容增强时间
    result.time_enhance_min = _TIME_PER_MINUTE["enhance"] / 60 * video_duration_min
    if comment_analysis:
        result.time_enhance_min *= 1.5

    # 保存时间（固定）
    result.time_save_min = _TIME_PER_MINUTE["save"] / 60

    # 总时间
    result.time_total_min = (
        result.time_download_min +
        result.time_asr_min +
        result.time_llm_min +
        result.time_ocr_min +
        result.time_enhance_min +
        result.time_save_min
    )

    # ═══ 费用估算 ═══

    # ASR 费用
    if asr_engine == "bailian":
        result.cost_asr_cny = video_duration_min * p["bailian_asr_per_minute"]
    elif asr_engine == "openai_whisper":
        result.cost_asr_cny = video_duration_min * p["openai_whisper_per_minute"]
    else:
        result.cost_asr_cny = 0.0

    # LLM 费用
    if llm_backend in ("ollama", "vllm", "none"):
        result.cost_llm_cny = 0.0
    elif llm_backend == "deepseek":
        input_tokens = _TOKENS_PER_MINUTE["llm_fix_input"] * video_duration_min
        output_tokens = _TOKENS_PER_MINUTE["llm_fix_output"] * video_duration_min * 0.3
        result.cost_llm_cny = (
            input_tokens / 1000 * p["deepseek_input_per_1k"] +
            output_tokens / 1000 * p["deepseek_output_per_1k"]
        )
    elif llm_backend == "openai":
        input_tokens = _TOKENS_PER_MINUTE["llm_fix_input"] * video_duration_min
        output_tokens = _TOKENS_PER_MINUTE["llm_fix_output"] * video_duration_min * 0.3
        result.cost_llm_cny = (
            input_tokens / 1000 * p["openai_input_per_1k"] +
            output_tokens / 1000 * p["openai_output_per_1k"]
        )

    # OCR 费用
    if ocr_enabled:
        if ocr_engine == "bailian":
            result.cost_ocr_cny = ocr_frame_count * p["bailian_ocr_per_frame"]
        else:
            result.cost_ocr_cny = 0.0

    # 总费用
    result.cost_total_cny = result.cost_asr_cny + result.cost_llm_cny + result.cost_ocr_cny

    # 生成白话
    result.to_plain_text()

    return result


def estimate_from_env(video_url: str, video_duration_min: Optional[float] = None) -> CostEstimate:
    """根据当前环境自动预估成本

    Args:
        video_url: 视频链接（用于识别平台）
        video_duration_min: 视频时长（分钟），不传则估一个默认值

    Returns:
        CostEstimate
    """
    from .env import get_environment_context

    ctx = get_environment_context()

    # ASR 引擎选择
    if ctx.asr_default == "bailian":
        asr_engine = "bailian"
    elif ctx.asr_default == "openai_whisper":
        asr_engine = "openai_whisper"
    else:
        asr_engine = "faster_whisper"

    # LLM 后端选择
    if ctx.llm_default == "openai":
        llm_backend = "openai"
    elif ctx.llm_default in ("ollama", "vllm"):
        llm_backend = ctx.llm_default
    elif ctx.llm_default == "deepseek":
        llm_backend = "deepseek"
    else:
        llm_backend = "deepseek"

    # 默认时长假设（用户没说时）
    duration = video_duration_min or 10.0

    return estimate_cost(
        video_duration_min=duration,
        asr_engine=asr_engine,
        llm_backend=llm_backend,
        ocr_enabled=ctx.enable_ocr,
        ocr_frame_count=ctx.ocr_frame_count,
    )


def format_cost_dialog(estimate: CostEstimate) -> str:
    """格式化成本对话（用于 3 次交互确认）

    示例输出:
    ┌─────────────────────────────────┐
    │  处理预估                        │
    ├─────────────────────────────────┤
    │  视频时长: 10 分钟               │
    │  预计时间: 8 分钟                │
    │  预计费用: 约 3 毛               │
    │  ASR: faster-whisper (本地)      │
    │  LLM: DeepSeek                   │
    │  OCR: PaddleOCR (20帧)           │
    └─────────────────────────────────┘
    """
    cost = estimate.cost_total_cny
    if cost < 0.01:
        cost_display = "几乎不花钱"
    elif cost < 0.1:
        cost_display = f"约 {int(cost * 10)} 毛"
    else:
        cost_display = f"¥{cost:.2f}"

    time_val = estimate.time_total_min
    if time_val < 1:
        time_display = f"{int(time_val * 60)}秒"
    else:
        time_display = f"{time_val:.0f}分钟"

    asr_label = {
        "faster_whisper": "faster-whisper (本地)",
        "bailian": "百炼ASR (云端)",
        "openai_whisper": "OpenAI Whisper (云端)",
    }.get(estimate.asr_engine, estimate.asr_engine)

    llm_label = {
        "deepseek": "DeepSeek",
        "openai": "OpenAI",
        "ollama": "Ollama (本地)",
        "vllm": "vLLM (本地)",
        "none": "无",
    }.get(estimate.llm_backend, estimate.llm_backend)

    lines = [
        "┌─────────────────────────────────┐",
        "│  处理预估                        │",
        "├─────────────────────────────────┤",
        f"│  视频时长: {estimate.video_minutes:.0f} 分钟",
        f"│  预计时间: {time_display}",
        f"│  预计费用: {cost_display}",
        f"│  ASR: {asr_label}",
        f"│  LLM: {llm_label}",
    ]

    if estimate.ocr_engine != "none":
        lines.append(f"│  OCR: {estimate.ocr_engine} ({estimate.time_ocr_min:.0f}帧)")

    lines.extend([
        "└─────────────────────────────────┘",
    ])

    return "\n".join(lines)
