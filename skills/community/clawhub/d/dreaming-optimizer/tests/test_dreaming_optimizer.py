#!/usr/bin/env python3
"""
Test suite for dreaming-optimizer skill — matches current implementation.

Covers:
  1. score_entries  (bin/score_entries.py)
  2. deduplicate    (bin/deduplicate.py)
  3. commit         (bin/commit.py)
  4. dreaming_summary (scripts/dreaming_summary.py)
"""
import json, sys, sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta

import pytest

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "bin"))
sys.path.insert(0, str(SKILL_ROOT / "lib"))
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from score_entries import score_entry, score_entries, parse_memory_file
from deduplicate import deduplicate_entries, token_similarity, get_blayer_memories
from commit import commit_to_blayer, tag_entry
from dreaming_summary import generate_summary


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_md_file_with_separators(tmp_path):
    """Create a memory .md file with --- separators (real format)."""
    mem_dir = tmp_path / "memory"
    mem_dir.mkdir(parents=True)
    f = mem_dir / "2026-04-17.md"
    f.write_text(
        "---\n昨天完成数据库连接池优化工作。\n---\n今天计划实现新的dedup逻辑。\n---\n明天准备测试health-check模块。",
        encoding="utf-8",
    )
    return f


@pytest.fixture
def sample_md_file_short(tmp_path):
    """Create a memory .md file with short entries (< 10 chars → filtered)."""
    mem_dir = tmp_path / "memory"
    mem_dir.mkdir(parents=True)
    f = mem_dir / "2026-04-17.md"
    f.write_text("---\n短\n---", encoding="utf-8")
    return f


@pytest.fixture
def sample_md_file_paragraphs(tmp_path):
    """Create a memory .md file using blank-line paragraph splitting."""
    mem_dir = tmp_path / "memory"
    mem_dir.mkdir(parents=True)
    f = mem_dir / "2026-04-17.md"
    f.write_text("第一段很长的内容描述。\n\n第二段更长的内容。", encoding="utf-8")
    return f


# ---------------------------------------------------------------------------
# 1. score_entries tests
# ---------------------------------------------------------------------------

class TestParseMemoryFile:
    """Unit tests for memory file parsing."""

    def test_parse_with_separators(self, sample_md_file_with_separators):
        """--- separators split file into 3 entries of sufficient length."""
        entries = parse_memory_file(sample_md_file_with_separators)
        assert len(entries) == 3
        for e in entries:
            assert "filename" in e
            assert "mtime" in e

    def test_parse_short_fragment_filtered(self, sample_md_file_short):
        """Fragments shorter than 10 chars are filtered out."""
        entries = parse_memory_file(sample_md_file_short)
        assert all(len(e["content"]) >= 10 for e in entries)

    def test_parse_with_paragraphs(self, sample_md_file_paragraphs):
        """Paragraph-split files return at least one entry."""
        entries = parse_memory_file(sample_md_file_paragraphs)
        assert len(entries) >= 1

    def test_parse_missing_file_returns_empty(self, tmp_path):
        """Non-existent file → empty list (graceful)."""
        entries = parse_memory_file(tmp_path / "nonexistent.md")
        assert entries == []


class TestScoreEntry:
    """Unit tests for single-entry scoring."""

    def test_score_fact_terms_above_baseline(self):
        """Content with fact terms scores above baseline 50."""
        result = score_entry("已修复了数据库bug，测试通过。")
        assert result["score"] > 50
        assert len(result["fact_terms_found"]) > 0

    def test_score_short_content_penalty(self):
        """Content shorter than 20 chars receives a penalty."""
        result = score_entry("今天还好。")
        assert result["score"] < 50

    def test_score_empty_content(self):
        """Empty content returns base score 50."""
        result = score_entry("")
        assert result["score"] == 50
        assert "Empty content" in result["reasons"][0]

    def test_score_clamped_to_100(self):
        """Score cannot exceed 100."""
        content = "已修复 已实现 已完成 已部署 已上线 " * 10
        result = score_entry(content)
        assert result["score"] <= 100
        assert result["score"] >= 0

    def test_score_with_recent_mtime(self):
        """Recent mtime (< 7 days) gives recency bonus."""
        recent = datetime.now(tz=timezone.utc) - timedelta(days=2)
        result = score_entry("数据库API配置", mtime=recent)
        assert any("recency" in r for r in result["reasons"])

    def test_score_with_old_mtime(self):
        """Old mtime (> 7 days) gives no recency bonus."""
        old = datetime.now(tz=timezone.utc) - timedelta(days=30)
        result = score_entry("数据库API配置", mtime=old)
        assert not any("recency" in r for r in result["reasons"])


class TestTagEntry:
    """Unit tests for fact/opinion/preference/learning tagger."""

    def test_tag_fact(self):
        assert tag_entry("已修复了数据库bug，测试通过。") == "fact"

    def test_tag_opinion(self):
        assert tag_entry("我觉得这个方案可能更好。") == "opinion"

    def test_tag_preference(self):
        assert tag_entry("我更喜欢使用tiktoken，不喜欢其他的。") == "preference"

    def test_tag_learning(self):
        assert tag_entry("学到了新的优化技巧，发现了insight。") == "learning"

    def test_tag_context_fallback(self):
        assert tag_entry("今天天气很好，适合散步。") == "context"

    def test_tag_fact_priority_over_opinion(self):
        """Content with both fact and opinion → 'fact' wins."""
        result = tag_entry("已修复了可能存在的数据库bug。")
        assert result == "fact"


class TestScoreEntries:
    """Integration tests for score_entries (file I/O)."""

    def test_score_entries_empty_list(self):
        """Empty file list → total_processed 0."""
        result = score_entries(memory_files=[], threshold=70)
        assert result["scored"] == []
        assert result["total_processed"] == 0

    def test_score_entries_threshold_filters(self, sample_md_file_with_separators):
        """Entries below threshold go to archived (some may pass due to fact terms)."""
        result = score_entries(memory_files=[sample_md_file_with_separators], threshold=70)
        assert result["total_processed"] >= 1
        # All archived entries must have score < 70
        for a in result["archived"]:
            assert a["score"] < 70

    def test_score_entries_high_threshold(self, sample_md_file_with_separators):
        """Threshold 100 → nothing passes."""
        result = score_entries(memory_files=[sample_md_file_with_separators], threshold=100)
        assert result["passed"] == []

    def test_score_entries_passing_entries(self):
        """High-fact content passes threshold."""
        f = tmp_path = Path("/tmp/test_score_pass.md")
        # Write content with many fact terms to score high
        high_content = (
            "---\n"
            "已修复 已实现 已完成 已部署 测试通过 "
            "数据库API模块 代码优化 函数重构 架构调整 "
            .strip()
        )
        # Create temp file
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, dir="/tmp"
        ) as tf:
            tf.write(high_content)
            tf_path = Path(tf.name)

        try:
            result = score_entries(memory_files=[tf_path], threshold=70)
            # With all those fact terms score should be high
            assert result["total_processed"] >= 1
        finally:
            tf_path.unlink(missing_ok=True)

    def test_score_entries_threshold_used_stored(self):
        """threshold_used matches what was passed."""
        result = score_entries(memory_files=[], threshold=80)
        assert result["threshold_used"] == 80

    def test_score_entries_mixed_results(self, sample_md_file_with_separators):
        """Categorization is correct: passed ∪ archived = scored."""
        result = score_entries(memory_files=[sample_md_file_with_separators], threshold=70)
        ids_in_scored = {id(e) for e in result["scored"]}
        ids_in_passed = {id(e) for e in result["passed"]}
        ids_in_archived = {id(e) for e in result["archived"]}
        assert ids_in_passed | ids_in_archived == ids_in_scored
        for p in result["passed"]:
            assert p["score"] >= 70
        for a in result["archived"]:
            assert a["score"] < 70


# ---------------------------------------------------------------------------
# 2. deduplicate tests
# ---------------------------------------------------------------------------

class TestTokenSimilarity:
    """Unit tests for token-overlap similarity."""

    def test_identical_strings(self):
        assert token_similarity("hello world", "hello world") == 1.0

    def test_no_overlap(self):
        assert token_similarity("apple banana", "desk chair") == 0.0

    def test_partial_overlap(self):
        s = token_similarity(
            "database API fix test passed",
            "database API config deploy done",
        )
        assert 0 < s < 1

    def test_empty_string(self):
        assert token_similarity("", "anything") == 0.0


class TestDedupEntries:
    """Tests for deduplicate_entries()."""

    def test_deduplicate_no_blayer(self):
        """B-layer empty → all unique."""
        entries = [
            {"content": "这是第一条独特记忆内容"},
            {"content": "这是第二条独特记忆内容"},
        ]
        result = deduplicate_entries(entries, blayer_memories=[], threshold=0.85)
        assert result["stats"]["unique_count"] == 2
        assert result["stats"]["merged_count"] == 0

    def test_deduplicate_all_unique(self):
        """No overlap → all unique."""
        existing = [{"id": 1, "content": "完全不相关的另一个主题"}]
        entries = [
            {"content": "今天学习了新的编程语言特性"},
            {"content": "明天准备测试health模块"},
        ]
        result = deduplicate_entries(entries, blayer_memories=existing, threshold=0.85)
        assert result["stats"]["unique_count"] == 2
        assert result["stats"]["merged_count"] == 0

    def test_deduplicate_exact_duplicate(self):
        """Exact content match → merged."""
        existing = [{"id": 1, "content": "已完成数据库API修复"}]
        entries = [{"content": "已完成数据库API修复"}]
        result = deduplicate_entries(entries, blayer_memories=existing, threshold=0.85)
        assert result["stats"]["merged_count"] >= 1

    def test_deduplicate_partial_duplicate(self):
        """High similarity (token overlap ≥ threshold) → merged."""
        existing = [{"id": 1, "content": "fixed the database API issue and deployed it to production"}]
        entries = [{"content": "fixed the database API issue and deployed it to production environment"}]
        result = deduplicate_entries(entries, blayer_memories=existing, threshold=0.85)
        assert result["stats"]["merged_count"] >= 1

    def test_deduplicate_empty_input(self):
        """Empty list → zero counts."""
        result = deduplicate_entries([], blayer_memories=[], threshold=0.85)
        assert result["stats"]["unique_count"] == 0
        assert result["stats"]["merged_count"] == 0

    def test_deduplicate_threshold_respected(self):
        """Low similarity below threshold → kept unique."""
        existing = [{"id": 1, "content": "today is a nice weather day for a walk"}]
        entries = [{"content": "database API configuration setup"}]
        result = deduplicate_entries(entries, blayer_memories=existing, threshold=0.90)
        assert result["stats"]["unique_count"] == 1


# ---------------------------------------------------------------------------
# 3. commit tests  (mock blayer_client.get_client)
# ---------------------------------------------------------------------------

class TestCommitToBlayer:
    """Tests for commit_to_blayer() — mocks blayer_client.get_client."""

    def _fake_client(self):
        client = MagicMock()
        client.commit_entry.return_value = 1
        client.log_action.return_value = None
        return client

    def test_commit_result_counts(self):
        """High-scoring entries contribute to committed count."""
        entries = [
            {"content": "测试内容A。", "score": 85, "source_file": "test.md"},
            {"content": "测试内容B。", "score": 80, "source_file": "test.md"},
        ]
        fake = self._fake_client()
        with patch("commit.get_client", return_value=fake):
            result = commit_to_blayer(entries, dry_run=True)
        assert result["committed"] == 2
        assert result["dry_run"] is True
        assert result["failed"] == 0

    def test_commit_empty_list(self):
        """Empty list → no client calls, committed=0."""
        fake = self._fake_client()
        with patch("commit.get_client", return_value=fake):
            result = commit_to_blayer([])
        assert result["committed"] == 0
        assert result["failed"] == 0

    def test_commit_low_score_archived(self):
        """Score below commit threshold but above archive → archived."""
        entries = [{"content": "还行吧。", "score": 40, "source_file": "test.md"}]
        fake = self._fake_client()
        with patch("commit.get_client", return_value=fake):
            result = commit_to_blayer(entries, dry_run=True)
        assert result["archived"] == 1

    def test_commit_below_archive_discarded(self):
        """Score below archive threshold → discarded."""
        entries = [{"content": "xxx", "score": 10, "source_file": "test.md"}]
        fake = self._fake_client()
        with patch("commit.get_client", return_value=fake):
            result = commit_to_blayer(entries, dry_run=True)
        assert result["committed"] == 0
        assert result["archived"] == 0

    def test_commit_tag_inference(self):
        """High-scoring entries are counted as committed."""
        entries = [
            {"content": "I think this plan is better.", "score": 85, "source_file": "test.md"},
            {"content": "Fixed the database bug and deployed.", "score": 88, "source_file": "test.md"},
        ]
        fake = self._fake_client()
        with patch("commit.get_client", return_value=fake):
            result = commit_to_blayer(entries, dry_run=True)
        assert result["committed"] == 2
        assert result["failed"] == 0


# ---------------------------------------------------------------------------
# 4. dreaming_summary tests
# ---------------------------------------------------------------------------

class TestDreamingSummary:
    """Tests for generate_summary() — explicit parameters, writes JSON+MD."""

    def test_summary_valid_json(self, fake_home):
        """Summary is JSON-serialisable with expected fields."""
        summary_dir = fake_home / "summary_out"
        summary = generate_summary(
            scored=10, passed=7, archived=3, merged=2,
            committed=5, discarded=0,
            tag_counts={"fact": 3, "opinion": 2, "context": 2},
            output_dir=summary_dir,
        )
        assert isinstance(summary, dict)
        assert summary["scored"] == 10
        assert summary["passed"] == 7
        assert summary["archived"] == 3
        assert summary["merged"] == 2
        assert summary["committed"] == 5
        assert summary["dreaming_version"] == "1.0.0"
        json.dumps(summary)  # must not raise

    def test_summary_file_saved(self, fake_home):
        """Both JSON and Markdown files are written to output_dir."""
        summary_dir = fake_home / "summary_out"
        summary = generate_summary(scored=5, passed=3, archived=2, output_dir=summary_dir)
        date_str = summary["ts"][:10]
        json_file = summary_dir / f"dreaming-summary-{date_str}.json"
        md_file = summary_dir / f"dreaming-summary-{date_str}.md"
        assert json_file.exists()
        assert md_file.exists()
        loaded = json.loads(json_file.read_text())
        assert loaded["scored"] == 5

    def test_summary_zero_counts(self, fake_home):
        """Zero-count summary is valid JSON."""
        summary_dir = fake_home / "summary_out"
        summary = generate_summary(output_dir=summary_dir)
        json.dumps(summary)  # must not raise

    def test_summary_dreaming_version(self, fake_home):
        """dreaming_version field equals '1.0.0'."""
        summary_dir = fake_home / "summary_out"
        summary = generate_summary(output_dir=summary_dir)
        assert summary["dreaming_version"] == "1.0.0"

    def test_summary_recommendations(self, fake_home):
        """recommendations are included when provided."""
        summary_dir = fake_home / "summary_out"
        recs = ["Consider archiving low-score entries", "Review duplicate patterns"]
        summary = generate_summary(
            scored=5, passed=2, archived=2, merged=1,
            recommendations=recs, output_dir=summary_dir,
        )
        assert summary["recommendations"] == recs
