"""Unit tests for Symphony Concurrency Manager"""

import pytest

from builder.symphony.concurrency import (
    ConcurrencyLimits, ConcurrencyState, ConcurrencyManager
)
from builder.symphony.state_machine import TaskState


class TestConcurrencyLimits:
    """Test ConcurrencyLimits dataclass"""

    def test_default_limits(self):
        """Test default concurrency limits"""
        limits = ConcurrencyLimits()

        assert limits.max_concurrent_builds == 3
        assert limits.building == 3
        assert limits.testing == 5
        assert limits.fixing == 2
        assert limits.publishing == 3

    def test_custom_limits(self):
        """Test custom concurrency limits"""
        limits = ConcurrencyLimits(
            max_concurrent_builds=5,
            building=5,
            testing=10,
            fixing=3,
            publishing=5
        )

        assert limits.max_concurrent_builds == 5
        assert limits.building == 5
        assert limits.testing == 10

    def test_limits_to_dict(self):
        """Test serialization to dict"""
        limits = ConcurrencyLimits()

        limits_dict = limits.to_dict()

        assert limits_dict['max_concurrent_builds'] == 3
        assert limits_dict['building'] == 3
        assert limits_dict['testing'] == 5


class TestConcurrencyState:
    """Test ConcurrencyState dataclass"""

    def test_initial_state(self):
        """Test initial concurrency state"""
        state = ConcurrencyState()

        assert len(state.active_tasks) == 0
        assert state.state_counts[TaskState.CLAIMED] == 0
        assert state.state_counts[TaskState.RUNNING] == 0


class TestConcurrencyManager:
    """Test ConcurrencyManager"""

    def test_initialization(self):
        """Test concurrency manager initialization"""
        limits = ConcurrencyLimits(max_concurrent_builds=2)
        manager = ConcurrencyManager(limits)

        assert manager.limits.max_concurrent_builds == 2
        assert len(manager.state.active_tasks) == 0

    def test_can_start_task(self):
        """Test checking if task can start"""
        manager = ConcurrencyManager()

        # Under capacity
        assert manager.can_start_task("task1", stage="building") is True

        # Start a task
        manager.start_task("task1", stage="building")

        # Still under capacity (max is 3)
        assert manager.can_start_task("task2", stage="building") is True

    def test_cannot_start_duplicate_task(self):
        """Test cannot start same task twice"""
        manager = ConcurrencyManager()

        manager.start_task("task1", stage="building")

        # Same task cannot start again
        assert manager.can_start_task("task1", stage="building") is False

    def test_cannot_start_at_capacity(self):
        """Test cannot start task at capacity"""
        limits = ConcurrencyLimits(max_concurrent_builds=2)
        manager = ConcurrencyManager(limits)

        # Start tasks up to capacity
        manager.start_task("task1", stage="building")
        manager.start_task("task2", stage="building")

        # At capacity, cannot start more
        assert manager.can_start_task("task3", stage="building") is False

    def test_start_task(self):
        """Test starting a task"""
        manager = ConcurrencyManager()

        result = manager.start_task("task1", stage="building")

        assert result is True
        assert "task1" in manager.state.active_tasks
        assert manager.task_stages["task1"] == "building"
        assert manager.state.state_counts[TaskState.RUNNING] == 1

    def test_start_task_at_capacity(self):
        """Test starting task at capacity fails"""
        limits = ConcurrencyLimits(max_concurrent_builds=1)
        manager = ConcurrencyManager(limits)

        manager.start_task("task1", stage="building")

        # Cannot start more at capacity
        result = manager.start_task("task2", stage="building")

        assert result is False
        assert "task2" not in manager.state.active_tasks

    def test_complete_task(self):
        """Test completing a task"""
        manager = ConcurrencyManager()

        manager.start_task("task1", stage="building")
        assert "task1" in manager.state.active_tasks

        result = manager.complete_task("task1")

        assert result is True
        assert "task1" not in manager.state.active_tasks
        assert "task1" not in manager.task_stages

    def test_complete_nonexistent_task(self):
        """Test completing nonexistent task"""
        manager = ConcurrencyManager()

        result = manager.complete_task("nonexistent")

        assert result is False

    def test_fail_task(self):
        """Test failing a task"""
        manager = ConcurrencyManager()

        manager.start_task("task1", stage="building")

        result = manager.fail_task("task1")

        assert result is True
        assert "task1" not in manager.state.active_tasks

    def test_get_active_count(self):
        """Test getting active task count"""
        manager = ConcurrencyManager()

        assert manager.get_active_count() == 0

        manager.start_task("task1", stage="building")
        assert manager.get_active_count() == 1

        manager.start_task("task2", stage="building")
        assert manager.get_active_count() == 2

    def test_get_available_slots(self):
        """Test getting available slots"""
        manager = ConcurrencyManager()

        # Default max is 3
        assert manager.get_available_slots() == 3

        manager.start_task("task1", stage="building")
        assert manager.get_available_slots() == 2

        manager.start_task("task2", stage="building")
        assert manager.get_available_slots() == 1

    def test_get_stage_count(self):
        """Test getting count by stage"""
        manager = ConcurrencyManager()

        manager.start_task("task1", stage="building")
        manager.start_task("task2", stage="testing")

        assert manager.get_stage_count("building") == 1
        assert manager.get_stage_count("testing") == 1
        assert manager.get_stage_count("fixing") == 0

    def test_get_stage_limit(self):
        """Test getting limit by stage"""
        manager = ConcurrencyManager()

        assert manager.get_stage_limit("building") == 3
        assert manager.get_stage_limit("testing") == 5
        assert manager.get_stage_limit("fixing") == 2

    def test_is_at_capacity(self):
        """Test checking if at capacity"""
        limits = ConcurrencyLimits(max_concurrent_builds=2)
        manager = ConcurrencyManager(limits)

        assert manager.is_at_capacity() is False

        manager.start_task("task1", stage="building")
        assert manager.is_at_capacity() is False

        manager.start_task("task2", stage="building")
        assert manager.is_at_capacity() is True

    def test_get_utilization(self):
        """Test getting utilization percentage"""
        limits = ConcurrencyLimits(max_concurrent_builds=10)
        manager = ConcurrencyManager(limits)

        assert manager.get_utilization() == 0.0

        manager.start_task("task1", stage="building")
        assert manager.get_utilization() == 10.0

        manager.start_task("task2", stage="building")
        assert manager.get_utilization() == 20.0

        manager.start_task("task3", stage="building")
        assert manager.get_utilization() == 30.0

    def test_get_active_tasks(self):
        """Test getting set of active tasks"""
        manager = ConcurrencyManager()

        manager.start_task("task1", stage="building")
        manager.start_task("task2", stage="testing")

        active = manager.get_active_tasks()

        assert "task1" in active
        assert "task2" in active
        assert len(active) == 2

    def test_get_task_stage(self):
        """Test getting stage for task"""
        manager = ConcurrencyManager()

        manager.start_task("task1", stage="building")

        assert manager.get_task_stage("task1") == "building"
        assert manager.get_task_stage("task2") is None

    def test_get_statistics(self):
        """Test getting statistics"""
        manager = ConcurrencyManager()

        manager.start_task("task1", stage="building")
        manager.start_task("task2", stage="testing")

        stats = manager.get_statistics()

        assert stats['active_tasks'] == 2
        assert stats['max_concurrent_builds'] == 3
        assert stats['available_slots'] == 1
        assert stats['utilization_percent'] == pytest.approx(66.67, rel=1.0)

    def test_update_limits(self):
        """Test updating limits"""
        manager = ConcurrencyManager()

        old_limits = manager.limits
        new_limits = ConcurrencyLimits(max_concurrent_builds=5)

        result = manager.update_limits(new_limits)

        assert result is True
        assert manager.limits.max_concurrent_builds == 5
        assert manager.limits is not old_limits

    def test_stage_limit_enforcement(self):
        """Test per-stage limit enforcement"""
        limits = ConcurrencyLimits(
            max_concurrent_builds=10,
            building=2  # Only 2 concurrent builds
        )
        manager = ConcurrencyManager(limits)

        # Start 2 building tasks (at stage limit)
        assert manager.can_start_task("task1", stage="building") is True
        manager.start_task("task1", stage="building")

        assert manager.can_start_task("task2", stage="building") is True
        manager.start_task("task2", stage="building")

        # 3rd building task should be blocked by stage limit
        assert manager.can_start_task("task3", stage="building") is False

        # But testing stage should still be available
        assert manager.can_start_task("task4", stage="testing") is True
