"""Symphony Orchestrator Implementation

Main daemon loop for Symphony-style orchestration.
Based on OpenAI's Symphony orchestration specification.
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from .state_machine import (
    SymphonyStateMachine, TaskState, TerminalReason, SymphonyTask
)
from .notion_tracker import NotionTrackerAdapter
from .workspace import WorkspaceManager, WorkspaceConfig, WorkspaceHook
from .concurrency import ConcurrencyManager, ConcurrencyLimits

logger = logging.getLogger('builder-agent.symphony.orchestrator')


class SymphonyOrchestrator:
    """Main orchestrator for Symphony workflow

    Daemon loop:
    1. Reconcile running tasks (stall detection, state refresh)
    2. Poll tracker for new tasks
    3. Claim tasks within concurrency limits
    4. Process running tasks in parallel
    5. Handle retry queue with exponential backoff
    """

    # Default configuration
    DEFAULT_POLL_INTERVAL = 30  # seconds
    DEFAULT_STALL_TIMEOUT = 300  # 5 minutes
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_BACKOFF_BASE = 2

    def __init__(self, config, notion_database_id: Optional[str] = None):
        """Initialize Symphony orchestrator

        Args:
            config: Dev-factory configuration object
            notion_database_id: Notion database ID (uses config default if not provided)
        """
        self.config = config

        # Notion tracker
        database_id = notion_database_id or config.notion.database_id
        self.tracker = NotionTrackerAdapter(database_id)

        # State machine
        self.state_machine = SymphonyStateMachine()

        # Workspace manager
        workspace_config = WorkspaceConfig(
            base_dir=Path("/tmp/dev-factory-workspaces"),
            auto_cleanup=True,
            retention_hours=24,
            hooks={
                WorkspaceHook.AFTER_CREATE: [
                    "python -m venv .venv",
                ],
                WorkspaceHook.BEFORE_RUN: [
                    "rm -rf dist/ build/",
                ],
                WorkspaceHook.AFTER_RUN: [
                    "pytest --cov=. --cov-report=xml || true",
                ],
            }
        )
        self.workspace_manager = WorkspaceManager(workspace_config)

        # Concurrency manager
        concurrency_limits = ConcurrencyLimits(
            max_concurrent_builds=config.features.parallel_builds and 3 or 1,
            building=3,
            testing=5,
            fixing=2,
            publishing=3,
        )
        self.concurrency = ConcurrencyManager(concurrency_limits)

        # Retry tracking
        self.retry_backoffs: Dict[str, int] = {}

        # Orchestrator state
        self.running = False
        self.poll_interval = self.DEFAULT_POLL_INTERVAL
        self.stall_timeout = self.DEFAULT_STALL_TIMEOUT

        logger.info("Symphony orchestrator initialized")

    async def run_daemon(self):
        """Run the main daemon loop"""
        self.running = True
        logger.info("Starting Symphony daemon loop...")

        try:
            while self.running:
                # 1. Reconcile running tasks (stall detection, state refresh)
                await self._reconcile_running_tasks()

                # 2. Poll tracker for new tasks
                await self._poll_new_tasks()

                # 3. Claim tasks within concurrency limits
                await self._claim_available_tasks()

                # 4. Process running tasks in parallel
                await self._process_running_tasks()

                # 5. Handle retry queue with exponential backoff
                await self._handle_retry_queue()

                # 6. Cleanup
                self._cleanup()

                # Sleep until next poll
                await asyncio.sleep(self.poll_interval)

        except Exception as e:
            logger.error("Daemon loop error: %s", e)
            raise
        finally:
            logger.info("Symphony daemon loop stopped")

    def stop(self):
        """Stop the daemon loop"""
        logger.info("Stopping Symphony daemon...")
        self.running = False

    # ──────────────────────────────────────────────
    # Reconciliation
    # ──────────────────────────────────────────────

    async def _reconcile_running_tasks(self):
        """Reconcile running tasks (stall detection, state refresh)"""
        stale_tasks = self.state_machine.get_stale_tasks(self.stall_timeout)

        for task in stale_tasks:
            logger.warning(
                "Stale task detected: %s (stale for %ds)",
                task.task_id,
                (datetime.now() - task.last_activity).total_seconds()
            )

            # Mark as stalled
            self.state_machine.transition(
                task.task_id,
                TaskState.RELEASED,
                terminal_reason=TerminalReason.STALLED
            )

            # Update Notion
            await self._sync_task_to_notion(task)

            # Release workspace
            self.workspace_manager.remove_workspace(task.task_id)

            # Release from concurrency
            self.concurrency.complete_task(task.task_id)

    # ──────────────────────────────────────────────
    # Polling
    # ──────────────────────────────────────────────

    async def _poll_new_tasks(self):
        """Poll tracker for new tasks"""
        try:
            # Poll for unclaimed tasks
            new_tasks = self.tracker.poll_unclaimed(limit=10)

            for task in new_tasks:
                # Add to state machine if not already tracked
                if not self.state_machine.get_task(task.task_id):
                    self.state_machine.add_task(task)
                    logger.info("New task added: %s - %s", task.task_id, task.title)

        except Exception as e:
            logger.error("Failed to poll for new tasks: %s", e)

    # ──────────────────────────────────────────────
    # Task Claiming
    # ──────────────────────────────────────────────

    async def _claim_available_tasks(self):
        """Claim tasks within concurrency limits"""
        if self.concurrency.is_at_capacity():
            logger.debug("At capacity, cannot claim new tasks")
            return

        available_slots = self.concurrency.get_available_slots()
        unclaimed_tasks = self.state_machine.get_unclaimed_tasks()

        claimed = 0
        for task in unclaimed_tasks:
            if claimed >= available_slots:
                break

            # Claim task
            if await self._claim_task(task):
                claimed += 1

        if claimed > 0:
            logger.info("Claimed %d new tasks", claimed)

    async def _claim_task(self, task: SymphonyTask) -> bool:
        """Claim a single task"""
        try:
            # Update state
            if not self.state_machine.transition(task.task_id, TaskState.CLAIMED):
                logger.warning("Failed to transition task %s to CLAIMED", task.task_id)
                return False

            # Update Notion
            if not self.tracker.claim_task(task):
                logger.warning("Failed to claim task %s in Notion", task.task_id)
                # Revert state
                self.state_machine.transition(task.task_id, TaskState.UNCLAIMED)
                return False

            # Create workspace
            workspace = self.workspace_manager.create_workspace(task.task_id)
            task.workspace_path = str(workspace.path)

            # Mark as running
            self.state_machine.transition(task.task_id, TaskState.RUNNING)

            # Track in concurrency
            self.concurrency.start_task(task.task_id, stage='building')

            logger.info("Claimed and started task %s", task.task_id)
            return True

        except Exception as e:
            logger.error("Failed to claim task %s: %s", task.task_id, e)
            return False

    # ──────────────────────────────────────────────
    # Task Processing
    # ──────────────────────────────────────────────

    async def _process_running_tasks(self):
        """Process running tasks in parallel"""
        running_tasks = self.state_machine.get_tasks_in_state(TaskState.RUNNING)

        if not running_tasks:
            return

        logger.info("Processing %d running tasks", len(running_tasks))

        # Execute concurrently
        tasks_to_process = [
            self._process_task(task) for task in running_tasks
        ]

        results = await asyncio.gather(*tasks_to_process, return_exceptions=True)

        # Handle results
        for task, result in zip(running_tasks, results):
            if isinstance(result, Exception):
                logger.error("Task %s failed with exception: %s", task.task_id, result)
                await self._handle_task_failure(task, str(result))

    async def _process_task(self, task: SymphonyTask) -> Dict:
        """Process a single task

        This delegates to the existing dev-factory pipeline.
        """
        try:
            # Import existing pipeline
            from builder.pipeline import BuilderPipeline

            # Create pipeline instance
            pipeline = BuilderPipeline(self.config)

            # Get workspace
            workspace = self.workspace_manager.get_workspace(task.task_id)
            if not workspace:
                raise Exception(f"Workspace not found for task {task.task_id}")

            # Run before_run hooks
            self.workspace_manager.before_run(task.task_id)

            # Prepare idea dict
            idea = {
                'title': task.title,
                'description': task.description,
                'complexity': task.complexity,
                'url': task.metadata.get('url'),
                'source': task.metadata.get('source', 'manual'),
            }

            # Run build pipeline (async wrapper)
            result = await asyncio.to_thread(
                pipeline.run_build_pipeline,
                idea,
                workspace.path,
                resume=False
            )

            # Run after_run hooks
            self.workspace_manager.after_run(task.task_id)

            # Update task
            task.build_result = result

            # Mark as completed
            if result.get('success'):
                self.state_machine.transition(
                    task.task_id,
                    TaskState.RELEASED,
                    terminal_reason=TerminalReason.SUCCEEDED
                )
                await self._sync_task_to_notion(task)
            else:
                # Retry or fail
                await self._handle_task_failure(task, result.get('error', 'Unknown error'))

            # Release from concurrency
            self.concurrency.complete_task(task.task_id)

            return result

        except Exception as e:
            logger.error("Task %s processing error: %s", task.task_id, e)
            await self._handle_task_failure(task, str(e))
            raise

    async def _handle_task_failure(self, task: SymphonyTask, error: str):
        """Handle task failure with retry logic"""
        task.retry_count += 1
        task.retry_reason = error

        if task.retry_count < self.DEFAULT_MAX_RETRIES:
            # Queue for retry
            self.state_machine.transition(task.task_id, TaskState.RETRY_QUEUED)

            # Calculate backoff
            backoff_seconds = self.DEFAULT_RETRY_BACKOFF_BASE ** task.retry_count
            self.retry_backoffs[task.task_id] = backoff_seconds

            logger.info(
                "Task %s queued for retry (attempt %d/%d, backoff: %ds)",
                task.task_id, task.retry_count, self.DEFAULT_MAX_RETRIES, backoff_seconds
            )
        else:
            # Max retries exceeded, mark as failed
            self.state_machine.transition(
                task.task_id,
                TaskState.RELEASED,
                terminal_reason=TerminalReason.FAILED
            )
            await self._sync_task_to_notion(task)

            logger.error(
                "Task %s failed after %d retries: %s",
                task.task_id, task.retry_count, error
            )

        # Release from concurrency
        self.concurrency.complete_task(task.task_id)

    # ──────────────────────────────────────────────
    # Retry Queue
    # ──────────────────────────────────────────────

    async def _handle_retry_queue(self):
        """Handle retry queue with exponential backoff"""
        retry_tasks = self.state_machine.get_retry_queue_tasks()

        for task in retry_tasks:
            backoff_seconds = self.retry_backoffs.get(task.task_id, 0)
            time_since_last_activity = (
                datetime.now() - task.last_activity
            ).total_seconds() if task.last_activity else 0

            if time_since_last_activity >= backoff_seconds:
                # Ready to retry
                logger.info("Retrying task %s", task.task_id)

                # Reset to claimed state
                self.state_machine.transition(task.task_id, TaskState.CLAIMED)

                # Start task
                if self.concurrency.start_task(task.task_id, stage='building'):
                    self.state_machine.transition(task.task_id, TaskState.RUNNING)
                else:
                    # No capacity, keep in retry queue
                    self.state_machine.transition(task.task_id, TaskState.RETRY_QUEUED)

    # ──────────────────────────────────────────────
    # Sync and Cleanup
    # ──────────────────────────────────────────────

    async def _sync_task_to_notion(self, task: SymphonyTask):
        """Sync task state to Notion"""
        try:
            self.tracker.sync_task_state(task)
        except Exception as e:
            logger.error("Failed to sync task %s to Notion: %s", task.task_id, e)

    def _cleanup(self):
        """Periodic cleanup"""
        # Clean up old completed tasks
        self.state_machine.cleanup_old_tasks(older_than_hours=24)

        # Clean up old workspaces
        self.workspace_manager.cleanup_old_workspaces(older_than_hours=24)

    # ──────────────────────────────────────────────
    # Statistics
    # ──────────────────────────────────────────────

    def get_statistics(self) -> Dict:
        """Get orchestrator statistics"""
        return {
            'state_machine': self.state_machine.get_statistics(),
            'concurrency': self.concurrency.get_statistics(),
            'workspace': self.workspace_manager.get_statistics(),
            'running': self.running,
        }
