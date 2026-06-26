"""Unit tests for Symphony State Machine"""

import pytest
from datetime import datetime, timedelta

from builder.symphony.state_machine import (
    TaskState, TerminalReason, SymphonyTask, SymphonyStateMachine
)


class TestTaskState:
    """Test TaskState enum"""

    def test_state_values(self):
        """Test state enum values"""
        assert TaskState.UNCLAIMED.value == "unclaimed"
        assert TaskState.CLAIMED.value == "claimed"
        assert TaskState.RUNNING.value == "running"
        assert TaskState.RETRY_QUEUED.value == "retry_queued"
        assert TaskState.RELEASED.value == "released"


class TestTerminalReason:
    """Test TerminalReason enum"""

    def test_reason_values(self):
        """Test terminal reason enum values"""
        assert TerminalReason.SUCCEEDED.value == "succeeded"
        assert TerminalReason.FAILED.value == "failed"
        assert TerminalReason.TIMED_OUT.value == "timed_out"
        assert TerminalReason.STALLED.value == "stalled"


class TestSymphonyTask:
    """Test SymphonyTask dataclass"""

    def test_task_creation(self):
        """Test task creation"""
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project"
        )

        assert task.task_id == "test123"
        assert task.notion_page_id == "page123"
        assert task.title == "Test Project"
        assert task.description == "A test project"
        assert task.state == TaskState.UNCLAIMED
        assert task.retry_count == 0

    def test_task_to_dict(self):
        """Test task serialization to dict"""
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project",
            complexity="simple"
        )

        task_dict = task.to_dict()

        assert task_dict['task_id'] == "test123"
        assert task_dict['notion_page_id'] == "page123"
        assert task_dict['title'] == "Test Project"
        assert task_dict['complexity'] == "simple"
        assert task_dict['state'] == "unclaimed"

    def test_task_from_dict(self):
        """Test task deserialization from dict"""
        task_dict = {
            'task_id': 'test123',
            'notion_page_id': 'page123',
            'title': 'Test Project',
            'description': 'A test project',
            'complexity': 'simple',
            'state': 'unclaimed',
            'retry_count': 0,
            'metadata': {},
        }

        task = SymphonyTask.from_dict(task_dict)

        assert task.task_id == "test123"
        assert task.notion_page_id == "page123"
        assert task.title == "Test Project"
        assert task.complexity == "simple"

    def test_task_is_terminal(self):
        """Test is_terminal method"""
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project"
        )

        assert not task.is_terminal()

        task.terminal_reason = TerminalReason.SUCCEEDED
        assert task.is_terminal()

    def test_task_is_active(self):
        """Test is_active method"""
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project",
            state=TaskState.UNCLAIMED
        )

        assert not task.is_active()

        task.state = TaskState.CLAIMED
        assert task.is_active()

        task.state = TaskState.RUNNING
        assert task.is_active()

    def test_task_is_stale(self):
        """Test is_stale method"""
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project",
            state=TaskState.RUNNING
        )

        # No activity yet, not stale
        assert not task.is_stale()

        # Set recent activity
        task.last_activity = datetime.now()
        assert not task.is_stale()

        # Set old activity (simulate 10 minutes ago)
        task.last_activity = datetime.now() - timedelta(minutes=10)
        assert task.is_stale(timeout_seconds=300)  # 5 minutes


class TestSymphonyStateMachine:
    """Test SymphonyStateMachine"""

    def test_state_machine_initialization(self):
        """Test state machine initialization"""
        sm = SymphonyStateMachine()

        assert len(sm.tasks) == 0
        assert len(sm.state_index[TaskState.UNCLAIMED]) == 0

    def test_add_task(self):
        """Test adding task to state machine"""
        sm = SymphonyStateMachine()
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project"
        )

        result = sm.add_task(task)

        assert result is True
        assert task.task_id in sm.tasks
        assert task.task_id in sm.state_index[TaskState.UNCLAIMED]

    def test_add_duplicate_task(self):
        """Test adding duplicate task"""
        sm = SymphonyStateMachine()
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project"
        )

        sm.add_task(task)
        result = sm.add_task(task)

        assert result is False

    def test_get_task(self):
        """Test getting task by ID"""
        sm = SymphonyStateMachine()
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project"
        )

        sm.add_task(task)
        retrieved = sm.get_task("test123")

        assert retrieved is not None
        assert retrieved.task_id == "test123"

    def test_get_nonexistent_task(self):
        """Test getting nonexistent task"""
        sm = SymphonyStateMachine()
        retrieved = sm.get_task("nonexistent")

        assert retrieved is None

    def test_valid_transition(self):
        """Test valid state transition"""
        sm = SymphonyStateMachine()
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project",
            state=TaskState.UNCLAIMED
        )

        sm.add_task(task)
        result = sm.transition("test123", TaskState.CLAIMED)

        assert result is True
        assert task.state == TaskState.CLAIMED
        assert task.claimed_at is not None

    def test_invalid_transition(self):
        """Test invalid state transition"""
        sm = SymphonyStateMachine()
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project",
            state=TaskState.UNCLAIMED
        )

        sm.add_task(task)
        # Direct jump from UNCLAIMED to RETRY_QUEUED is invalid
        result = sm.transition("test123", TaskState.RETRY_QUEUED)

        assert result is False
        assert task.state == TaskState.UNCLAIMED

    def test_transition_with_terminal_reason(self):
        """Test transition with terminal reason"""
        sm = SymphonyStateMachine()
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project",
            state=TaskState.RUNNING
        )

        sm.add_task(task)
        result = sm.transition(
            "test123",
            TaskState.RELEASED,
            terminal_reason=TerminalReason.SUCCEEDED
        )

        assert result is True
        assert task.terminal_reason == TerminalReason.SUCCEEDED
        assert task.completed_at is not None

    def test_get_tasks_in_state(self):
        """Test getting tasks by state"""
        sm = SymphonyStateMachine()

        task1 = SymphonyTask(
            task_id="test1",
            notion_page_id="page1",
            title="Test 1",
            description="Test 1",
            state=TaskState.UNCLAIMED
        )

        task2 = SymphonyTask(
            task_id="test2",
            notion_page_id="page2",
            title="Test 2",
            description="Test 2",
            state=TaskState.RUNNING
        )

        sm.add_task(task1)
        sm.add_task(task2)

        unclaimed = sm.get_tasks_in_state(TaskState.UNCLAIMED)
        running = sm.get_tasks_in_state(TaskState.RUNNING)

        assert len(unclaimed) == 1
        assert len(running) == 1
        assert unclaimed[0].task_id == "test1"
        assert running[0].task_id == "test2"

    def test_get_active_tasks(self):
        """Test getting active tasks"""
        sm = SymphonyStateMachine()

        task1 = SymphonyTask(
            task_id="test1",
            notion_page_id="page1",
            title="Test 1",
            description="Test 1",
            state=TaskState.CLAIMED
        )

        task2 = SymphonyTask(
            task_id="test2",
            notion_page_id="page2",
            title="Test 2",
            description="Test 2",
            state=TaskState.RUNNING
        )

        task3 = SymphonyTask(
            task_id="test3",
            notion_page_id="page3",
            title="Test 3",
            description="Test 3",
            state=TaskState.UNCLAIMED
        )

        sm.add_task(task1)
        sm.add_task(task2)
        sm.add_task(task3)

        active = sm.get_active_tasks()

        assert len(active) == 2
        assert task1.task_id in [t.task_id for t in active]
        assert task2.task_id in [t.task_id for t in active]

    def test_remove_task(self):
        """Test removing task"""
        sm = SymphonyStateMachine()
        task = SymphonyTask(
            task_id="test123",
            notion_page_id="page123",
            title="Test Project",
            description="A test project"
        )

        sm.add_task(task)
        assert task.task_id in sm.tasks

        result = sm.remove_task("test123")

        assert result is True
        assert task.task_id not in sm.tasks

    def test_count_by_state(self):
        """Test counting tasks by state"""
        sm = SymphonyStateMachine()

        for i in range(3):
            task = SymphonyTask(
                task_id=f"test{i}",
                notion_page_id=f"page{i}",
                title=f"Test {i}",
                description=f"Test {i}",
                state=TaskState.UNCLAIMED
            )
            sm.add_task(task)

        # Transition one to CLAIMED
        sm.transition("test0", TaskState.CLAIMED)

        counts = sm.count_by_state()

        assert counts[TaskState.UNCLAIMED] == 2
        assert counts[TaskState.CLAIMED] == 1

    def test_get_statistics(self):
        """Test getting statistics"""
        sm = SymphonyStateMachine()

        task1 = SymphonyTask(
            task_id="test1",
            notion_page_id="page1",
            title="Test 1",
            description="Test 1",
            state=TaskState.CLAIMED
        )

        task2 = SymphonyTask(
            task_id="test2",
            notion_page_id="page2",
            title="Test 2",
            description="Test 2",
            state=TaskState.RUNNING
        )

        sm.add_task(task1)
        sm.add_task(task2)

        stats = sm.get_statistics()

        assert stats['total_tasks'] == 2
        assert stats['active_tasks'] == 2
        assert stats['stale_tasks'] == 0
