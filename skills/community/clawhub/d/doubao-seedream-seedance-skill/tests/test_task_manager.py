"""
Tests for task manager.

Tests verify task lifecycle management.
"""

import pytest
from toolkit.task_manager import TaskManager
from toolkit.models.base import TaskStatus, TaskType
from toolkit.models.task import TaskParams, TaskResult
from toolkit.api_client import VolcengineAPIClient
from toolkit.config import ConfigManager
from toolkit.error_handler import TaskError


@pytest.fixture
def task_manager():
    """Create task manager for testing."""
    config = ConfigManager()
    config.set("api_key", "test-api-key")
    api_client = VolcengineAPIClient(config=config)
    
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as tmpdir:
        from toolkit.state_manager import StateManager
        state_manager = StateManager(state_dir=Path(tmpdir))
        yield TaskManager(api_client, state_manager)
    
    api_client.close()


class TestTaskManager:
    """Test cases for TaskManager."""
    
    class TestParams(TaskParams):
        prompt: str = "test prompt"
    
    def test_create_task(self, task_manager):
        """Test task creation."""
        params = self.TestParams()
        task = task_manager.create_task(TaskType.IMAGE_GENERATION, params)
        
        assert task.id is not None
        assert task.type == TaskType.IMAGE_GENERATION
        assert task.status == TaskStatus.QUEUED
        assert task.created_at is not None
    
    def test_update_task_status(self, task_manager):
        """Test updating task status."""
        params = self.TestParams()
        task = task_manager.create_task(TaskType.VIDEO_T2V, params)
        
        updated = task_manager.update_task_status(
            task.id,
            TaskStatus.RUNNING
        )
        
        assert updated.status == TaskStatus.RUNNING
        assert updated.updated_at > updated.created_at
    
    def test_update_task_with_result(self, task_manager):
        """Test updating task with result."""
        params = self.TestParams()
        task = task_manager.create_task(TaskType.AUDIO_TTS, params)
        
        result = TaskResult(url="https://example.com/audio.mp3")
        updated = task_manager.update_task_status(
            task.id,
            TaskStatus.SUCCEEDED,
            result=result
        )
        
        assert updated.status == TaskStatus.SUCCEEDED
        assert updated.result.url == "https://example.com/audio.mp3"
    
    def test_update_task_with_error(self, task_manager):
        """Test updating task with error."""
        params = self.TestParams()
        task = task_manager.create_task(TaskType.VISION_DETECTION, params)
        
        updated = task_manager.update_task_status(
            task.id,
            TaskStatus.FAILED,
            error="API error"
        )
        
        assert updated.status == TaskStatus.FAILED
        assert updated.error == "API error"
    
    def test_get_task(self, task_manager):
        """Test getting task by ID."""
        params = self.TestParams()
        created = task_manager.create_task(TaskType.IMAGE_EDIT, params)
        
        retrieved = task_manager.get_task(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id
    
    def test_get_nonexistent_task(self, task_manager):
        """Test getting nonexistent task."""
        task = task_manager.get_task("nonexistent-id")
        assert task is None
    
    def test_list_tasks(self, task_manager):
        """Test listing all tasks."""
        params = self.TestParams()
        task_manager.create_task(TaskType.IMAGE_GENERATION, params)
        task_manager.create_task(TaskType.VIDEO_T2V, params)
        
        tasks = task_manager.list_tasks()
        
        assert len(tasks) == 2
    
    def test_list_tasks_by_status(self, task_manager):
        """Test listing tasks by status."""
        params = self.TestParams()
        task1 = task_manager.create_task(TaskType.IMAGE_GENERATION, params)
        task2 = task_manager.create_task(TaskType.VIDEO_T2V, params)
        
        task_manager.update_task_status(task1.id, TaskStatus.RUNNING)
        
        running = task_manager.list_tasks(status=TaskStatus.RUNNING)
        queued = task_manager.list_tasks(status=TaskStatus.QUEUED)
        
        assert len(running) == 1
        assert len(queued) == 1
    
    def test_list_tasks_by_type(self, task_manager):
        """Test listing tasks by type."""
        params = self.TestParams()
        task_manager.create_task(TaskType.IMAGE_GENERATION, params)
        task_manager.create_task(TaskType.VIDEO_T2V, params)
        task_manager.create_task(TaskType.VIDEO_I2V, params)
        
        video_tasks = task_manager.list_tasks(task_type=TaskType.VIDEO_T2V)
        
        assert len(video_tasks) == 1
    
    def test_list_tasks_with_limit(self, task_manager):
        """Test listing tasks with limit."""
        params = self.TestParams()
        for _ in range(10):
            task_manager.create_task(TaskType.IMAGE_GENERATION, params)
        
        tasks = task_manager.list_tasks(limit=5)
        
        assert len(tasks) == 5
    
    def test_delete_task(self, task_manager):
        """Test deleting task."""
        params = self.TestParams()
        task = task_manager.create_task(TaskType.AUDIO_TTS, params)
        
        result = task_manager.delete_task(task.id)
        
        assert result is True
        assert task_manager.get_task(task.id) is None
    
    def test_delete_nonexistent_task(self, task_manager):
        """Test deleting nonexistent task."""
        result = task_manager.delete_task("nonexistent-id")
        assert result is False
    
    def test_update_nonexistent_task_raises_error(self, task_manager):
        """Test updating nonexistent task raises error."""
        with pytest.raises(TaskError):
            task_manager.update_task_status(
                "nonexistent-id",
                TaskStatus.RUNNING
            )
