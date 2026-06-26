"""
Base data models for Volcengine API Skill.

This module contains the foundational enums and base classes
used throughout the toolkit.
"""

from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""
    
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    """Enumeration of supported task types."""
    
    IMAGE_GENERATION = "image_generation"
    IMAGE_EDIT = "image_edit"
    VIDEO_T2V = "video_t2v"
    VIDEO_I2V = "video_i2v"
    VIDEO_FRAMES = "video_frames"
    VIDEO_REFERENCES = "video_references"
    AUDIO_TTS = "audio_tts"
    VISION_DETECTION = "vision_detection"


class BaseModelConfig(BaseModel):
    """
    Base configuration for all Pydantic models in the toolkit.
    
    Provides common configuration options including automatic
    enum value serialization.
    """
    
    class Config:
        use_enum_values = True
