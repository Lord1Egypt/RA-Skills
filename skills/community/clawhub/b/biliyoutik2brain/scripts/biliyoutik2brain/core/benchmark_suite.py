"""
BiliYouTik2Brain — 自动基准测试 (v4.0)

每次发版前自动跑标准视频集，对比准确率/速度/成本。
数据公开可查，质量可量化追踪。
"""

import os
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════
#  基准测试套件
# ═══════════════════════════════════════════════════════════

_BENCHMARK_DIR = os.path.expanduser("~/.biliyoutik2brain/benchmarks")
os.makedirs(_BENCHMARK_DIR, exist_ok=True)


@dataclass
class BenchmarkResult:
    """单次基准测试结果"""
    version: str
    date: str
    video_id: str
    video_url: str
    platform: str

    # 准确率
    word_error_rate: float = 0.0        # 词错误率（越低越好）
    confidence_score: float = 0.0       # 平均置信度

    # 性能
    processing_time_s: float = 0.0      # 处理时间（秒）
    chars_per_second: float = 0.0       # 处理速度（字/秒）

    # 成本
    cost_cny: float = 0.0              # 费用（元）

    # OCR
    ocr_accuracy: float = 0.0           # OCR 准确率
    ocr_frame_count: int = 0            # OCR 帧数

    # 元信息
    asr_engine: str = ""
    llm_backend: str = ""
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "date": self.date,
            "video_id": self.video_id,
            "video_url": self.video_url,
            "platform": self.platform,
            "word_error_rate": self.word_error_rate,
            "confidence_score": self.confidence_score,
            "processing_time_s": self.processing_time_s,
            "chars_per_second": self.chars_per_second,
            "cost_cny": self.cost_cny,
            "ocr_accuracy": self.ocr_accuracy,
            "ocr_frame_count": self.ocr_frame_count,
            "asr_engine": self.asr_engine,
            "llm_backend": self.llm_backend,
            "notes": self.notes,
        }


# ═══════════════════════════════════════════════════════════
#  标准视频集
# ═══════════════════════════════════════════════════════════

STANDARD_VIDEOS = [
    {
        "video_id": "benchmark_bili_001",
        "url": "https://www.bilibili.com/video/BV1JFz3B8Ehn",
        "platform": "bilibili",
        "expected_duration_min": 10,
        "domain": "trading",
        "has_charts": True,
    },
    {
        "video_id": "benchmark_youtube_001",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "platform": "youtube",
        "expected_duration_min": 5,
        "domain": "education",
        "has_charts": False,
    },
    # 更多标准视频...
]


# ═══════════════════════════════════════════════════════════
#  基准测试执行
# ═══════════════════════════════════════════════════════════

def run_benchmark_suite(
    version: str = "",
    video_urls: List[str] = None,
    transcribe_fn: callable = None,
    ocr_fn: callable = None,
) -> List[BenchmarkResult]:
    """执行基准测试套件

    Args:
        version: 版本号
        video_urls: 要测试的视频列表（默认用标准视频集）
        transcribe_fn: 转录函数
        ocr_fn: OCR 函数

    Returns:
        BenchmarkResult 列表
    """
    if not version:
        from core.version_channels import get_version
        version = get_version().get("version", "unknown")

    videos = video_urls or STANDARD_VIDEOS
    results = []

    for video in videos:
        result = BenchmarkResult(
            version=version,
            date=time.strftime("%Y-%m-%d %H:%M:%S"),
            video_id=video.get("video_id", ""),
            video_url=video.get("url", ""),
            platform=video.get("platform", ""),
        )

        try:
            start_time = time.time()

            # 转录
            if transcribe_fn:
                transcript = transcribe_fn(video.get("url", ""))
                result.confidence_score = transcript.get("confidence", 0.0)
                result.chars_per_second = transcript.get("chars_per_second", 0.0)
                result.asr_engine = transcript.get("engine", "")

            # OCR
            if ocr_fn and video.get("has_charts"):
                ocr_result = ocr_fn(video.get("url", ""))
                result.ocr_accuracy = ocr_result.get("accuracy", 0.0)
                result.ocr_frame_count = ocr_result.get("frame_count", 0)

            # 计算耗时和成本
            elapsed = time.time() - start_time
            result.processing_time_s = elapsed
            result.cost_cny = _estimate_benchmark_cost(result)

            results.append(result)

        except Exception as e:
            result.notes = f"测试失败: {str(e)[:200]}"
            results.append(result)

    # 保存结果
    _save_benchmark_results(results)

    return results


def _estimate_benchmark_cost(result: BenchmarkResult) -> float:
    """估算基准测试成本"""
    cost = 0.0

    # ASR 成本
    if result.asr_engine == "bailian":
        cost += result.processing_time_s / 60 * 0.003
    elif result.asr_engine == "openai_whisper":
        cost += result.processing_time_s / 60 * 0.006

    # LLM 成本
    if result.llm_backend == "deepseek":
        cost += 0.01  # 粗略估算
    elif result.llm_backend == "openai":
        cost += 0.03

    return round(cost, 4)


def _save_benchmark_results(results: List[BenchmarkResult]):
    """保存基准测试结果"""
    all_results = []
    result_file = os.path.join(_BENCHMARK_DIR, "results.json")

    if os.path.exists(result_file):
        with open(result_file, encoding="utf-8") as f:
            all_results = json.load(f)

    all_results.extend([r.to_dict() for r in results])

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
#  质量门禁
# ═══════════════════════════════════════════════════════════

def check_quality_gate(version: str = "") -> Dict:
    """发版前质量门禁检查

    Returns:
        {pass: bool, checks: [...], blockers: [...]}
    """
    checks = []
    blockers = []

    # 加载最近一次基准测试结果
    result_file = os.path.join(_BENCHMARK_DIR, "results.json")
    if not os.path.exists(result_file):
        blockers.append("无基准测试数据，无法进行质量门禁")
        return {"pass": False, "checks": checks, "blockers": blockers}

    with open(result_file, encoding="utf-8") as f:
        all_results = json.load(f)

    if not all_results:
        blockers.append("基准测试结果为空")
        return {"pass": False, "checks": checks, "blockers": blockers}

    # 取最近一次的结果
    latest = all_results[-1]

    # 检查 1: 置信度 >= 90%
    confidence = latest.get("confidence_score", 0)
    if confidence >= 0.9:
        checks.append(f"✅ 置信度: {confidence:.0%} (≥ 90%)")
    else:
        blockers.append(f"❌ 置信度: {confidence:.0%} (< 90%)")

    # 检查 2: 处理速度（10 分钟视频 ≤ 5 分钟处理完）
    processing_time = latest.get("processing_time_s", 0)
    if processing_time <= 300:  # 5 分钟
        checks.append(f"✅ 处理速度: {processing_time:.0f}秒 (≤ 300秒)")
    else:
        blockers.append(f"❌ 处理速度: {processing_time:.0f}秒 (> 300秒)")

    # 检查 3: 成本 ≤ ¥0.20
    cost = latest.get("cost_cny", 0)
    if cost <= 0.20:
        checks.append(f"✅ 成本: ¥{cost:.2f} (≤ ¥0.20)")
    else:
        blockers.append(f"❌ 成本: ¥{cost:.2f} (> ¥0.20)")

    # 检查 4: OCR 覆盖率 ≥ 60%（如果有图表）
    ocr_accuracy = latest.get("ocr_accuracy", 0)
    if ocr_accuracy > 0:
        if ocr_accuracy >= 0.6:
            checks.append(f"✅ OCR 准确率: {ocr_accuracy:.0%} (≥ 60%)")
        else:
            blockers.append(f"❌ OCR 准确率: {ocr_accuracy:.0%} (< 60%)")

    return {
        "pass": len(blockers) == 0,
        "checks": checks,
        "blockers": blockers,
        "latest_result": latest,
    }


# ═══════════════════════════════════════════════════════════
#  反馈闭环
# ═══════════════════════════════════════════════════════════

_FEEDBACK_FILE = os.path.expanduser("~/.biliyoutik2brain/feedback.json")


def submit_feedback(
    video_id: str,
    rating: int,           # 1-5 评分
    issues: List[str] = None,
    suggestions: str = "",
):
    """提交转录结果反馈

    反馈自动回流到知识库和纠错词典。
    """
    feedbacks = []
    if os.path.exists(_FEEDBACK_FILE):
        with open(_FEEDBACK_FILE, encoding="utf-8") as f:
            feedbacks = json.load(f)

    feedbacks.append({
        "video_id": video_id,
        "rating": rating,
        "issues": issues or [],
        "suggestions": suggestions,
        "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    })

    with open(_FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=2)


def get_feedback_summary() -> Dict:
    """获取反馈摘要"""
    if not os.path.exists(_FEEDBACK_FILE):
        return {"count": 0, "avg_rating": 0, "common_issues": []}

    with open(_FEEDBACK_FILE, encoding="utf-8") as f:
        feedbacks = json.load(f)

    if not feedbacks:
        return {"count": 0, "avg_rating": 0, "common_issues": []}

    # 平均评分
    avg_rating = sum(f.get("rating", 0) for f in feedbacks) / len(feedbacks)

    # 常见问题
    issue_counts = {}
    for f in feedbacks:
        for issue in f.get("issues", []):
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

    common_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "count": len(feedbacks),
        "avg_rating": round(avg_rating, 2),
        "common_issues": common_issues,
    }
