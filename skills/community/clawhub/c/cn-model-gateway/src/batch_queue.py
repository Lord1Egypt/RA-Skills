"""Batch task queue with SQLite WAL + background worker.

v1.8.0: batch_submit / batch_result tool pair.
Tasks are persisted in SQLite, executed sequentially by a background thread
with hardware-aware concurrency control. Failed tasks auto-retry once with
a backup provider.
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .monitor import compute_concurrency_limit, get_hardware_info


TASK_STATUS_PENDING = "pending"
TASK_STATUS_RUNNING = "running"
TASK_STATUS_DONE = "done"
TASK_STATUS_FAILED = "failed"
TASK_STATUS_RETRY = "retry"


class BatchQueue:
    """SQLite-backed task queue for batch operations."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = str(Path.home() / ".cn-model-gateway" / "batch.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
        self._hardware = get_hardware_info()
        self._concurrency_limit = compute_concurrency_limit(self._hardware)

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS batch_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    priority INTEGER NOT NULL DEFAULT 5,
                    total_count INTEGER NOT NULL DEFAULT 0,
                    done_count INTEGER NOT NULL DEFAULT 0,
                    error_count INTEGER NOT NULL DEFAULT 0,
                    items TEXT NOT NULL DEFAULT '[]',
                    results TEXT NOT NULL DEFAULT '[]',
                    errors TEXT NOT NULL DEFAULT '[]'
                )
            """)
            conn.commit()

    def create_task(self, items: List[Dict[str, Any]], priority: int = 5) -> str:
        """Create a new batch task. Returns task_id."""
        task_id = f"batch_{int(time.time() * 1000)}"
        now = time.time()
        items_json = json.dumps(items, ensure_ascii=False)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO batch_tasks "
                "(task_id, created_at, updated_at, status, priority, total_count, items) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (task_id, now, now, TASK_STATUS_PENDING, priority, len(items), items_json),
            )
            conn.commit()
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status and results."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM batch_tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
            if not row:
                return None
            items = json.loads(row["items"])
            results = json.loads(row["results"])
            errors = json.loads(row["errors"])
            # Build per-item status list
            item_status = []
            for i, item in enumerate(items):
                status = "pending"
                result_val = results[i] if i < len(results) else None
                error_val = errors[i] if i < len(errors) else None
                if error_val and result_val is None:
                    status = "failed"
                elif result_val:
                    status = "done"
                else:
                    # Check if currently running (between done_count and total)
                    if i < row["done_count"]:
                        status = "running"
                item_status.append({
                    "index": i,
                    "tool": item.get("tool", "ask_model"),
                    "arguments": item.get("args", {}),
                    "status": status,
                    "result": result_val,
                    "error": error_val,
                    "retried": item.get("_retry", False),
                })
            return {
                "task_id": row["task_id"],
                "status": row["status"],
                "priority": row["priority"],
                "total": row["total_count"],
                "done": row["done_count"],
                "errors": row["error_count"],
                "items": items,
                "item_status": item_status,
                "results": results,
                "error_details": errors,
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }

    def claim_next_item(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Atomically claim the next pending item. Returns item dict or None."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT items, done_count FROM batch_tasks WHERE task_id = ?",
                (task_id,),
            ).fetchone()
            if not row:
                return None
            items = json.loads(row["items"])
            done = row["done_count"]
            if done >= len(items):
                return None
            item = items[done]
            item["_index"] = done
            # Mark as running
            conn.execute(
                "UPDATE batch_tasks SET status = ?, updated_at = ? WHERE task_id = ?",
                (TASK_STATUS_RUNNING, time.time(), task_id),
            )
            conn.commit()
            return item

    def complete_item(
        self,
        task_id: str,
        index: int,
        result: Any,
        error: Optional[str] = None,
    ) -> None:
        """Record completion of a single item."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM batch_tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
            if not row:
                return
            results = json.loads(row["results"])
            errors = json.loads(row["errors"])
            # Pad results list if needed
            while len(results) <= index:
                results.append(None)
            results[index] = result
            if error:
                while len(errors) <= index:
                    errors.append(None)
                errors[index] = error
                conn.execute(
                    "UPDATE batch_tasks SET results = ?, errors = ?, "
                    "done_count = done_count + 1, error_count = error_count + 1, "
                    "updated_at = ? WHERE task_id = ?",
                    (json.dumps(results, ensure_ascii=False),
                     json.dumps(errors, ensure_ascii=False),
                     time.time(), task_id),
                )
            else:
                conn.execute(
                    "UPDATE batch_tasks SET results = ?, "
                    "done_count = done_count + 1, "
                    "updated_at = ? WHERE task_id = ?",
                    (json.dumps(results, ensure_ascii=False),
                     time.time(), task_id),
                )
            conn.commit()

    def finish_task(self, task_id: str) -> None:
        """Mark task as done."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE batch_tasks SET status = ?, updated_at = ? WHERE task_id = ?",
                (TASK_STATUS_DONE, time.time(), task_id),
            )
            conn.commit()

    def fail_task(self, task_id: str, error: str) -> None:
        """Mark task as failed."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE batch_tasks SET status = ?, errors = ?, updated_at = ? "
                "WHERE task_id = ?",
                (TASK_STATUS_FAILED, json.dumps([error], ensure_ascii=False),
                 time.time(), task_id),
            )
            conn.commit()

    def list_items(self, task_id: str) -> List[Dict[str, Any]]:
        """List all items for a task, including their individual status."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT items, results, errors FROM batch_tasks WHERE task_id = ?",
                (task_id,)
            ).fetchone()
            if not row:
                return []
            items = json.loads(row["items"])
            results = json.loads(row["results"])
            errors = json.loads(row["errors"])
            result_list = []
            for i, item in enumerate(items):
                status = "pending"
                result_val = results[i] if i < len(results) else None
                error_val = errors[i] if i < len(errors) else None
                if error_val and result_val is None:
                    status = "failed"
                elif result_val:
                    status = "done"
                else:
                    # Check if currently running
                    done_count = conn.execute(
                        "SELECT done_count FROM batch_tasks WHERE task_id = ?",
                        (task_id,)
                    ).fetchone()[0]
                    if i < done_count:
                        status = "running"
                result_list.append({
                    "index": i,
                    "tool": item.get("tool", "ask_model"),
                    "arguments": item.get("args", {}),
                    "status": status,
                    "result": result_val,
                    "error": error_val,
                    "retried": item.get("_retry", False),
                })
            return result_list

    def list_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent tasks."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT task_id, status, total_count, done_count, error_count, "
                "created_at, updated_at FROM batch_tasks "
                "ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]


class BatchWorker:
    """Background worker that processes batch tasks sequentially."""

    def __init__(
        self,
        queue: BatchQueue,
        router: Any,
        monitor: Any,
        max_concurrency: Optional[int] = None,
    ) -> None:
        self.queue = queue
        self.router = router
        self.monitor = monitor
        self._max_concurrency = max_concurrency or queue._concurrency_limit
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._active_tasks: Dict[str, int] = {}  # task_id -> active count

    def start(self) -> None:
        """Start the background worker thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the background worker."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def is_running(self) -> bool:
        return self._running

    def _run(self) -> None:
        """Main loop: process pending tasks."""
        while self._running:
            try:
                self._process_pending_tasks()
            except Exception:
                pass
            time.sleep(1)

    def _process_pending_tasks(self) -> None:
        """Find and process pending tasks."""
        # Get pending tasks, ordered by priority (lower = higher priority)
        with sqlite3.connect(self.queue.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT task_id, total_count, done_count FROM batch_tasks "
                "WHERE status IN (?, ?) ORDER BY priority ASC, created_at ASC",
                (TASK_STATUS_PENDING, TASK_STATUS_RUNNING),
            ).fetchall()
            pending_tasks = [dict(r) for r in rows]

        for task_row in pending_tasks:
            if not self._running:
                break
            task_id = task_row["task_id"]
            self._process_task(task_id)

    def _process_task(self, task_id: str) -> None:
        """Process a single batch task."""
        while self._running:
            # Check concurrency
            active = self._active_tasks.get(task_id, 0)
            if active >= self._max_concurrency:
                time.sleep(0.5)
                continue

            # Claim next item
            item = self.queue.claim_next_item(task_id)
            if item is None:
                # Task complete
                self.queue.finish_task(task_id)
                self._active_tasks.pop(task_id, None)
                break

            # Execute item in thread pool
            self._active_tasks[task_id] = active + 1
            t = threading.Thread(
                target=self._execute_item,
                args=(task_id, item),
                daemon=True,
            )
            t.start()

    def _execute_item(self, task_id: str, item: Dict[str, Any]) -> None:
        """Execute a single batch item with failover + retry."""
        index = item.get("_index", 0)
        tool_name = item.get("tool", "ask_model")
        args = item.get("args", {})
        provider = args.get("provider")

        try:
            # Use router to call the provider
            if tool_name == "ask_model":
                from .adapters.base import ChatMessage
                question = args.get("question", "")
                msgs = [ChatMessage(role="user", content=question)]
                resp = self.router.chat(msgs, provider=provider)
                result = {
                    "content": resp.content,
                    "model": resp.model,
                    "provider": resp.provider,
                    "duration_ms": resp.duration_ms,
                    "usage": resp.usage,
                }
            elif tool_name == "describe_image":
                # Vision task
                adapter = None
                if provider:
                    adapter = self.router.get_adapter(provider)
                else:
                    available = self.router.list_available()
                    if available:
                        adapter = self.router.get_adapter(available[0])
                if adapter:
                    resp = adapter.describe_image(
                        args.get("image", ""),
                        args.get("prompt", "请描述这张图片"),
                    )
                    result = {
                        "content": resp.content,
                        "model": resp.model,
                        "provider": resp.provider,
                    }
                else:
                    result = None
                    raise RuntimeError("No vision provider available")
            else:
                raise ValueError(f"Unsupported batch tool: {tool_name}")

            self.queue.complete_item(task_id, index, result)
        except Exception as e:
            # Retry once without explicit provider (auto-failover)
            if provider and item.get("_retry", False):
                # Already retried, mark as failed
                self.queue.complete_item(task_id, index, None, error=str(e))
            elif provider and not item.get("_retry", False):
                # Retry with auto-selected provider
                item["_retry"] = True
                args["provider"] = None
                item["args"] = args
                self._execute_item(task_id, item)
                return
            else:
                self.queue.complete_item(task_id, index, None, error=str(e))
        finally:
            active = self._active_tasks.get(task_id, 1)
            if active <= 1:
                self._active_tasks.pop(task_id, None)
            else:
                self._active_tasks[task_id] = active - 1

    @property
    def max_concurrency(self) -> int:
        return self._max_concurrency
