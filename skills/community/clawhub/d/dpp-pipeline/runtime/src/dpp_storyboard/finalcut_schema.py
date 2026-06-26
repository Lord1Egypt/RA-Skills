from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class FinalCutResult(BaseModel):
    """最终剪辑合成结果报告，记录将 generated 视频替换回原视频后的元数据。"""

    model_config = ConfigDict(extra="forbid")

    composition_result_path: str = Field(min_length=1)
    source_video_path: str = Field(min_length=1)
    generated_video_path: str = Field(min_length=1)
    best_segment_index: int = Field(ge=1)
    replace_start_sec: float = Field(ge=0)
    replace_end_sec: float = Field(gt=0)
    output_video_path: str = Field(min_length=1)
    generated_at: str = Field(min_length=1)


def build_finalcut_result(
    *,
    composition_result_path: str,
    source_video_path: str,
    generated_video_path: str,
    best_segment_index: int,
    replace_start_sec: float,
    replace_end_sec: float,
    output_video_path: str,
    generated_at: str | None = None,
) -> FinalCutResult:
    """构建 FinalCutResult 实例的工厂函数。"""

    timestamp = generated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return FinalCutResult(
        composition_result_path=composition_result_path,
        source_video_path=source_video_path,
        generated_video_path=generated_video_path,
        best_segment_index=best_segment_index,
        replace_start_sec=replace_start_sec,
        replace_end_sec=replace_end_sec,
        output_video_path=output_video_path,
        generated_at=timestamp,
    )
