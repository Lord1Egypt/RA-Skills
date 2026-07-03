"""Background worker for async memory extraction and consolidation.

Corresponds to the async background thread in the architecture.
After each user message, this worker runs in the background to:
1. Extract structured entities (facts) from the conversation
2. Generate embeddings for episodes
3. Clean up conflicting or stale memories
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Callable, Optional

from .models import Entity, Episode, Message

logger = logging.getLogger(__name__)


class BackgroundWorker:
    """Async worker that processes conversations into structured memories.

    Uses an LLM (via callback) to extract entities and summarize episodes.
    Runs as a background task so the user never waits.
    """

    def __init__(
        self,
        entity_memory,   # EntityMemory
        episodic_memory, # EpisodicMemory
        llm_extract_fn: Optional[Callable] = None,
        embed_fn: Optional[Callable] = None,
    ) -> None:
        self._entity_memory = entity_memory
        self._episodic_memory = episodic_memory
        self._llm_extract = llm_extract_fn
        self._embed_fn = embed_fn
        self._embed_fn: Optional[Callable] = None
        self._pending_tasks: set[asyncio.Task] = set()

    async def process_turn(
        self, user_msg: Message, assistant_msg: Message
    ) -> None:
        """Process a completed turn in the background.

        Spawns both entity extraction and episode archival as concurrent tasks.
        """
        combined = f"User: {user_msg.content}\nAssistant: {assistant_msg.content}"

        task = asyncio.create_task(self._process_combined(combined))
        self._pending_tasks.add(task)
        task.add_done_callback(self._pending_tasks.discard)

    async def _process_combined(self, combined_text: str) -> None:
        """Run extraction and archival."""
        if self._llm_extract is None:
            logger.warning("No LLM extract function set; skipping background work")
            return

        try:
            # Step 1: Extract entities
            entities = await self._extract_entities(combined_text)
            for entity in entities:
                self._entity_memory.upsert(entity)

            # Step 2: Archive as episode
            episode = await self._create_episode(combined_text)
            if episode:
                try:
                    # Generate embedding for the episode
                    if self._embed_fn:
                        emb = await self._embed_fn(episode.content)
                    else:
                        emb = None
                    self._episodic_memory.add(episode, embedding=emb)
                except Exception:
                    pass  # Episodic storage is best-effort

            # Step 3: Periodic cleanup (forgetting mechanism)
            self._entity_memory.forget_low_confidence(threshold=0.2)

        except Exception as e:
            logger.error(f"Background processing failed: {e}")

    async def _extract_entities(self, text: str) -> list[Entity]:
        """Use LLM to extract structured facts from conversation."""
        prompt = f"""Extract structured user facts from this conversation.
Return ONLY a JSON array of objects with keys: key, value, evidence, confidence (0-1).
Focus on: name, preferences, fears, hobbies, occupation, relationships, important dates, goals.
If no new facts found, return empty array [].

Conversation:
{text}

JSON output:"""

        response = await self._llm_extract(prompt)
        try:
            raw = self._parse_json(response)
            entities = []
            for item in raw:
                entities.append(
                    Entity(
                        key=str(item.get("key", "")).strip(),
                        value=str(item.get("value", "")).strip(),
                        evidence=str(item.get("evidence", "")).strip(),
                        confidence=float(item.get("confidence", 0.8)),
                    )
                )
            return entities
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(f"Failed to parse entity extraction: {e}")
            return []

    async def _create_episode(self, text: str) -> Optional[Episode]:
        """Create an episodic memory chunk with auto-summary."""
        summary_prompt = f"""Summarize this conversation segment in one short sentence (max 20 words),
focusing on the key topic or emotional tone:

{text}

Summary:"""

        summary = await self._llm_extract(summary_prompt)
        summary = summary.strip().strip('"').strip("'")

        return Episode(
            id=f"ep_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}",
            content=text,
            summary=summary,
        )

    @staticmethod
    def _parse_json(text: str) -> list | dict:
        """Robust JSON parsing from LLM output."""
        text = text.strip()
        # Handle markdown code fences
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:] if len(lines) > 1 else lines
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        # Find first [ or { and last ] or }
        start = min(
            (text.find(c) for c in "[{" if text.find(c) != -1),
            default=0,
        )
        end = max(
            (text.rfind(c) for c in "]}" if text.rfind(c) != -1),
            default=len(text),
        )
        return json.loads(text[start:end + 1])
