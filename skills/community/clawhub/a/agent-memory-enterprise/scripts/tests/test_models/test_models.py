"""Tests for Pydantic models."""

import pytest
from agent_memory.models.base import MemoryType, TaskStatus, StepStatus


def test_memory_type_values():
    assert MemoryType.CONTEXT == "context"
    assert MemoryType.TASK == "task"
    assert MemoryType.USER == "user"
    assert MemoryType.KNOWLEDGE == "knowledge"
    assert MemoryType.EXPERIENCE == "experience"


def test_task_status_values():
    assert TaskStatus.PENDING == "pending"
    assert TaskStatus.IN_PROGRESS == "in_progress"
    assert TaskStatus.COMPLETED == "completed"
    assert TaskStatus.FAILED == "failed"
    assert TaskStatus.ARCHIVED == "archived"


def test_step_status_values():
    assert StepStatus.PENDING == "pending"
    assert StepStatus.RUNNING == "running"
    assert StepStatus.DONE == "done"


def test_context_message():
    from agent_memory.models.context import ContextMessage, MessageRole
    msg = ContextMessage(role=MessageRole.USER, content="Hello", token_count=5)
    assert msg.role == MessageRole.USER
    assert msg.content == "Hello"
    assert msg.token_count == 5
    assert msg.id is not None


def test_conversation_window():
    from agent_memory.models.context import ConversationWindow, ContextMessage, MessageRole
    window = ConversationWindow(session_id="test_session")
    assert window.session_id == "test_session"
    assert len(window.messages) == 0
    assert window.total_tokens == 0


def test_task_state():
    from agent_memory.models.task import TaskState, TaskStep
    task = TaskState(
        goal="Test goal",
        steps=[
            TaskStep(step_index=0, description="Step 1"),
            TaskStep(step_index=1, description="Step 2"),
        ],
    )
    assert task.goal == "Test goal"
    assert len(task.steps) == 2
    assert task.status == TaskStatus.PENDING
    assert task.task_id is not None


def test_user_profile():
    from agent_memory.models.user import UserProfile, UserPreference
    profile = UserProfile(user_id="user_123")
    assert profile.user_id == "user_123"
    assert len(profile.preferences) == 0

    pref = UserPreference(key="language", value="zh-CN", source="explicit")
    assert pref.key == "language"
    assert pref.value == "zh-CN"
    assert pref.confidence == 1.0


def test_document_and_chunk():
    from agent_memory.models.knowledge import Document, DocumentChunk
    doc = Document(title="Test Doc", content="Some content", domain="test")
    assert doc.title == "Test Doc"
    assert doc.domain == "test"

    chunk = DocumentChunk(document_id=doc.id, chunk_index=0, content="Some content")
    assert chunk.document_id == doc.id


def test_experience_record():
    from agent_memory.models.experience import ExperienceRecord, ExperienceOutcome
    record = ExperienceRecord(
        task_type="analysis",
        goal_description="Test analysis",
        approach="manual review",
        outcome=ExperienceOutcome.SUCCESS,
        duration_seconds=120.0,
    )
    assert record.outcome == ExperienceOutcome.SUCCESS
    assert record.task_type == "analysis"


def test_importance_score():
    from agent_memory.models.scoring import ImportanceScore, ScoreComponents
    score = ImportanceScore(
        memory_id="test",
        memory_type=MemoryType.CONTEXT,
        total=0.85,
        components=ScoreComponents(relevance=0.9, recency=0.8, frequency=0.7, explicit_rating=0.9),
    )
    assert score.total == 0.85
    assert score.components.relevance == 0.9
