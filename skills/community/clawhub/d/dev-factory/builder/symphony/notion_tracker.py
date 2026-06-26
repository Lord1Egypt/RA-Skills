"""Notion Tracker Adapter for Symphony

Adapts the existing NotionSync to Symphony's tracker interface.
Maps Notion statuses to Symphony task states.
"""

import logging
import secrets
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from builder.integration.notion_sync import NotionSync
from .state_machine import TaskState, TerminalReason, SymphonyTask

logger = logging.getLogger('builder-agent.symphony.notion_tracker')


class NotionTrackerAdapter:
    """Adapter for Notion as Symphony tracker

    Maps Notion statuses to Symphony task states:
    - "아이디어" (Idea) → UNCLAIMED
    - "개발중" (Developing) → RUNNING
    - "완료" (Completed) → SUCCEEDED
    - "실패" (Failed) → FAILED
    """

    # Notion status to Symphony state mapping
    NOTION_STATUS_TO_STATE = {
        "아이디어": TaskState.UNCLAIMED,
        "개발중": TaskState.RUNNING,
        "완료": TaskState.UNCLAIMED,  # Completed tasks are terminal
        "실패": TaskState.UNCLAIMED,  # Failed tasks are terminal
    }

    # Symphony state to Notion status mapping
    STATE_TO_NOTION_STATUS = {
        TaskState.UNCLAIMED: "아이디어",
        TaskState.CLAIMED: "개발중",       # Claimed → Developing
        TaskState.RUNNING: "개발중",      # Running → Developing
        TaskState.RETRY_QUEUED: "개발중",  # Retry → still Developing
        TaskState.RELEASED: "아이디어",    # Released → back to Idea
    }

    # Terminal reason to Notion status mapping
    TERMINAL_TO_NOTION_STATUS = {
        TerminalReason.SUCCEEDED: "배포 완료",
        TerminalReason.FAILED: "실패",
        TerminalReason.TIMED_OUT: "실패",
        TerminalReason.STALLED: "실패",
    }

    def __init__(self, database_id: str, token: Optional[str] = None):
        """Initialize Notion tracker adapter

        Args:
            database_id: Notion database ID
            token: Notion API token (optional, loaded from env if not provided)
        """
        self.database_id = database_id
        self.notion_sync = NotionSync(database_id, token)
        logger.info("Notion tracker adapter initialized for database: %s", database_id)

    def poll_unclaimed(self, limit: int = 10) -> List[SymphonyTask]:
        """Poll Notion for unclaimed tasks

        Args:
            limit: Maximum number of tasks to return

        Returns:
            List of Symphony tasks in UNCLAIMED state
        """
        if not self.notion_sync.token:
            logger.warning("Notion token not configured")
            return []

        try:
            # Query for "아이디어" status
            query_data = {
                "filter": {
                    "property": "상태",
                    "status": {"equals": "아이디어"}
                },
                "page_size": limit
            }

            import json
            import urllib.request

            url = f"{self.notion_sync.api_base}/databases/{self.database_id}/query"
            req = urllib.request.Request(
                url,
                data=json.dumps(query_data).encode('utf-8'),
                headers=self.notion_sync.headers
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())

            tasks = []
            for page in result.get('results', []):
                task = self._parse_notion_page(page)
                if task:
                    tasks.append(task)

            logger.info("Polled %d unclaimed tasks from Notion", len(tasks))
            return tasks

        except Exception as e:
            logger.error("Failed to poll Notion: %s", e)
            return []

    def claim_task(self, task: SymphonyTask) -> bool:
        """Claim a task in Notion

        Updates the Notion status to "개발중" (Developing).

        Args:
            task: Task to claim

        Returns:
            True if successful, False otherwise
        """
        try:
            success = self.notion_sync.update_status(
                task.notion_page_id,
                "개발중"  # Developing
            )

            if success:
                logger.info("Claimed task %s in Notion", task.task_id)
            else:
                logger.warning("Failed to claim task %s", task.task_id)

            return success

        except Exception as e:
            logger.error("Error claiming task %s: %s", task.task_id, e)
            return False

    def complete_task(self, task: SymphonyTask, terminal_reason: TerminalReason) -> bool:
        """Mark a task as complete in Notion

        Args:
            task: Task to complete
            terminal_reason: Reason for completion

        Returns:
            True if successful, False otherwise
        """
        notion_status = self.TERMINAL_TO_NOTION_STATUS.get(terminal_reason)

        if not notion_status:
            logger.warning("No Notion status mapping for terminal reason: %s", terminal_reason)
            return False

        try:
            success = self.notion_sync.update_status(
                task.notion_page_id,
                notion_status
            )

            if success:
                logger.info(
                    "Completed task %s in Notion with status: %s",
                    task.task_id, notion_status
                )
            else:
                logger.warning("Failed to complete task %s", task.task_id)

            return success

        except Exception as e:
            logger.error("Error completing task %s: %s", task.task_id, e)
            return False

    def release_task(self, task: SymphonyTask) -> bool:
        """Release a task back to the pool

        Updates the Notion status back to "아이디어" (Idea).

        Args:
            task: Task to release

        Returns:
            True if successful, False otherwise
        """
        try:
            success = self.notion_sync.update_status(
                task.notion_page_id,
                "아이디어"  # Back to Idea
            )

            if success:
                logger.info("Released task %s in Notion", task.task_id)
            else:
                logger.warning("Failed to release task %s", task.task_id)

            return success

        except Exception as e:
            logger.error("Error releasing task %s: %s", task.task_id, e)
            return False

    def _parse_notion_page(self, page: Dict) -> Optional[SymphonyTask]:
        """Parse Notion page into Symphony task

        Args:
            page: Notion page data

        Returns:
            SymphonyTask or None if parsing fails
        """
        try:
            props = page.get('properties', {})

            # Extract title
            title = ""
            if '내용' in props and 'title' in props['내용']:
                titles = props['내용']['title']
                if titles:
                    title = titles[0].get('text', {}).get('content', '')

            # Extract description
            description = ""
            if '도구 설명' in props and 'rich_text' in props['도구 설명']:
                texts = props['도구 설명']['rich_text']
                if texts:
                    description = texts[0].get('text', {}).get('content', '')

            # Extract URL
            url = ""
            if 'URL' in props and 'url' in props['URL']:
                url = props['URL']['url']

            # Extract status
            status = "아이디어"
            if '상태' in props and 'status' in props['상태']:
                status = props['상태']['status'].get('name', '아이디어')

            # Extract tags for complexity/source
            complexity = "medium"
            source = "manual"

            if '테그' in props and 'multi_select' in props['테그']:
                tags = props['테그']['multi_select']
                for tag in tags:
                    tag_name = tag.get('name', '').lower()
                    if 'simple' in tag_name or '간단' in tag_name:
                        complexity = "simple"
                    elif 'complex' in tag_name or '복잡' in tag_name:
                        complexity = "complex"

            # Generate unique task ID
            task_id = secrets.token_hex(8)

            # Create Symphony task
            task = SymphonyTask(
                task_id=task_id,
                notion_page_id=page['id'],
                title=title,
                description=description,
                complexity=complexity,
                state=self.NOTION_STATUS_TO_STATE.get(status, TaskState.UNCLAIMED),
                metadata={
                    'url': url,
                    'source': source,
                    'notion_status': status,
                }
            )

            return task

        except Exception as e:
            logger.error("Failed to parse Notion page: %s", e)
            return None

    def get_all_tasks(self, limit: int = 100) -> List[SymphonyTask]:
        """Get all tasks from Notion

        Args:
            limit: Maximum number of tasks to return

        Returns:
            List of all Symphony tasks
        """
        if not self.notion_sync.token:
            logger.warning("Notion token not configured")
            return []

        try:
            import json
            import urllib.request

            query_data = {"page_size": limit}

            url = f"{self.notion_sync.api_base}/databases/{self.database_id}/query"
            req = urllib.request.Request(
                url,
                data=json.dumps(query_data).encode('utf-8'),
                headers=self.notion_sync.headers
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())

            tasks = []
            for page in result.get('results', []):
                task = self._parse_notion_page(page)
                if task:
                    tasks.append(task)

            logger.info("Retrieved %d tasks from Notion", len(tasks))
            return tasks

        except Exception as e:
            logger.error("Failed to get all tasks from Notion: %s", e)
            return []

    def sync_task_state(self, task: SymphonyTask) -> bool:
        """Sync task state back to Notion

        Args:
            task: Task to sync

        Returns:
            True if successful, False otherwise
        """
        # Map Symphony state to Notion status
        notion_status = self.STATE_TO_NOTION_STATUS.get(task.state)

        if not notion_status:
            # Task is terminal, use terminal reason mapping
            if task.terminal_reason:
                notion_status = self.TERMINAL_TO_NOTION_STATUS.get(task.terminal_reason)
            else:
                logger.warning("No Notion status mapping for state: %s", task.state)
                return False

        try:
            success = self.notion_sync.update_status(
                task.notion_page_id,
                notion_status
            )

            if success:
                logger.debug(
                    "Synced task %s state %s to Notion status: %s",
                    task.task_id, task.state.value, notion_status
                )

            return success

        except Exception as e:
            logger.error("Error syncing task %s: %s", task.task_id, e)
            return False

    def update_task_metadata(self, task: SymphonyTask, metadata: Dict) -> bool:
        """Update task metadata in Notion

        Args:
            task: Task to update
            metadata: Metadata to update

        Returns:
            True if successful, False otherwise
        """
        # Note: Notion API doesn't support arbitrary metadata updates
        # This is a placeholder for future implementation
        # Could add properties to Notion database schema if needed
        logger.debug("Metadata update requested for task %s: %s", task.task_id, metadata)
        return True
