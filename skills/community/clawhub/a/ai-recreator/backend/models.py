"""数据模型"""
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Any


class TaskStatus(str, Enum):
    # Phase 1
    PENDING = "pending"
    DOWNLOADING = "downloading"
    TRANSCRIBING = "transcribing"
    REWRITING = "rewriting"
    AWAITING_REVIEW = "awaiting_review"

    # Phase 2
    GENERATING_SPEECH = "generating_speech"
    TTS_COMPLETE = "tts_complete"  # 等用户上传参考视频
    AWAITING_VIDEO = "awaiting_video"

    # Phase 3
    GENERATING_VIDEO = "generating_video"
    COMPLETED = "completed"
    FAILED = "failed"


class CreateTaskRequest(BaseModel):
    video_url: str = Field(..., description="抖音/短视频链接")
    custom_prompt: str = Field(default="", description="改写风格提示，可选")
    tts_voice: str = Field(default="zh-CN-XiaoxiaoNeural", description="TTS 音色")


class CreateTaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    message: str = "任务已提交"


class TaskProgress(BaseModel):
    task_id: str
    status: TaskStatus
    progress: int = 0  # 0-100
    message: str = ""
    total_steps: int = 5
    current_step: int = 0

    # Phase 1 结果
    original_title: Optional[str] = None
    original_text: Optional[str] = None
    rewritten_text: Optional[str] = None

    # Phase 2 结果
    audio_url: Optional[str] = None
    tts_voice: Optional[str] = None

    # Phase 3 结果
    video_url: Optional[str] = None

    duration_ms: Optional[int] = None


class ConfirmRewriteRequest(BaseModel):
    """Phase 1 → Phase 2"""
    rewritten_text: str = Field(default="", description="用户编辑的改写稿")
    custom_prompt: str = Field(default="", description="改写风格提示")
    tts_voice: str = Field(default="zh-CN-XiaoxiaoNeural", description="TTS 音色")


class ConfirmRewriteResponse(BaseModel):
    task_id: str
    status: TaskStatus = "generating_speech"
    message: str = "正在合成语音..."


class StartVideoRequest(BaseModel):
    """Phase 2 → Phase 3: 开始合成数字人视频"""
    pass  # 音频已存在，不需额外参数


class StartVideoResponse(BaseModel):
    task_id: str
    status: TaskStatus = "generating_video"
    message: str = "正在生成数字人视频..."


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[Any] = None
