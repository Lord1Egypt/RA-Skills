"""Shared pytest fixtures for dreaming-optimizer tests."""
import json, sqlite3
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
import pytest

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def fake_home(tmp_path):
    """
    Replace Path.home() with a controlled temp directory for every test.
    """
    fake = tmp_path / "fake_openclaw_dreaming"
    fake.mkdir(parents=True, exist_ok=True)

    # Ensure required sub-dirs exist
    (fake / ".openclaw" / "workspace" / "memory").mkdir(parents=True, exist_ok=True)
    (fake / ".openclaw" / "memory").mkdir(parents=True, exist_ok=True)
    (fake / ".openclaw" / "workspace" / "memory" / "dreaming-summaries").mkdir(
        parents=True, exist_ok=True
    )

    with patch("pathlib.Path.home", return_value=fake):
        yield fake


@pytest.fixture
def empty_memory_dir(fake_home):
    """Return the path to the (empty) A-layer memory directory."""
    return fake_home / ".openclaw" / "workspace" / "memory"


@pytest.fixture
def sample_memory_files(empty_memory_dir):
    """Create three sample daily-memory .md files."""
    files = []

    # File 1: rich content with fact terms → high score
    f1 = empty_memory_dir / "2026-04-15.md"
    f1.write_text(
        "---\n昨天完成工作\n---\n已完成数据库连接池的API测试，发现了配置bug并修复。\n---\n使用tiktoken对memory entries做embedding，测试通过。",
        encoding="utf-8",
    )
    files.append(f1)

    # File 2: short vague content → low score
    f2 = empty_memory_dir / "2026-04-16.md"
    f2.write_text("---\n还行吧。", encoding="utf-8")
    files.append(f2)

    # File 3: medium content, borderline
    f3 = empty_memory_dir / "2026-04-17.md"
    f3.write_text(
        "---\n研究了memory-health-check skill的设计。\n---\n关键点：完整性检查、膨胀率、孤儿检测。",
        encoding="utf-8",
    )
    files.append(f3)

    return files


@pytest.fixture
def empty_blayer(fake_home):
    """Return path to a non-existent B-layer SQLite (empty state)."""
    return fake_home / ".openclaw" / "memory" / "main.sqlite"


@pytest.fixture
def populated_blayer(fake_home, empty_memory_dir):
    """Create a B-layer SQLite with a few existing memories."""
    db_path = fake_home / ".openclaw" / "memory" / "main.sqlite"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            score INTEGER DEFAULT 50,
            tag TEXT DEFAULT 'context',
            source TEXT,
            created_at TEXT,
            updated_at TEXT,
            dreaming_tag TEXT DEFAULT 'dreaming-optimizer'
        )
    """)
    now = datetime.now(tz=timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO memories (content, score, tag, source, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        ("已完成数据库API修复", 80, "fact", "dreaming-optimizer", now, now),
    )
    conn.execute(
        "INSERT INTO memories (content, score, tag, source, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        ("偏好使用tiktoken做embedding", 65, "preference", "dreaming-optimizer", now, now),
    )
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def sample_entries():
    """Return a list of entry dicts matching the current commit API."""
    return [
        {"content": "今天完成了数据库API测试，发现了配置bug并修复。", "score": 85, "source_file": "2026-04-15.md"},
        {"content": "研究了memory-health-check skill的设计，计划下周开始实现。", "score": 72, "source_file": "2026-04-17.md"},
        {"content": "今天还行吧。", "score": 55, "source_file": "2026-04-16.md"},
    ]
