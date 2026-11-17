# -*- coding: utf-8 -*-
"""结构规范测试：对标生态头部技能（self-improving-agent / agent-browser）。

验证 frontmatter 标准化（version + metadata）与渐进式披露（references/）已落地。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_REFS = ["security.md", "cli.md", "ranking.md", "enhancements.md", "roadmap.md"]


def _frontmatter():
    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    assert m, "SKILL.md 缺少合法 frontmatter"
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip().strip('"').strip("'")
    return fields, t


def test_frontmatter_has_version():
    fields, _ = _frontmatter()
    assert fields.get("version"), "缺少 version（头部技能均有，#1 技能已 3.0.24）"
    assert re.match(r"^\d+\.\d+\.\d+$", fields["version"]), "version 非语义化"


def test_frontmatter_has_metadata_block():
    _, t = _frontmatter()
    assert "metadata:" in t, "缺少 metadata 块（slug / displayName）"


def test_frontmatter_core_fields():
    fields, _ = _frontmatter()
    for f in ("name", "description", "author", "license"):
        assert fields.get(f), f"缺少 {f}"


def test_frontmatter_has_keywords():
    fields, _ = _frontmatter()
    assert fields.get("keywords"), "缺少 keywords（影响市场检索）"


def test_references_dir_exists_with_required_files():
    rd = ROOT / "references"
    assert rd.is_dir(), "缺少 references/ 目录（渐进式披露）"
    for fn in REQUIRED_REFS:
        assert (rd / fn).is_file(), f"缺少 references/{fn}"


def test_skill_card_exists():
    assert (ROOT / "market-card.md").is_file(), "缺少 market-card.md（市场标准卡）"


def test_skill_card_has_known_risks():
    t = (ROOT / "market-card.md").read_text(encoding="utf-8")
    assert "Known Risks" in t or "风险" in t
    assert "Mitigation" in t or "缓解" in t


def test_readme_has_privacy_section():
    t = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "隐私" in t


def test_skill_md_has_privacy_clause():
    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "隐私" in t


def test_skill_md_is_lean():
    """渐进式披露后 SKILL.md 应显著精炼（原 365 行单体）。"""
    n = len((ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines())
    assert n < 260, f"SKILL.md 仍过长：{n} 行（应拆分到 references/）"


def test_skill_md_links_references():
    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for fn in REQUIRED_REFS:
        assert f"references/{fn}" in t, f"SKILL.md 未链接 references/{fn}"
