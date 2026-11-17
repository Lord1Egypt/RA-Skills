"""测试环境体检 `doctor`：frontmatter 合法性 / 质量偏弱 / 重复安装 / 依赖连接器 / 硬编码路径。"""

from __future__ import annotations

from pathlib import Path

import pytest

import findskills as fk


def _make_skill(root: Path, name: str, *, valid=True, body="", extra=""):
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    if valid:
        txt = (
            "---\nname: " + name + "\nversion: 1.0.0\nauthor: T\nlicense: MIT\n"
            "description: " + name + " 测试技能\n---\n"
            "# " + name + "\n\n这是一个用于测试的技能。\n\n```python\nx = 1\n```\n\n步骤 1：先做 A。\n" + body
        )
    else:
        txt = "# " + name + "\n\n没有合法 frontmatter 的技能。\n"
    (d / "SKILL.md").write_text(txt + extra, encoding="utf-8")
    return d


def test_doctor_flags_invalid_frontmatter(monkeypatch, capsys, tmp_path):
    bad = _make_skill(tmp_path, "bad-skill", valid=False)
    monkeypatch.setattr(fk, "discover_local", lambda include_self=True: [
        {"name": "bad-skill", "slug": "bad-skill", "version": "?", "path": str(bad)},
    ])
    rc = fk.main(["doctor"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "bad-skill" in out
    assert "frontmatter" in out


def test_doctor_flags_connector_dependency(monkeypatch, capsys, tmp_path):
    dep = _make_skill(tmp_path, "dep-skill", body="本技能依赖 westock 行情连接器提供数据。\n")
    monkeypatch.setattr(fk, "discover_local", lambda include_self=True: [
        {"name": "dep-skill", "slug": "dep-skill", "version": "1.0.0", "path": str(dep)},
    ])
    rc = fk.main(["doctor"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "westock" in out


def test_doctor_healthy_when_all_valid(monkeypatch, capsys, tmp_path):
    good = _make_skill(tmp_path, "good-skill")
    monkeypatch.setattr(fk, "discover_local", lambda include_self=True: [
        {"name": "good-skill", "slug": "good-skill", "version": "1.0.0", "path": str(good)},
    ])
    rc = fk.main(["doctor"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "环境健康" in out


def test_doctor_flags_duplicate_installs(monkeypatch, capsys, tmp_path):
    a = _make_skill(tmp_path, "dup-skill-a")
    b = _make_skill(tmp_path, "dup-skill-b")
    # 两个不同路径但 frontmatter name 相同 → 重复安装
    (b / "SKILL.md").write_text(
        "---\nname: dup-skill\nversion: 1.0.0\nauthor: T\nlicense: MIT\n"
        "description: 重复\n---\n# dup\n\n```python\nx=1\n```\n步骤 1：A。\n", encoding="utf-8")
    (a / "SKILL.md").write_text(
        "---\nname: dup-skill\nversion: 1.0.0\nauthor: T\nlicense: MIT\n"
        "description: 重复\n---\n# dup\n\n```python\nx=1\n```\n步骤 1：A。\n", encoding="utf-8")
    monkeypatch.setattr(fk, "discover_local", lambda include_self=True: [
        {"name": "dup-skill", "slug": "dup-skill-a", "version": "1.0.0", "path": str(a)},
        {"name": "dup-skill", "slug": "dup-skill-b", "version": "1.0.0", "path": str(b)},
    ])
    rc = fk.main(["doctor"])
    assert rc == 0
    assert "重复安装" in capsys.readouterr().out
