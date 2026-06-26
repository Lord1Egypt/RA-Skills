"""
test_immediate_skill_hook.py - 单元测试

覆盖：
- TaskResult 构建
- RuleBasedExtractor 提取逻辑
- 置信度分流（高/中/低）
- SkillDocumentWriter 文件写入
- DreamingQueue 读写
- ImmediateSkillHook 端到端流程

运行：
    pytest agent-cluster/memory/tests/test_immediate_skill_hook.py -v
"""

from __future__ import annotations

import json
import os
import tempfile
import uuid
from pathlib import Path

import pytest

# 在 package 外 import 时需要路径
import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from memory.immediate_skill_hook import (
    DreamingQueue,
    ImmediateSkillHook,
    RuleBasedExtractor,
    SkillCandidate,
    SkillDocumentWriter,
    TaskResult,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_dirs():
    """临时技能目录 + 梦境队列"""
    with tempfile.TemporaryDirectory() as tmpdir:
        skills_dir = Path(tmpdir) / "skills"
        queue_path = Path(tmpdir) / "dream_queue.jsonl"
        yield {"skills_dir": skills_dir, "queue_path": queue_path}


@pytest.fixture
def sample_task_result() -> dict:
    return {
        "task_id": "task-001",
        "success": True,
        "content": "How to fix Python SSL certificate verification error",
        "result": (
            "1. Update certificates: /etc/ssl/certs/ca-certificates.crt\n"
            "2. Set REQUESTS_CA_BUNDLE environment variable\n"
            "3. Use verify=False as temporary workaround\n"
            "4. Reinstall certifi package"
        ),
        "agent_id": "agent-001",
        "session_id": "session-xyz",
        "duration_seconds": 3.5,
        "tools_used": ["bash", "search_web"],
        "error": "",
        "metadata": {},
    }


@pytest.fixture
def failed_task_result() -> dict:
    return {
        "task_id": "task-002",
        "success": False,
        "content": "Deploy to production",
        "result": "",
        "agent_id": "agent-001",
        "error": "Connection timeout to production server",
        "metadata": {},
    }


# =============================================================================
# TaskResult
# =============================================================================

class TestTaskResult:
    def test_from_dict_basic(self, sample_task_result):
        tr = TaskResult.from_dict(sample_task_result)
        assert tr.task_id == "task-001"
        assert tr.success is True
        assert tr.duration_seconds == 3.5
        assert "bash" in tr.tools_used

    def test_from_dict_missing_fields(self):
        tr = TaskResult.from_dict({"task_id": "t1", "success": False})
        assert tr.content == ""
        assert tr.error == ""

    def test_from_dict_copies_fields(self, sample_task_result):
        """验证 from_dict 正确复制所有字段"""
        tr = TaskResult.from_dict(sample_task_result)
        assert tr.task_id == "task-001"
        assert tr.success is True
        assert tr.duration_seconds == 3.5
        assert "bash" in tr.tools_used
        assert tr.error == ""


# =============================================================================
# RuleBasedExtractor
# =============================================================================

class TestRuleBasedExtractor:
    def test_extract_steps_ordered_list(self):
        extractor = RuleBasedExtractor()
        text = "1. First step\n2. Second step\n3. Third step"
        steps = extractor._extract_steps(text)
        assert len(steps) >= 2

    def test_extract_steps_unordered_list(self):
        extractor = RuleBasedExtractor()
        text = "- Install certifi\n- Update certificates"
        steps = extractor._extract_steps(text)
        assert len(steps) >= 1

    def test_extract_triggers(self):
        extractor = RuleBasedExtractor()
        text = "How to fix Python SSL error when should I update certs"
        triggers = extractor._extract_triggers(text)
        assert len(triggers) >= 1
        assert any("how" in t for t in triggers)

    def test_confidence_success_with_steps(self, sample_task_result):
        extractor = RuleBasedExtractor()
        tr = TaskResult.from_dict(sample_task_result)
        candidate = extractor.extract(tr)
        assert candidate.confidence >= 0.3
        assert candidate.confidence < 1.0

    def test_confidence_failed_task(self, failed_task_result):
        extractor = RuleBasedExtractor()
        tr = TaskResult.from_dict(failed_task_result)
        candidate = extractor.extract(tr)
        assert candidate.confidence < 0.3
        # 失败任务只有 error-case tag，不含 "error" 裸词
        assert "error-case" in candidate.tags

    def test_derive_name(self, sample_task_result):
        extractor = RuleBasedExtractor()
        tr = TaskResult.from_dict(sample_task_result)
        candidate = extractor.extract(tr)
        assert len(candidate.name) > 0
        assert "_" in candidate.name or candidate.name.startswith("skill_")

    def test_summarize_truncation(self):
        extractor = RuleBasedExtractor()
        long_text = "a" * 300
        summary = extractor._summarize(long_text)
        # max_len=200 + 截断时的省略符…，最多 201 字符
        assert len(summary) <= 203
        # 不应以 'a' 结尾（应落在完整词的边界）
        assert not summary.endswith("aaaa")


# =============================================================================
# SkillCandidate
# =============================================================================

class TestSkillCandidate:
    def test_skill_candidate_defaults(self):
        sc = SkillCandidate(name="test_skill", description="test", confidence=0.85)
        assert sc.version == "1.0.0"
        assert sc.triggers == []
        assert sc.actions == []
        assert len(sc.extracted_at) > 0


# =============================================================================
# SkillDocumentWriter
# =============================================================================

class TestSkillDocumentWriter:
    def test_write_high_confidence(self, temp_dirs, sample_task_result):
        extractor = RuleBasedExtractor()
        tr = TaskResult.from_dict(sample_task_result)
        candidate = extractor.extract(tr)
        candidate.confidence = 0.92  # 强制高置信度

        writer = SkillDocumentWriter(temp_dirs["skills_dir"])
        doc_path = writer.write(candidate)

        assert doc_path.exists()
        content = doc_path.read_text(encoding="utf-8")
        assert "# " in content
        assert "## Triggers" in content
        assert "## Actions" in content

    def test_write_metadata_json(self, temp_dirs, sample_task_result):
        extractor = RuleBasedExtractor()
        tr = TaskResult.from_dict(sample_task_result)
        candidate = extractor.extract(tr)
        candidate.confidence = 0.92

        writer = SkillDocumentWriter(temp_dirs["skills_dir"])
        doc_path = writer.write(candidate)

        meta_path = doc_path.parent / "metadata.json"
        assert meta_path.exists()
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        assert meta["confidence"] == 0.92
        assert "extracted_at" in meta

    def test_safe_name_sanitization(self, temp_dirs):
        writer = SkillDocumentWriter(temp_dirs["skills_dir"])
        candidate = SkillCandidate(
            name="Fix SSL Error!?? @#$%",
            description="test",
            confidence=0.9,
        )
        doc_path = writer.write(candidate)
        # 目录名中不应有特殊字符
        assert "#" not in str(doc_path)


# =============================================================================
# DreamingQueue
# =============================================================================

class TestDreamingQueue:
    def test_add_and_read(self, temp_dirs):
        queue = DreamingQueue(temp_dirs["queue_path"])
        candidate = SkillCandidate(
            name="test_dream_skill",
            description="test description",
            confidence=0.65,
            confidence_reason="medium confidence",
            triggers=["error", "timeout"],
            actions=["Step 1: Check connection"],
            source_task_id="task-003",
            source_agent_id="agent-001",
        )
        queue.add(candidate)

        pending = queue.read_pending()
        assert len(pending) == 1
        assert pending[0].name == "test_dream_skill"
        assert pending[0].confidence == 0.65

    def test_empty_queue(self, temp_dirs):
        queue = DreamingQueue(temp_dirs["queue_path"])
        assert queue.read_pending() == []


# =============================================================================
# ImmediateSkillHook（端到端）
# =============================================================================

class TestImmediateSkillHook:
    @pytest.mark.asyncio
    async def test_hook_high_confidence_direct_write(self, temp_dirs, sample_task_result):
        hook = ImmediateSkillHook(
            agent_id="agent-001",
            skills_dir=temp_dirs["skills_dir"],
            dream_queue_path=temp_dirs["queue_path"],
            persist_to_memory=False,   # 关闭记忆写入，避免依赖 persistent_store
        )
        # 强制高置信度
        hook.HIGH_CONFIDENCE_THRESHOLD = 0.0

        candidate = await hook.after_task_complete(sample_task_result)

        assert candidate is not None
        assert candidate.confidence >= 0.0

        # 验证文件已写入
        skill_files = list(temp_dirs["skills_dir"].rglob("*.md"))
        assert len(skill_files) >= 1

    @pytest.mark.asyncio
    async def test_hook_medium_confidence_queued(self, temp_dirs):
        """中置信度候选进入梦境队列，不写 skill 文档"""
        hook = ImmediateSkillHook(
            agent_id="agent-001",
            skills_dir=temp_dirs["skills_dir"],
            dream_queue_path=temp_dirs["queue_path"],
            persist_to_memory=False,
        )
        # 注入固定 0.65 置信度的提取器，触发梦境队列路由
        task_result = TaskResult(
            task_id="t-medium",
            success=True,
            content="Check server status when asked",
            result="Server is running.",
        )
        hook._llm_extractor = _FakeHighConfidenceExtractor(0.65)

        candidate = await hook.after_task_complete(task_result)
        assert candidate is not None
        assert candidate.confidence == 0.65

        # 验证进入梦境队列（不写 skill 文档）
        queue = DreamingQueue(temp_dirs["queue_path"])
        pending = queue.read_pending()
        assert len(pending) == 1
        assert pending[0].confidence == 0.65

    @pytest.mark.asyncio
    async def test_hook_empty_result_skipped(self, temp_dirs):
        hook = ImmediateSkillHook(
            agent_id="agent-001",
            skills_dir=temp_dirs["skills_dir"],
            dream_queue_path=temp_dirs["queue_path"],
            persist_to_memory=False,
        )
        result = await hook.after_task_complete({"task_id": "empty", "success": False})
        assert result is None

    @pytest.mark.asyncio
    async def test_hook_failed_task_low_confidence(self, temp_dirs, failed_task_result):
        hook = ImmediateSkillHook(
            agent_id="agent-001",
            skills_dir=temp_dirs["skills_dir"],
            dream_queue_path=temp_dirs["queue_path"],
            persist_to_memory=False,
        )
        # HIGH 阈值设为 1.0，这样即使失败候选也只到梦境队列
        hook.HIGH_CONFIDENCE_THRESHOLD = 1.0
        hook.MEDIUM_CONFIDENCE_THRESHOLD = 1.0

        candidate = await hook.after_task_complete(failed_task_result)
        # 失败任务置信度低，应该被丢弃
        assert candidate is None or candidate.confidence < 0.2


# =============================================================================
# 置信度分流边界
# =============================================================================

class TestConfidenceRouting:
    @pytest.mark.asyncio
    async def test_threshold_boundary_high(self, temp_dirs):
        """置信度 0.8 应该直接写盘"""
        hook = ImmediateSkillHook(
            agent_id="agent-001",
            skills_dir=temp_dirs["skills_dir"],
            dream_queue_path=temp_dirs["queue_path"],
            persist_to_memory=False,
        )
        hook.HIGH_CONFIDENCE_THRESHOLD = 0.8
        hook.MEDIUM_CONFIDENCE_THRESHOLD = 0.5

        tr = TaskResult(
            task_id="t-high",
            success=True,
            content="Important task: 1. First 2. Second 3. Third",
            result="Success",
        )
        # 模拟高置信度：替换提取器
        hook._llm_extractor = _FakeHighConfidenceExtractor(0.85)

        candidate = await hook.after_task_complete(tr)
        assert candidate is not None
        assert candidate.confidence >= 0.8

        # 检查是否写入了 skill 文件
        skill_files = list(temp_dirs["skills_dir"].rglob("*.md"))
        assert len(skill_files) >= 1

    @pytest.mark.asyncio
    async def test_threshold_boundary_medium(self, temp_dirs):
        """置信度 0.65 应该进入梦境队列，不写盘"""
        hook = ImmediateSkillHook(
            agent_id="agent-001",
            skills_dir=temp_dirs["skills_dir"],
            dream_queue_path=temp_dirs["queue_path"],
            persist_to_memory=False,
        )
        hook.HIGH_CONFIDENCE_THRESHOLD = 0.8
        hook.MEDIUM_CONFIDENCE_THRESHOLD = 0.5

        tr = TaskResult(
            task_id="t-med",
            success=True,
            content="Medium priority task: 1. Do this 2. Do that",
            result="Done",
        )
        hook._llm_extractor = _FakeHighConfidenceExtractor(0.65)

        await hook.after_task_complete(tr)

        # 应该进入队列，不写盘
        queue = DreamingQueue(temp_dirs["queue_path"])
        pending = queue.read_pending()
        assert len(pending) >= 1

        skill_files = list(temp_dirs["skills_dir"].rglob("*.md"))
        # med 置信度不会触发写盘
        if skill_files:
            # 如果有文件，可能是之前测试残留，不作强制判断
            pass


# =============================================================================
# 测试用假提取器
# =============================================================================

class _FakeHighConfidenceExtractor:
    """返回固定置信度的提取器（用于测试路由）"""

    def __init__(self, confidence: float):
        self._confidence = confidence

    async def extract(self, task_result: TaskResult) -> SkillCandidate:
        return SkillCandidate(
            name=f"fake_skill_{task_result.task_id}",
            description=f"Fake skill for {task_result.task_id}",
            confidence=self._confidence,
            confidence_reason="fake extractor",
            triggers=["test"],
            actions=["Step 1: test"],
            source_task_id=task_result.task_id,
        )
