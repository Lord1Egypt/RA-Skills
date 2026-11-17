"""Phase 3：生命周期——回收站、重复安装识别、清理重复。"""
import os
import tempfile
from pathlib import Path

import findskills


def test_send_to_trash_moves(tmp_path):
    d = tmp_path / "trash-me"
    d.mkdir()
    (d / "SKILL.md").write_text("x", encoding="utf-8")
    where = findskills.send_to_trash(d)
    assert where in ("recycle", "local-trash")
    assert not d.exists()


def test_find_duplicate_installs():
    local = [
        {"name": "dup", "slug": "dup", "path": "/a/dup/SKILL.md"},
        {"name": "dup", "slug": "dup", "path": "/b/dup/SKILL.md"},
        {"name": "uniq", "slug": "uniq", "path": "/c/uniq/SKILL.md"},
    ]
    dups = findskills.find_duplicate_installs(local)
    assert len(dups) == 1
    assert dups[0]["count"] == 2


def test_clean_dupes_keeps_latest(monkeypatch, tmp_path):
    old = tmp_path / "old"
    new = tmp_path / "new"
    old.mkdir()
    new.mkdir()
    (old / "SKILL.md").write_text("---\nname: dup\n---\n", encoding="utf-8")
    (new / "SKILL.md").write_text("---\nname: dup\n---\n", encoding="utf-8")
    # 让 old 更旧
    os.utime(old, (1_000_000, 1_000_000))
    os.utime(new, (2_000_000, 2_000_000))
    fake = [
        {"name": "dup", "slug": "dup", "path": str(old / "SKILL.md")},
        {"name": "dup", "slug": "dup", "path": str(new / "SKILL.md")},
    ]
    monkeypatch.setattr(findskills, "discover_local", lambda: fake)
    rc = findskills.main(["clean-dupes"])
    assert rc == 0
    # 最新的 new 保留，旧的 old 被移入回收站
    assert new.exists()
    assert not old.exists()


def test_uninstall_self_guard():
    rc = findskills.main(["uninstall", "find-skills-plusplus"])
    assert rc == 1
