"""
Tests for task data models.

Tests verify the correctness of TaskParams, TaskResult, and TaskInfo models.
"""

import pytest
from datetime import datetime
from toolkit.models.base import TaskStatus, TaskType
from toolkit.models.task import TaskParams, TaskResult, TaskInfo


class TestTaskParams:
    """Test cases for TaskParams model."""
    
    def test_task_params_creation(self):
        """Test that TaskParams can be created."""
        params = TaskParams()
        assert params is not None
    
    def test_task_params_inheritance(self):
        """Test that TaskParams inherits from BaseModelConfig."""
        from toolkit.models.base import BaseModelConfig
        assert isinstance(TaskParams(), BaseModelConfig)
    
    def test_task_params_extension(self):
        """Test that TaskParams can be extended."""
        
        class ImageParams(TaskParams):
            prompt: str
            width: int = 512
            height: int = 512
        
        params = ImageParams(prompt="test image", width=1024, height=768)
        assert params.prompt == "test image"
        assert params.width == 1024
        assert params.height == 768


class TestTaskResult:
    """Test cases for TaskResult model."""
    
    def test_task_result_empty(self):
        """Test that TaskResult can be created with no fields."""
        result = TaskResult()
        assert result.url is None
        assert result.local_path is None
        assert result.metadata is None
    
    def test_task_result_with_url(self):
        """Test TaskResult with URL."""
        result = TaskResult(url="https://example.com/image.png")
        assert result.url == "https://example.com/image.png"
    
    def test_task_result_with_local_path(self):
        """Test TaskResult with local path."""
        result = TaskResult(local_path="/tmp/image.png")
        assert result.local_path == "/tmp/image.png"
    
    def test_task_result_with_metadata(self):
        """Test TaskResult with metadata."""
        metadata = {"width": 1024, "height": 768, "format": "png"}
        result = TaskResult(metadata=metadata)
        assert result.metadata == metadata
    
    def test_task_result_full(self):
        """Test TaskResult with all fields."""
        result = TaskResult(
            url="https://example.com/image.png",
            local_path="/tmp/image.png",
            metadata={"size": 1024}
        )
        assert result.url == "https://example.com/image.png"
        assert result.local_path == "/tmp/image.png"
        assert result.metadata["size"] == 1024


class TestTaskInfo:
    """Test cases for TaskInfo model."""
    
    def test_task_info_creation(self):
        """Test that TaskInfo can be created with required fields."""
        now = datetime.now()
        task = TaskInfo(
            id="task-123",
            type=TaskType.IMAGE_GENERATION,
            status=TaskStatus.QUEUED,
            params=TaskParams(),
            created_at=now,
            updated_at=now
        )
        assert task.id == "task-123"
        assert task.type == TaskType.IMAGE_GENERATION
        assert task.status == TaskStatus.QUEUED
        assert task.created_at == now
        assert task.updated_at == now
    
    def test_task_info_with_result(self):
        """Test TaskInfo with result."""
        now = datetime.now()
        result = TaskResult(url="https://example.com/image.png")
        task = TaskInfo(
            id="task-123",
            type=TaskType.IMAGE_GENERATION,
            status=TaskStatus.SUCCEEDED,
            params=TaskParams(),
            result=result,
            created_at=now,
            updated_at=now
        )
        assert task.result.url == "https://example.com/image.png"
    
    def test_task_info_with_error(self):
        """Test TaskInfo with error."""
        now = datetime.now()
        task = TaskInfo(
            id="task-123",
            type=TaskType.IMAGE_GENERATION,
            status=TaskStatus.FAILED,
            params=TaskParams(),
            error="API error: rate limit exceeded",
            created_at=now,
            updated_at=now
        )
        assert task.error == "API error: rate limit exceeded"
    
    def test_task_info_json_serialization(self):
        """Test that TaskInfo serializes enums to strings."""
        now = datetime.now()
        task = TaskInfo(
            id="task-123",
            type=TaskType.IMAGE_GENERATION,
            status=TaskStatus.RUNNING,
            params=TaskParams(),
            created_at=now,
            updated_at=now
        )
        
        task_dict = task.model_dump()
        assert task_dict["type"] == "image_generation"
        assert task_dict["status"] == "running"
    
    def test_task_info_datetime_serialization(self):
        """Test that TaskInfo serializes datetime to ISO format."""
        now = datetime(2024, 1, 1, 12, 0, 0)
        task = TaskInfo(
            id="task-123",
            type=TaskType.VIDEO_T2V,
            status=TaskStatus.QUEUED,
            params=TaskParams(),
            created_at=now,
            updated_at=now
        )
        
        task_dict = task.model_dump()
        assert isinstance(task_dict["created_at"], datetime)
        assert isinstance(task_dict["updated_at"], datetime)
    
    def test_task_info_different_types(self):
        """Test TaskInfo with different task types."""
        now = datetime.now()
        
        for task_type in [TaskType.IMAGE_GENERATION, TaskType.VIDEO_T2V, 
                          TaskType.VISION_DETECTION]:
            task = TaskInfo(
                id=f"task-{task_type.value}",
                type=task_type,
                status=TaskStatus.QUEUED,
                params=TaskParams(),
                created_at=now,
                updated_at=now
            )
            assert task.type == task_type
    def test_task_info_different_statuses(self):
        """Test TaskInfo with different task statuses."""
        now = datetime.now()
        
        for status in [TaskStatus.QUEUED, TaskStatus.RUNNING, 
                       TaskStatus.SUCCEEDED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            task = TaskInfo(
                id=f"task-{status.value}",
                type=TaskType.IMAGE_GENERATION,
                status=status,
                params=TaskParams(),
                created_at=now,
                updated_at=now
            )
            assert task.status == status
