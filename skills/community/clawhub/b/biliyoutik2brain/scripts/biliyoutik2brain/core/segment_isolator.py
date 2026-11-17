"""
BiliYouTik2Brain — 分段隔离器 (v4.0)

长视频分段隔离执行，某段失败不影响其他段。
支持问题段重跑，不用全量重来。
"""

import os
import json
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class SegmentResult:
    """单段处理结果"""
    segment_id: str
    start_time: float
    end_time: float
    success: bool
    text: str = ""
    confidence: float = 0.0
    error: str = ""
    retry_count: int = 0
    processing_time_ms: float = 0


@dataclass
class SegmentedTask:
    """分段任务"""
    task_id: str
    video_path: str
    total_duration: float
    segments: List[SegmentResult] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    @property
    def success_rate(self) -> float:
        if not self.segments:
            return 0.0
        return sum(1 for s in self.segments if s.success) / len(self.segments)

    @property
    def failed_segments(self) -> List[SegmentResult]:
        return [s for s in self.segments if not s.success]


# ═══════════════════════════════════════════════════════════
#  分段策略
# ═══════════════════════════════════════════════════════════

def split_video_into_segments(
    duration_s: float,
    segment_duration: float = 300,  # 默认 5 分钟一段
    overlap_s: float = 10,           # 段间重叠 10 秒
) -> List[Tuple[float, float]]:
    """将视频分成多个段

    Args:
        duration_s: 视频总时长（秒）
        segment_duration: 每段时长（秒）
        overlap_s: 段间重叠（秒）

    Returns:
        [(start, end), ...] 列表
    """
    if duration_s <= segment_duration:
        return [(0, duration_s)]

    segments = []
    current = 0
    while current < duration_s:
        end = min(current + segment_duration, duration_s)
        segments.append((current, end))
        current = end - overlap_s  # 重叠

    return segments


# ═══════════════════════════════════════════════════════════
#  隔离执行
# ═══════════════════════════════════════════════════════════

def process_segment_isolated(
    video_path: str,
    start: float,
    end: float,
    segment_id: str,
    transcribe_fn: callable,
    max_retries: int = 2,
) -> SegmentResult:
    """隔离处理单段

    Args:
        video_path: 视频路径
        start: 段起始时间（秒）
        end: 段结束时间（秒）
        segment_id: 段 ID
        transcribe_fn: 转录函数 (audio_path) -> {text, confidence}
        max_retries: 最大重试次数

    Returns:
        SegmentResult
    """
    import subprocess
    import tempfile

    start_time = time.time()

    for attempt in range(max_retries + 1):
        try:
            # 1. 裁剪音频段
            with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as tmp:
                tmp_path = tmp.name

            result = subprocess.run(
                [
                    "ffmpeg", "-y", "-ss", str(start), "-to", str(end),
                    "-i", video_path, "-vn", "-acodec", "aac",
                    tmp_path,
                ],
                capture_output=True, text=True, timeout=120,
            )

            if result.returncode != 0:
                raise RuntimeError(f"ffmpeg 裁剪失败: {result.stderr[:200]}")

            # 2. 转录
            transcribe_result = transcribe_fn(tmp_path)
            text = transcribe_result.get("text", "")
            confidence = transcribe_result.get("confidence", 0.0)

            # 3. 清理临时文件
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

            processing_ms = (time.time() - start_time) * 1000

            return SegmentResult(
                segment_id=segment_id,
                start_time=start,
                end_time=end,
                success=True,
                text=text,
                confidence=confidence,
                retry_count=attempt,
                processing_time_ms=processing_ms,
            )

        except Exception as e:
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # 指数退避
                continue
            else:
                processing_ms = (time.time() - start_time) * 1000
                return SegmentResult(
                    segment_id=segment_id,
                    start_time=start,
                    end_time=end,
                    success=False,
                    error=str(e)[:200],
                    retry_count=attempt,
                    processing_time_ms=processing_ms,
                )

    return SegmentResult(
        segment_id=segment_id,
        start_time=start,
        end_time=end,
        success=False,
        error="未知错误",
        processing_time_ms=(time.time() - start_time) * 1000,
    )


def process_video_segmented(
    video_path: str,
    duration_s: float,
    transcribe_fn: callable,
    segment_duration: float = 300,
    overlap_s: float = 10,
    max_retries: int = 2,
) -> SegmentedTask:
    """分段处理整个视频

    Args:
        video_path: 视频路径
        duration_s: 总时长
        transcribe_fn: 转录函数
        segment_duration: 每段时长
        overlap_s: 段间重叠
        max_retries: 每段最大重试

    Returns:
        SegmentedTask（含所有段结果）
    """
    segments = split_video_into_segments(duration_s, segment_duration, overlap_s)
    task = SegmentedTask(
        task_id=f"seg_{int(time.time())}",
        video_path=video_path,
        total_duration=duration_s,
        created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
    )

    for i, (start, end) in enumerate(segments):
        seg_id = f"seg_{i:03d}"
        result = process_segment_isolated(
            video_path=video_path,
            start=start,
            end=end,
            segment_id=seg_id,
            transcribe_fn=transcribe_fn,
            max_retries=max_retries,
        )
        task.segments.append(result)

    task.updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
    return task


def retry_failed_segments(
    task: SegmentedTask,
    transcribe_fn: callable,
    max_retries: int = 2,
) -> SegmentedTask:
    """重跑失败的段

    Args:
        task: 分段任务
        transcribe_fn: 转录函数
        max_retries: 重试次数

    Returns:
        更新后的 SegmentedTask
    """
    failed = task.failed_segments
    if not failed:
        return task

    for seg in failed:
        new_result = process_segment_isolated(
            video_path=task.video_path,
            start=seg.start_time,
            end=seg.end_time,
            segment_id=seg.segment_id,
            transcribe_fn=transcribe_fn,
            max_retries=max_retries,
        )

        # 更新段结果
        for i, existing in enumerate(task.segments):
            if existing.segment_id == seg.segment_id:
                task.segments[i] = new_result
                break

    task.updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
    return task


# ═══════════════════════════════════════════════════════════
#  合并结果
# ═══════════════════════════════════════════════════════════

def merge_segment_results(task: SegmentedTask) -> Dict:
    """合并分段结果

    Returns:
        {
            "full_text": str,
            "segments": [...],
            "overall_confidence": float,
            "success_rate": float,
            "failed_segments": [...],
        }
    """
    full_text = ""
    total_confidence = 0
    valid_count = 0

    segments_data = []
    for seg in sorted(task.segments, key=lambda s: s.start_time):
        segments_data.append({
            "start": seg.start_time,
            "end": seg.end_time,
            "text": seg.text,
            "confidence": seg.confidence,
            "success": seg.success,
            "error": seg.error if not seg.success else None,
        })

        if seg.success:
            full_text += seg.text + "\n"
            total_confidence += seg.confidence
            valid_count += 1

    return {
        "full_text": full_text.strip(),
        "segments": segments_data,
        "overall_confidence": total_confidence / max(1, valid_count),
        "success_rate": task.success_rate,
        "failed_segments": [
            {"id": s.segment_id, "start": s.start_time, "end": s.end_time, "error": s.error}
            for s in task.failed_segments
        ],
    }
