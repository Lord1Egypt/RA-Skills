"""Concurrency Manager for Symphony

Manages concurrent builds with global and per-state limits.
Based on OpenAI's Symphony concurrency control pattern.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Set

from .state_machine import TaskState

logger = logging.getLogger('builder-agent.symphony.concurrency')


@dataclass
class ConcurrencyLimits:
    """Concurrency limits configuration"""
    max_concurrent_builds: int = 3  # Global limit
    building: int = 3               # Limit for building state
    testing: int = 5                # Limit for testing state
    fixing: int = 2                 # Limit for fixing state
    publishing: int = 3             # Limit for publishing state

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'max_concurrent_builds': self.max_concurrent_builds,
            'building': self.building,
            'testing': self.testing,
            'fixing': self.fixing,
            'publishing': self.publishing,
        }


@dataclass
class ConcurrencyState:
    """Track active tasks by state"""
    active_tasks: Set[str] = field(default_factory=set)
    state_counts: Dict[TaskState, int] = field(default_factory=lambda: {
        TaskState.CLAIMED: 0,
        TaskState.RUNNING: 0,
    })


class ConcurrencyManager:
    """Manages concurrent build execution

    Enforces:
    - Global concurrent build limit
    - Per-state limits (building, testing, fixing, publishing)
    - Tracks active tasks and enforces limits
    """

    # Pipeline stage to limit mapping
    STAGE_LIMITS = {
        'building': 'building',
        'testing': 'testing',
        'fixing': 'fixing',
        'publishing': 'publishing',
    }

    def __init__(self, limits: Optional[ConcurrencyLimits] = None):
        """Initialize concurrency manager

        Args:
            limits: Concurrency limits (uses defaults if not provided)
        """
        self.limits = limits or ConcurrencyLimits()
        self.state = ConcurrencyState()
        self.task_stages: Dict[str, str] = {}  # task_id -> stage

        logger.info(
            "Concurrency manager initialized: limits=%s",
            self.limits.to_dict()
        )

    def can_start_task(self, task_id: str, stage: str = 'building') -> bool:
        """Check if a task can start based on concurrency limits

        Args:
            task_id: Task identifier
            stage: Pipeline stage (building, testing, fixing, publishing)

        Returns:
            True if task can start, False otherwise
        """
        # Check if task is already active
        if task_id in self.state.active_tasks:
            logger.debug("Task %s is already active", task_id)
            return False

        # Check global limit
        if len(self.state.active_tasks) >= self.limits.max_concurrent_builds:
            logger.debug(
                "Global limit reached: %d/%d",
                len(self.state.active_tasks),
                self.limits.max_concurrent_builds
            )
            return False

        # Check per-stage limit
        stage_limit = self._get_stage_limit(stage)
        stage_count = self._get_stage_count(stage)

        if stage_count >= stage_limit:
            logger.debug(
                "Stage %s limit reached: %d/%d",
                stage, stage_count, stage_limit
            )
            return False

        return True

    def start_task(self, task_id: str, stage: str = 'building') -> bool:
        """Mark a task as started

        Args:
            task_id: Task identifier
            stage: Pipeline stage

        Returns:
            True if successful, False otherwise
        """
        if not self.can_start_task(task_id, stage):
            logger.warning("Cannot start task %s in stage %s", task_id, stage)
            return False

        self.state.active_tasks.add(task_id)
        self.task_stages[task_id] = stage

        # Update RUNNING state count
        self.state.state_counts[TaskState.RUNNING] += 1

        logger.info(
            "Started task %s in stage %s (active: %d/%d, stage: %d/%d)",
            task_id, stage,
            len(self.state.active_tasks),
            self.limits.max_concurrent_builds,
            self._get_stage_count(stage),
            self._get_stage_limit(stage)
        )
        return True

    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed

        Args:
            task_id: Task identifier

        Returns:
            True if successful, False otherwise
        """
        if task_id not in self.state.active_tasks:
            logger.warning("Task %s is not active", task_id)
            return False

        stage = self.task_stages.get(task_id, 'unknown')

        self.state.active_tasks.discard(task_id)
        self.task_stages.pop(task_id, None)

        # Update RUNNING state count
        self.state.state_counts[TaskState.RUNNING] = max(
            0, self.state.state_counts[TaskState.RUNNING] - 1
        )

        logger.info(
            "Completed task %s in stage %s (active: %d/%d)",
            task_id, stage,
            len(self.state.active_tasks),
            self.limits.max_concurrent_builds
        )
        return True

    def fail_task(self, task_id: str) -> bool:
        """Mark a task as failed

        Args:
            task_id: Task identifier

        Returns:
            True if successful, False otherwise
        """
        return self.complete_task(task_id)

    def get_active_count(self) -> int:
        """Get number of active tasks"""
        return len(self.state.active_tasks)

    def get_available_slots(self) -> int:
        """Get number of available build slots"""
        return max(
            0,
            self.limits.max_concurrent_builds - len(self.state.active_tasks)
        )

    def get_stage_count(self, stage: str) -> int:
        """Get number of active tasks in a specific stage"""
        return self._get_stage_count(stage)

    def get_stage_limit(self, stage: str) -> int:
        """Get limit for a specific stage"""
        return self._get_stage_limit(stage)

    def is_at_capacity(self) -> bool:
        """Check if at global capacity"""
        return len(self.state.active_tasks) >= self.limits.max_concurrent_builds

    def get_utilization(self) -> float:
        """Get current utilization as a percentage"""
        if self.limits.max_concurrent_builds == 0:
            return 0.0

        return (
            len(self.state.active_tasks) / self.limits.max_concurrent_builds
        ) * 100

    def get_active_tasks(self) -> Set[str]:
        """Get set of active task IDs"""
        return self.state.active_tasks.copy()

    def get_task_stage(self, task_id: str) -> Optional[str]:
        """Get stage for a specific task"""
        return self.task_stages.get(task_id)

    def get_statistics(self) -> Dict:
        """Get concurrency statistics"""
        return {
            'active_tasks': len(self.state.active_tasks),
            'max_concurrent_builds': self.limits.max_concurrent_builds,
            'available_slots': self.get_available_slots(),
            'utilization_percent': round(self.get_utilization(), 2),
            'by_stage': {
                stage: {
                    'active': self._get_stage_count(stage),
                    'limit': self._get_stage_limit(stage),
                }
                for stage in self.STAGE_LIMITS.keys()
            },
        }

    def update_limits(self, new_limits: ConcurrencyLimits) -> bool:
        """Update concurrency limits

        Args:
            new_limits: New limits to apply

        Returns:
            True if successful, False otherwise
        """
        old_limits = self.limits
        self.limits = new_limits

        logger.info(
            "Updated concurrency limits: %s -> %s",
            old_limits.to_dict(),
            new_limits.to_dict()
        )
        return True

    def _get_stage_limit(self, stage: str) -> int:
        """Get limit for a stage"""
        limit_key = self.STAGE_LIMITS.get(stage, 'building')
        return getattr(self.limits, limit_key, self.limits.max_concurrent_builds)

    def _get_stage_count(self, stage: str) -> int:
        """Get count of active tasks in a stage"""
        count = 0
        for task_id, task_stage in self.task_stages.items():
            if task_stage == stage:
                count += 1
        return count


class AdaptiveConcurrencyManager(ConcurrencyManager):
    """Concurrency manager with adaptive limits

    Adjusts limits based on system resources and performance.
    """

    def __init__(self, limits: Optional[ConcurrencyLimits] = None,
                 min_utilization: float = 50.0,
                 max_utilization: float = 90.0):
        """Initialize adaptive concurrency manager

        Args:
            limits: Initial concurrency limits
            min_utilization: Minimum utilization before scaling up
            max_utilization: Maximum utilization before scaling down
        """
        super().__init__(limits)
        self.min_utilization = min_utilization
        self.max_utilization = max_utilization
        self.utilization_history: list = []

    def record_utilization(self) -> float:
        """Record current utilization and return it"""
        util = self.get_utilization()
        self.utilization_history.append(util)

        # Keep only last 100 samples
        if len(self.utilization_history) > 100:
            self.utilization_history = self.utilization_history[-100:]

        return util

    def get_average_utilization(self, samples: int = 10) -> float:
        """Get average utilization over last N samples"""
        if not self.utilization_history:
            return 0.0

        recent = self.utilization_history[-samples:]
        return sum(recent) / len(recent)

    def should_scale_up(self) -> bool:
        """Check if limits should be increased"""
        avg_util = self.get_average_utilization()
        return avg_util > self.max_utilization

    def should_scale_down(self) -> bool:
        """Check if limits should be decreased"""
        avg_util = self.get_average_utilization()
        return avg_util < self.min_utilization

    def suggest_new_limits(self) -> Optional[ConcurrencyLimits]:
        """Suggest new limits based on utilization

        Returns:
            New limits if scaling is needed, None otherwise
        """
        if self.should_scale_up():
            # Increase by 1
            return ConcurrencyLimits(
                max_concurrent_builds=min(10, self.limits.max_concurrent_builds + 1),
                building=self.limits.building + 1,
                testing=self.limits.testing,
                fixing=self.limits.fixing,
                publishing=self.limits.publishing,
            )

        elif self.should_scale_down():
            # Decrease by 1 (but not below 1)
            return ConcurrencyLimits(
                max_concurrent_builds=max(1, self.limits.max_concurrent_builds - 1),
                building=max(1, self.limits.building - 1),
                testing=max(1, self.limits.testing),
                fixing=max(1, self.limits.fixing),
                publishing=max(1, self.limits.publishing),
            )

        return None

    def auto_scale(self) -> bool:
        """Automatically adjust limits based on utilization

        Returns:
            True if limits were adjusted, False otherwise
        """
        new_limits = self.suggest_new_limits()

        if new_limits:
            logger.info(
                "Auto-scaling: %s -> %s",
                self.limits.to_dict(),
                new_limits.to_dict()
            )
            self.update_limits(new_limits)
            return True

        return False
