# -*- coding: utf-8 -*-
"""Orchestrator -- the central RAG assembly engine.

Corresponds to the "中枢处理" in the architecture.
Assembles: System Prompt + Entity Cards + Retrieved Episodes + Recent Messages
into the final prompt sent to the LLM.
"""

from __future__ import annotations

from typing import Callable, Optional

from .models import MemoryContext, Message, MessageRole
from .short_term import ShortTermMemory
from .entity_memory import EntityMemory
from .episodic_memory import EpisodicMemory
from .background_worker import BackgroundWorker

import asyncio


DEFAULT_SYSTEM_PROMPT = """你是一个有长期记忆的AI助手，名叫阿龙。
你能记住用户告诉你的个人信息和过往对话。
当引用过去的对话时，请自然地提及，让用户感受到你记得他们。"""


class MemoryOrchestrator:
    """Central engine that coordinates all three memory layers.

    Usage:
        orchestrator = MemoryOrchestrator(
            entity_memory=entity_mem,
            episodic_memory=episodic_mem,
            embed_fn=my_embedding_function,
        )
        response = await orchestrator.chat("你好，我叫白小纯")
    """

    def __init__(
        self,
        entity_memory: EntityMemory,
        episodic_memory: EpisodicMemory,
        short_term_memory: Optional[ShortTermMemory] = None,
        embed_fn: Optional[Callable] = None,
        llm_chat_fn: Optional[Callable] = None,
        llm_extract_fn: Optional[Callable] = None,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        short_term_turns: int = 20,
        episodic_top_k: int = 3,
    ) -> None:
        self._entity_memory = entity_memory
        self._episodic_memory = episodic_memory
        self._short_term = short_term_memory or ShortTermMemory(
            max_turns=short_term_turns
        )
        self._embed_fn = embed_fn
        self._llm_chat = llm_chat_fn
        self._system_prompt = system_prompt
        self._episodic_top_k = episodic_top_k

        self._background = BackgroundWorker(
            entity_memory=entity_memory,
            episodic_memory=episodic_memory,
            llm_extract_fn=llm_extract_fn,
            embed_fn=embed_fn,
        )

    async def chat(self, user_text: str) -> str:
        """Process a user message and return the AI response.

        Flow:
        1. Assemble MemoryContext (entity cards + episodes + recent messages)
        2. Call LLM with assembled context
        3. Store the turn in short-term memory
        4. Trigger background worker for async extraction
        """
        # 1. Build context
        context = await self._assemble_context(user_text)

        # 2. Build messages and append current user query
        messages = context.build_messages()
        messages.append({"role": "user", "content": user_text})
        if self._llm_chat is None:
            raise RuntimeError("llm_chat_fn must be set before calling chat()")
        response = await self._llm_chat(messages)

        # 3. Store in short-term memory
        self._short_term.add_turn(user_text, response)

        # 4. Background async processing
        user_msg = Message(role=MessageRole.USER, content=user_text)
        assistant_msg = Message(role=MessageRole.ASSISTANT, content=response)
        asyncio.create_task(self._background.process_turn(user_msg, assistant_msg))

        return response

    async def _assemble_context(self, query: str) -> MemoryContext:
        """Assemble the full memory context for this query.

        The four components:
        1. System Prompt (base personality)
        2. Entity Cards (structured facts -- "档案袋")
        3. Retrieved Episodes (semantic search -- "模糊召回")
        4. Recent Messages (short-term -- coherence)
        """
        # Component 2: Entity cards -- all known structured facts
        entity_cards = self._entity_memory.get_all()

        # Component 3: Semantic retrieval from episodic memory
        retrieved_episodes: list = []
        if self._episodic_memory.count() > 0 and self._embed_fn is not None:
            try:
                query_embedding = await self._embed_fn(query)
                retrieved_episodes = self._episodic_memory.query(
                    query_text=query,
                    n_results=self._episodic_top_k,
                    query_embedding=query_embedding,
                )
            except Exception:
                pass  # Graceful degradation if vector search fails

        # Component 4: Recent conversation
        recent = self._short_term.get_recent()

        return MemoryContext(
            system_prompt=self._system_prompt,
            entity_cards=entity_cards,
            retrieved_episodes=retrieved_episodes,
            recent_messages=recent,
        )

    def get_entity(self, key: str):
        """Direct lookup of a structured fact."""
        return self._entity_memory.get(key)

    def get_all_entities(self):
        """Return all structured facts about the user."""
        return self._entity_memory.get_all()

    def clear_short_term(self) -> None:
        self._short_term.clear()
