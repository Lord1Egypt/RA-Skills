"""Tests for Knowledge Memory with ChromaDB."""

import pytest
import pytest_asyncio

from agent_memory.config import KnowledgeMemoryConfig
from agent_memory.memories.knowledge_memory import KnowledgeMemory
from agent_memory.models.knowledge import Document


@pytest_asyncio.fixture
async def knowledge_memory(fake_chroma):
    config = KnowledgeMemoryConfig(chunk_size=50, chunk_overlap=10, top_k=3)
    memory = KnowledgeMemory(fake_chroma, config)
    await memory.initialize()
    return memory


class TestKnowledgeMemory:
    @pytest.mark.asyncio
    async def test_index_and_search(self, knowledge_memory):
        doc_id = await knowledge_memory.index_text(
            title="Python Guide",
            content="Python is a popular programming language used for web development, data science, and automation.",
            domain="programming",
        )
        assert doc_id is not None

        results = await knowledge_memory.search_similar("What is Python used for?")
        assert len(results) > 0
        assert any("Python" in r.content for r in results)

    @pytest.mark.asyncio
    async def test_search_with_domain_filter(self, knowledge_memory):
        await knowledge_memory.index_text(
            title="Python Guide",
            content="Python programming language for development",
            domain="programming",
        )
        await knowledge_memory.index_text(
            title="Cooking Tips",
            content="How to cook pasta with olive oil and garlic",
            domain="cooking",
        )

        results = await knowledge_memory.search_similar("programming", domain="programming")
        # All results should be from programming domain
        for r in results:
            assert r.metadata.get("domain") == "programming"

    @pytest.mark.asyncio
    async def test_delete_document(self, knowledge_memory):
        doc_id = await knowledge_memory.index_text(
            title="To Delete",
            content="This document will be deleted. It has some content.",
            domain="test",
        )

        count_before = await knowledge_memory.count()
        assert count_before > 0

        deleted = await knowledge_memory.delete_document(doc_id)
        assert deleted is True

    @pytest.mark.asyncio
    async def test_count(self, knowledge_memory):
        initial = await knowledge_memory.count()
        await knowledge_memory.index_text(
            title="Doc 1",
            content="First document content for counting test purposes",
            domain="test",
        )
        after = await knowledge_memory.count()
        assert after > initial

    @pytest.mark.asyncio
    async def test_chunk_text(self, knowledge_memory):
        chunks = knowledge_memory._chunk_text(
            "word " * 200,  # 200 words
            chunk_size=50,
            chunk_overlap=10,
        )
        assert len(chunks) > 1
        # First chunk should have ~50 words
        assert len(chunks[0].split()) <= 52  # small tolerance
