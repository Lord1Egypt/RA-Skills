"""Pre-fetching manager for AI-Buff: anticipates likely-needed runs."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger("ghostclaw.qmd.prefetch")


class PrefetchManager:
    """
    Proactively loads related analysis runs into cache to reduce agent latency.

    Operates entirely within the asyncio event loop; no extra threads.
    Tracks pending prefetch tasks and completion stats.
    """

    def __init__(self, store: 'QMDMemoryStore'):
        """
        Initialize prefetch manager.

        Args:
            store: QMDMemoryStore instance to use for fetching runs
        """
        self.store = store
        self._pending: Set[int] = set()
        self._stats = {
            "enabled": True,
            "triggered": 0,
            "completed": 0,
            "errors": 0,
            "cache_hits_after_prefetch": 0,
        }

    def trigger(self, context: Dict[str, Any]) -> None:
        """
        Schedule prefetch tasks based on current access context.

        Fire-and-forget: schedules an async task that runs all strategies.
        Must be called from an async context (it always is from store methods).
        """
        self._stats["triggered"] += 1
        # Schedule the strategy runner as a background task
        asyncio.create_task(self._run_strategies(context))

    async def _run_strategies(self, context: Dict[str, Any]) -> None:
        """Execute all prefetch strategies and schedule fetches for discovered run IDs."""
        strategies = [
            self._prefetch_sequential,
            self._prefetch_time_window,
            self._prefetch_vibe_proximity,
            self._prefetch_same_stack,
        ]

        run_ids_to_fetch: Set[int] = set()

        for strategy in strategies:
            try:
                ids = await strategy(context)
                run_ids_to_fetch.update(ids)
            except Exception as e:
                logger.debug("Prefetch strategy %s failed: %s", strategy.__name__, e)

        # Deduplicate and filter out already pending
        new_ids = [rid for rid in run_ids_to_fetch if rid not in self._pending]
        for rid in new_ids:
            self._pending.add(rid)
            asyncio.create_task(self._prefetch_run(rid))

        logger.debug("Prefetch queued %d new runs (pending=%d)", len(new_ids), len(self._pending))

    async def _prefetch_run(self, run_id: int) -> None:
        """Background coroutine: fetch a run to warm caches."""
        try:
            run = await self.store.get_run(run_id)
            if run:
                self._stats["completed"] += 1
                logger.debug("Prefetched run %d successfully", run_id)
            else:
                logger.debug("Prefetch run %d not found", run_id)
        except Exception as e:
            logger.warning("Prefetch error for run %d: %s", run_id, e)
            self._stats["errors"] += 1
        finally:
            self._pending.discard(run_id)

    async def _prefetch_sequential(self, context: Dict[str, Any]) -> Set[int]:
        """
        Strategy A: Sequential delta pattern.
        If a run N is accessed from a repo, pre-fetch runs N-1, N-2, N+1, N+2.
        """
        repo_path = context.get("filters", {}).get("repo_path")
        if not repo_path:
            return set()

        try:
            recent = await self.store.list_runs(limit=50, repo_path=repo_path)
            if not recent:
                return set()

            # Sort by id ascending to establish sequence
            recent_sorted = sorted(recent, key=lambda r: r["id"])
            run_ids = [r["id"] for r in recent_sorted]

            current_id = context.get("run_id")
            if current_id is None or current_id not in run_ids:
                return set()

            idx = run_ids.index(current_id)
            window = context.get("prefetch_window", 2)
            start = max(0, idx - window)
            end = min(len(run_ids), idx + window + 1)
            neighbors = set(run_ids[start:end])
            neighbors.discard(current_id)
            return neighbors
        except Exception as e:
            logger.debug("Sequential prefetch failed: %s", e)
            return set()

    async def _prefetch_time_window(self, context: Dict[str, Any]) -> Set[int]:
        """
        Strategy B: Time window.
        Pre-fetch all runs within ±X hours of the current run's timestamp.
        """
        run_data = context.get("run_data")
        if not run_data:
            return set()

        timestamp_str = run_data.get("timestamp")
        if not timestamp_str:
            return set()

        try:
            current_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except ValueError:
            return set()

        hours = context.get("prefetch_hours", 24)
        delta = timedelta(hours=hours)
        start_time = current_time - delta
        end_time = current_time + delta

        repo_path = run_data.get("repo_path")
        if not repo_path:
            return set()

        try:
            recent = await self.store.list_runs(limit=100, repo_path=repo_path)
            candidates = set()
            for r in recent:
                try:
                    ts = datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
                    if start_time <= ts <= end_time:
                        candidates.add(r["id"])
                except Exception:
                    continue
            candidates.discard(run_data.get("id"))
            return candidates
        except Exception as e:
            logger.debug("Time window prefetch failed: %s", e)
            return set()

    async def _prefetch_vibe_proximity(self, context: Dict[str, Any]) -> Set[int]:
        """
        Strategy C: Vibe score proximity.
        Pre-fetch runs with vibe_score within ±delta of current run.
        """
        run_data = context.get("run_data")
        if not run_data:
            return set()

        current_score = run_data.get("vibe_score")
        if current_score is None:
            return set()

        delta = context.get("prefetch_vibe_delta", 10)
        repo_path = run_data.get("repo_path")
        if not repo_path:
            return set()

        try:
            recent = await self.store.list_runs(limit=100, repo_path=repo_path)
            candidates = set()
            for r in recent:
                score = r.get("vibe_score")
                if score is not None and abs(score - current_score) <= delta:
                    candidates.add(r["id"])
            candidates.discard(run_data.get("id"))
            return candidates
        except Exception as e:
            logger.debug("Vibe proximity prefetch failed: %s", e)
            return set()

    async def _prefetch_same_stack(self, context: Dict[str, Any]) -> Set[int]:
        """
        Strategy D: Stack correlation.
        Pre-fetch runs with matching stack from recent history.
        """
        run_data = context.get("run_data")
        if not run_data:
            return set()

        stack = run_data.get("stack")
        if not stack:
            return set()

        count = context.get("prefetch_stack_count", 5)
        repo_path = run_data.get("repo_path")
        if not repo_path:
            return set()

        try:
            recent = await self.store.list_runs(limit=100, repo_path=repo_path)
            same_stack = [r for r in recent if r.get("stack") == stack]
            same_stack.sort(key=lambda r: r["id"], reverse=True)  # newest first
            candidates = set(r["id"] for r in same_stack[:count])
            candidates.discard(run_data.get("id"))
            return candidates
        except Exception as e:
            logger.debug("Same stack prefetch failed: %s", e)
            return set()

    def get_stats(self) -> Dict[str, Any]:
        """Return prefetch statistics."""
        stats = self._stats.copy()
        stats["pending"] = len(self._pending)
        return stats

    def shutdown(self) -> None:
        """Cleanup (no-op for asyncio version, kept for compatibility)."""
        logger.debug("PrefetchManager shutdown (no-op)")
