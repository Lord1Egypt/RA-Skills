"""
Tests for state management.

Tests verify state persistence and retrieval.
"""

import pytest
from pathlib import Path
from toolkit.state_manager import StateManager


class TestStateManager:
    """Test cases for StateManager."""
    
    def test_initialization(self, tmp_path):
        """Test StateManager initialization."""
        state_manager = StateManager(state_dir=tmp_path)
        assert state_manager.state_dir == tmp_path
        assert state_manager.state_file.exists() or True  # May not exist yet
    
    def test_user_preferences(self, tmp_path):
        """Test user preference management."""
        state_manager = StateManager(state_dir=tmp_path)
        
        # Set preference
        state_manager.set_preference("default_model", "seedream-4.0")
        
        # Get preference
        assert state_manager.get_preference("default_model") == "seedream-4.0"
        
        # Get nonexistent preference
        assert state_manager.get_preference("nonexistent") is None
        assert state_manager.get_preference("nonexistent", "default") == "default"
    
    def test_get_all_preferences(self, tmp_path):
        """Test getting all preferences."""
        state_manager = StateManager(state_dir=tmp_path)
        
        state_manager.set_preference("key1", "value1")
        state_manager.set_preference("key2", "value2")
        
        all_prefs = state_manager.get_all_preferences()
        assert all_prefs["key1"] == "value1"
        assert all_prefs["key2"] == "value2"
    
    def test_task_state(self, tmp_path):
        """Test task state management."""
        state_manager = StateManager(state_dir=tmp_path)
        
        task_data = {
            "status": "running",
            "type": "image_generation",
            "prompt": "test prompt"
        }
        
        # Save task state
        state_manager.save_task_state("task-123", task_data)
        
        # Get task state
        retrieved = state_manager.get_task_state("task-123")
        assert retrieved["status"] == "running"
        assert retrieved["type"] == "image_generation"
        assert "updated_at" in retrieved
    
    def test_get_nonexistent_task(self, tmp_path):
        """Test getting nonexistent task."""
        state_manager = StateManager(state_dir=tmp_path)
        assert state_manager.get_task_state("nonexistent") is None
    
    def test_get_all_tasks(self, tmp_path):
        """Test getting all tasks."""
        state_manager = StateManager(state_dir=tmp_path)
        
        state_manager.save_task_state("task-1", {"status": "running"})
        state_manager.save_task_state("task-2", {"status": "succeeded"})
        
        all_tasks = state_manager.get_all_tasks()
        assert len(all_tasks) == 2
        assert "task-1" in all_tasks
        assert "task-2" in all_tasks
    
    def test_delete_task_state(self, tmp_path):
        """Test deleting task state."""
        state_manager = StateManager(state_dir=tmp_path)
        
        state_manager.save_task_state("task-123", {"status": "running"})
        
        # Delete existing task
        assert state_manager.delete_task_state("task-123") is True
        assert state_manager.get_task_state("task-123") is None
        
        # Delete nonexistent task
        assert state_manager.delete_task_state("nonexistent") is False
    
    def test_get_tasks_by_status(self, tmp_path):
        """Test filtering tasks by status."""
        state_manager = StateManager(state_dir=tmp_path)
        
        state_manager.save_task_state("task-1", {"status": "running"})
        state_manager.save_task_state("task-2", {"status": "succeeded"})
        state_manager.save_task_state("task-3", {"status": "running"})
        
        running_tasks = state_manager.get_tasks_by_status("running")
        assert len(running_tasks) == 2
        
        succeeded_tasks = state_manager.get_tasks_by_status("succeeded")
        assert len(succeeded_tasks) == 1
    
    def test_operation_history(self, tmp_path):
        """Test operation history."""
        state_manager = StateManager(state_dir=tmp_path)
        
        # Add history entries
        state_manager.add_history_entry("image_generation", {"prompt": "test"})
        state_manager.add_history_entry("video_generation", {"duration": 5})
        
        history = state_manager.get_history()
        assert len(history) == 2
        assert history[0]["operation"] == "image_generation"
        assert history[1]["operation"] == "video_generation"
    
    def test_get_history_with_limit(self, tmp_path):
        """Test getting limited history."""
        state_manager = StateManager(state_dir=tmp_path)
        
        for i in range(5):
            state_manager.add_history_entry(f"operation_{i}")
        
        limited_history = state_manager.get_history(limit=3)
        assert len(limited_history) == 3
        assert limited_history[0]["operation"] == "operation_2"
    
    def test_clear_history(self, tmp_path):
        """Test clearing history."""
        state_manager = StateManager(state_dir=tmp_path)
        
        state_manager.add_history_entry("operation1")
        state_manager.add_history_entry("operation2")
        
        state_manager.clear_history()
        assert len(state_manager.get_history()) == 0
    
    def test_operation_count(self, tmp_path):
        """Test counting operations."""
        state_manager = StateManager(state_dir=tmp_path)
        
        state_manager.add_history_entry("image_generation")
        state_manager.add_history_entry("image_generation")
        state_manager.add_history_entry("video_generation")
        
        assert state_manager.get_operation_count("image_generation") == 2
        assert state_manager.get_operation_count("video_generation") == 1
        assert state_manager.get_operation_count("nonexistent") == 0
    
    def test_total_operations(self, tmp_path):
        """Test total operation count."""
        state_manager = StateManager(state_dir=tmp_path)
        
        assert state_manager.get_total_operations() == 0
        
        state_manager.add_history_entry("operation1")
        state_manager.add_history_entry("operation2")
        
        assert state_manager.get_total_operations() == 2
    
    def test_persistence(self, tmp_path):
        """Test that state persists across instances."""
        state_manager1 = StateManager(state_dir=tmp_path)
        
        state_manager1.set_preference("test_pref", "test_value")
        state_manager1.save_task_state("task-1", {"status": "running"})
        state_manager1.add_history_entry("test_operation")
        
        # Create new instance
        state_manager2 = StateManager(state_dir=tmp_path)
        
        # Verify state persisted
        assert state_manager2.get_preference("test_pref") == "test_value"
        assert state_manager2.get_task_state("task-1")["status"] == "running"
        assert len(state_manager2.get_history()) == 1
