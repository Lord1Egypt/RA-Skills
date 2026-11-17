# -*- coding: utf-8 -*-
"""回归：find-skills++ 必须能给自己打分（自检）。

背景（真实缺陷）：discover_local 无条件排除自身目录名，导致
`quality find-skills-plusplus` 报「未找到该技能」——一个宣称能做质量评级的
工具评不了自己，出场演示当场穿帮。

修复：discover_local 增加 include_self 参数；quality 自检时包含自身，
并支持 `self` / `find-skills++` 等别名。默认仍排除自己（避免搜索结果自荐）。

注意：discover_local 的排除/包含逻辑不再依赖真实安装位置——测试注入临时
roots，保证在 CI（无 ~/.workbuddy/skills）等任意环境都能确定性验证。
"""
import io
import contextlib
from pathlib import Path

import pytest

import findskills


@pytest.fixture
def fake_skills_dir(tmp_path):
    """构造临时技能根目录，含「自己」与「另一个」两个技能，让 discover_local
    的排除/包含逻辑可在任意环境（含 CI）确定性验证。"""
    base = tmp_path / "skills"
    self_dir = base / findskills.SELF_SLUG
    self_dir.mkdir(parents=True)
    (self_dir / "SKILL.md").write_text(
        "---\nname: find-skills++\nversion: 5.3.0\n---\n", encoding="utf-8")
    other_dir = base / "other-skill"
    other_dir.mkdir(parents=True)
    (other_dir / "SKILL.md").write_text(
        "---\nname: other\nslug: other-skill\nversion: 1.0\n---\n", encoding="utf-8")
    return base


def test_discover_local_excludes_self_by_default(fake_skills_dir):
    """默认不列出自己——搜索结果里不该自荐。"""
    names = {s["slug"] for s in findskills.discover_local(roots=[fake_skills_dir])}
    assert findskills.SELF_SLUG not in names
    assert "other-skill" in names


def test_discover_local_include_self(fake_skills_dir):
    """include_self=True 时能找到自己。"""
    names = {s["slug"] for s in findskills.discover_local(include_self=True, roots=[fake_skills_dir])}
    assert findskills.SELF_SLUG in names


def test_quality_self_alias_runs():
    """`quality self` 必须能跑通并给出评分，不报「未找到」。"""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = findskills.main(["quality", "self"])
    out = buf.getvalue()
    assert rc == 0, f"quality self 失败，输出：{out}"
    assert "未找到" not in out
    assert "分" in out or "评级" in out or "质量" in out


def test_quality_by_slug_runs():
    """用完整 slug 也应能定位到自己。"""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = findskills.main(["quality", "find-skills-plusplus"])
    out = buf.getvalue()
    assert rc == 0, f"quality <slug> 失败，输出：{out}"
    assert "未找到" not in out
