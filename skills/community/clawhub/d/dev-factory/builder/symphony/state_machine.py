"""Symphony State Machine Implementation

Manages task lifecycle through states with proper transitions and terminal states.
Based on OpenAI's Symphony orchestration specification.
"""

import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field

logger = logging.getLogger('builder-agent.symphony.state_machine')


class TaskState(Enum):
    """Task states in Symphony workflow"""
    UNCLAIMED = "unclaimed"       # In Notion queue (status: "아이디어")
    CLAIMED = "claimed"           # Reserved by orchestrator
    RUNNING = "running"           # Agent executing (status: "개발중")
    RETRY_QUEUED = "retry_queued" # Waiting for retry
    RELEASED = "released"         # Worker gave up


class TerminalReason(Enum):
    """Reasons for terminal task states"""
    SUCCEEDED = "succeeded"       # → Notion: "완료"
    FAILED = "failed"             # → Notion: "실패"
    TIMED_OUT = "timed_out"
    STALLED = "stalled"


@dataclass
class SymphonyTask:
    """A task in the Symphony workflow"""
    task_id: str                  # Unique task identifier
    notion_page_id: str           # Notion page ID
    title: str                    # Project title
    description: str              # Project description
    complexity: str = "medium"    # simple, medium, complex
    state: TaskState = TaskState.UNCLAIMED
    claimed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    retry_count: int = 0
    retry_reason: Optional[str] = None
    terminal_reason: Optional[TerminalReason] = None
    metadata: Dict = field(default_factory=dict)
    workspace_path: Optional[str] = None
    build_result: Optional[Dict] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'task_id': self.task_id,
            'notion_page_id': self.notion_page_id,
            'title': self.title,
            'description': self.description,
            'complexity': self.complexity,
            'state': self.state.value,
            'claimed_at': self.claimed_at.isoformat() if self.claimed_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'retry_count': self.retry_count,
            'retry_reason': self.retry_reason,
            'terminal_reason': self.terminal_reason.value if self.terminal_reason else None,
            'metadata': self.metadata,
            'workspace_path': self.workspace_path,
            'build_result': self.build_result,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'SymphonyTask':
        """Create from dictionary"""
        task = cls(
            task_id=data['task_id'],
            notion_page_id=data['notion_page_id'],
            title=data['title'],
            description=data['description'],
            complexity=data.get('complexity', 'medium'),
            state=TaskState(data.get('state', TaskState.UNCLAIMED.value)),
            retry_count=data.get('retry_count', 0),
            metadata=data.get('metadata', {}),
            workspace_path=data.get('workspace_path'),
            build_result=data.get('build_result'),
        )

        # Parse datetime fields
        for field_name in ['claimed_at', 'started_at', 'completed_at', 'last_activity']:
            if data.get(field_name):
                setattr(task, field_name, datetime.fromisoformat(data[field_name]))

        # Parse terminal reason
        if data.get('terminal_reason'):
            task.terminal_reason = TerminalReason(data['terminal_reason'])

        task.retry_reason = data.get('retry_reason')

        return task

    def is_terminal(self) -> bool:
        """Check if task is in terminal state"""
        return self.terminal_reason is not None

    def is_active(self) -> bool:
        """Check if task is currently active (claimed or running)"""
        return self.state in [TaskState.CLAIMED, TaskState.RUNNING]

    def is_stale(self, timeout_seconds: int = 300) -> bool:
        """Check if task has stalled (no recent activity)"""
        if not self.last_activity:
            return False

        if not self.is_active():
            return False

        elapsed = (datetime.now() - self.last_activity).total_seconds()
        return elapsed > timeout_seconds


class SymphonyStateMachine:
    """Manages state transitions for Symphony tasks"""

    # Valid state transitions
    TRANSITIONS = {
        TaskState.UNCLAIMED: [TaskState.CLAIMED, TaskState.RELEASED],
        TaskState.CLAIMED: [TaskState.RUNNING, TaskState.RELEASED, TaskState.RETRY_QUEUED],
        TaskState.RUNNING: [TaskState.RETRY_QUEUED, TaskState.RELEASED],
        TaskState.RETRY_QUEUED: [TaskState.CLAIMED, TaskState.RELEASED],
        TaskState.RELEASED: [TaskState.CLAIMED],
    }

    def __init__(self):
        """Initialize state machine"""
        self.tasks: Dict[str, SymphonyTask] = {}
        self.state_index: Dict[TaskState, Set[str]] = {
            state: set() for state in TaskState
        }

    def add_task(self, task: SymphonyTask) -> bool:
        """Add a new task to the state machine"""
        if task.task_id in self.tasks:
            logger.warning("Task %s already exists", task.task_id)
            return False

        self.tasks[task.task_id] = task
        self.state_index[task.state].add(task.task_id)
        logger.info("Added task %s in state %s", task.task_id, task.state.value)
        return True

    def get_task(self, task_id: str) -> Optional[SymphonyTask]:
        """Get task by ID"""
        return self.tasks.get(task_id)

    def transition(self, task_id: str, new_state: TaskState,
                   terminal_reason: Optional[TerminalReason] = None,
                   metadata_update: Optional[Dict] = None) -> bool:
        """Transition task to new state"""
        task = self.get_task(task_id)
        if not task:
            logger.warning("Task %s not found", task_id)
            return False

        # Check if transition is valid
        if new_state not in self.TRANSITIONS.get(task.state, []):
            logger.warning(
                "Invalid transition: %s -> %s for task %s",
                task.state.value, new_state.value, task_id
            )
            return False

        # Update state index
        self.state_index[task.state].discard(task_id)
        self.state_index[new_state].add(task_id)

        # Update task
        old_state = task.state
        task.state = new_state
        task.last_activity = datetime.now()

        # Set timestamps
        if new_state == TaskState.CLAIMED and not task.claimed_at:
            task.claimed_at = datetime.now()
        elif new_state == TaskState.RUNNING and not task.started_at:
            task.started_at = datetime.now()
        elif terminal_reason and not task.completed_at:
            task.completed_at = datetime.now()
            task.terminal_reason = terminal_reason

        # Update metadata
        if metadata_update:
            task.metadata.update(metadata_update)

        logger.info(
            "Task %s transitioned: %s -> %s",
            task_id, old_state.value, new_state.value
        )
        return True

    def get_tasks_in_state(self, state: TaskState) -> List[SymphonyTask]:
        """Get all tasks in a specific state"""
        task_ids = self.state_index.get(state, set())
        return [self.tasks[tid] for tid in task_ids if tid in self.tasks]

    def get_active_tasks(self) -> List[SymphonyTask]:
        """Get all active tasks (claimed or running)"""
        active = []
        for state in [TaskState.CLAIMED, TaskState.RUNNING]:
            active.extend(self.get_tasks_in_state(state))
        return active

    def get_stale_tasks(self, timeout_seconds: int = 300) -> List[SymphonyTask]:
        """Get tasks that have stalled"""
        return [
            task for task in self.get_active_tasks()
            if task.is_stale(timeout_seconds)
        ]

    def get_unclaimed_tasks(self) -> List[SymphonyTask]:
        """Get all unclaimed tasks"""
        return self.get_tasks_in_state(TaskState.UNCLAIMED)

    def get_retry_queue_tasks(self) -> List[SymphonyTask]:
        """Get tasks waiting for retry"""
        return self.get_tasks_in_state(TaskState.RETRY_QUEUED)

    def count_by_state(self) -> Dict[TaskState, int]:
        """Count tasks by state"""
        return {
            state: len(self.state_index[state])
            for state in TaskState
        }

    def remove_task(self, task_id: str) -> bool:
        """Remove task from state machine"""
        task = self.get_task(task_id)
        if not task:
            return False

        self.state_index[task.state].discard(task_id)
        del self.tasks[task_id]
        logger.info("Removed task %s", task_id)
        return True

    def cleanup_old_tasks(self, older_than_hours: int = 24) -> int:
        """Remove completed tasks older than specified hours"""
        cutoff = datetime.now() - timedelta(hours=older_than_hours)
        to_remove = []

        for task_id, task in self.tasks.items():
            if task.completed_at and task.completed_at < cutoff:
                to_remove.append(task_id)

        for task_id in to_remove:
            self.remove_task(task_id)

        logger.info("Cleaned up %d old tasks", len(to_remove))
        return len(to_remove)

    def get_statistics(self) -> Dict:
        """Get state machine statistics"""
        active = self.get_active_tasks()
        stale = self.get_stale_tasks()

        return {
            'total_tasks': len(self.tasks),
            'by_state': {
                state.value: len(self.state_index[state])
                for state in TaskState
            },
            'active_tasks': len(active),
            'stale_tasks': len(stale),
            'retry_queue_size': len(self.get_retry_queue_tasks()),
        }
