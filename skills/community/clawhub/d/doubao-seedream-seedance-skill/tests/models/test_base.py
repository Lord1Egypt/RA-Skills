"""
Tests for base data models.

Tests verify the correctness of TaskStatus, TaskType enums
and BaseModelConfig base class.
"""

import json
import pytest
from toolkit.models.base import TaskStatus, TaskType, BaseModelConfig


class TestTaskStatus:
    """Test cases for TaskStatus enum."""
    
    def test_task_status_values(self):
        """Test that TaskStatus has all required values."""
        assert TaskStatus.QUEUED == "queued"
        assert TaskStatus.RUNNING == "running"
        assert TaskStatus.SUCCEEDED == "succeeded"
        assert TaskStatus.FAILED == "failed"
        assert TaskStatus.CANCELLED == "cancelled"
    
    def test_task_status_count(self):
        """Test that TaskStatus has exactly 5 values."""
        assert len(TaskStatus) == 5
    
    def test_task_status_is_string_enum(self):
        """Test that TaskStatus is a string enum."""
        assert isinstance(TaskStatus.QUEUED, str)
        assert TaskStatus.QUEUED.value == "queued"


class TestTaskType:
    """Test cases for TaskType enum."""
    
    def test_task_type_values(self):
        """Test that TaskType has all required values."""
        assert TaskType.IMAGE_GENERATION == "image_generation"
        assert TaskType.IMAGE_EDIT == "image_edit"
        assert TaskType.VIDEO_T2V == "video_t2v"
        assert TaskType.VIDEO_I2V == "video_i2v"
        assert TaskType.VIDEO_FRAMES == "video_frames"
        assert TaskType.VIDEO_REFERENCES == "video_references"
        assert TaskType.AUDIO_TTS == "audio_tts"
        assert TaskType.VISION_DETECTION == "vision_detection"
    
    def test_task_type_count(self):
        """Test that TaskType has exactly 8 values."""
        assert len(TaskType) == 8
    
    def test_task_type_is_string_enum(self):
        """Test that TaskType is a string enum."""
        assert isinstance(TaskType.IMAGE_GENERATION, str)
        assert TaskType.IMAGE_GENERATION.value == "image_generation"


class TestBaseModelConfig:
    """Test cases for BaseModelConfig base class."""
    
    def test_base_model_config_inheritance(self):
        """Test that BaseModelConfig can be inherited."""
        
        class TestModel(BaseModelConfig):
            name: str
            value: int
        
        # Should be able to create instance
        instance = TestModel(name="test", value=42)
        assert instance.name == "test"
        assert instance.value == 42
    
    def test_base_model_config_with_enum(self):
        """Test that BaseModelConfig properly handles enums."""
        
        class TaskModel(BaseModelConfig):
            status: TaskStatus
            type: TaskType
        
        # Create instance with enum values
        task = TaskModel(status=TaskStatus.RUNNING, type=TaskType.IMAGE_GENERATION)
        
        # Should serialize enum values to strings
        task_dict = task.model_dump()
        assert task_dict["status"] == "running"
        assert task_dict["type"] == "image_generation"
    
    def test_base_model_config_validation(self):
        """Test that BaseModelConfig validates data properly."""
        
        class StrictModel(BaseModelConfig):
            count: int
        
        # Should validate types
        with pytest.raises(Exception):
            StrictModel(**json.loads('{"count": "not an int"}'))
        
        # Should accept valid data
        instance = StrictModel(count=10)
        assert instance.count == 10
