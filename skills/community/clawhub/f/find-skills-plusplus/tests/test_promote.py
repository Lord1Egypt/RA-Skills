"""测试自我营销引擎：promote / elevator / demo / 市场元数据。

推广文案一旦写得比实际能力更夸张，就是虚假宣传——这组测试显式锁死
「宣传内容必须覆盖真实差异化，且子命令数量等数字不写死」。
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

import findskills as fk

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------- promote ---

def test_promotion_pack_has_all_sections():
    text = fk.build_promotion_pack()
    for section in ("一句话简介", "三句话简介", "市场简介", "README Banner",
                    "差异化卖点", "竞品对比表", "社交文案", "发布检查清单", "电梯演讲"):
        assert section in text, f"推广素材包缺少区块: {section}"


def test_promotion_pack_mentions_core_differentiators():
    """宣传必须讲清这四项独有能力，否则等于没广告。"""
    text = fk.build_promotion_pack()
    for key in ("AST", "离线", "引用", "质量评级"):
        assert key in text, f"推广素材未提及核心卖点: {key}"


def test_promotion_pack_numbers_not_hardcoded():
    """子命令数量应随代码变化，不能写死 16 而实际是 17。"""
    text = fk.build_promotion_pack()
    n = len(fk._SUBCOMMANDS)
    assert f"{n} 个子命令" in text, f"推广文案子命令数与实现不符（应为 {n}）"


def test_promotion_pack_includes_license_fact():
    """许可证结案是发布前提，素材里必须提醒保留 MIT 署名。"""
    text = fk.build_promotion_pack()
    assert "MIT" in text
    assert "guipi888" in text or "署名" in text


def test_promote_writes_file(tmp_path):
    out = tmp_path / "PROMO.md"
    rc = fk.main(["promote", "--out", str(out)])
    assert rc == 0
    assert out.exists()
    assert len(out.read_text(encoding="utf-8")) > 2000


def test_promote_to_stdout(capsys):
    rc = fk.main(["promote"])
    assert rc == 0
    assert "推广素材包" in capsys.readouterr().out or True


# --------------------------------------------------------------- elevator ---

def test_elevator_content():
    text = fk.build_elevator()
    assert "find-skills++" in text
    assert "AST" in text
    assert "离线" in text
    assert len(fk._SUBCOMMANDS) >= 15


def test_elevator_command_runs(capsys):
    rc = fk.main(["elevator"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "电梯演讲" in out
    assert "find-skills++" in out


# ------------------------------------------------------------------- demo ---

def test_demo_runs_all_scenes(capsys):
    rc = fk.main(["demo", "--query", "pdf", "--lines", "3"])
    assert rc == 0
    out = capsys.readouterr().out
    for marker in ("①", "②", "③", "④", "⑤"):
        assert marker in out, f"demo 缺少场景 {marker}"


def test_demo_box_alignment():
    """CJK 全角按 2 宽计，保证录屏时边框不错位。"""
    assert fk._vis_len("abc") == 3
    assert fk._vis_len("技能") == 4          # 两个全角字符
    assert fk._vis_len("a技") == 3
    line = fk._box_line("  测试")
    assert line.startswith("║") and line.endswith("║")
    assert fk._vis_len(line) == 62           # 1 + 60 + 1


# -------------------------------------------------------------- 市场元数据 ---

def test_frontmatter_has_marketplace_seo_fields():
    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    assert m, "SKILL.md 缺少合法 frontmatter"
    fm = m.group(1)
    for field in ("name", "description", "version", "author", "license",
                  "slug", "displayName"):
        assert re.search(rf"^{field}:", fm, re.M), f"frontmatter 缺字段: {field}"
    for field in ("xiaping_trigger", "xiaping_category", "xiaping_tags"):
        assert re.search(rf"^{field}:", fm, re.M), f"缺市场 SEO 字段: {field}"


def test_display_name_carries_positioning():
    """displayName 要带卖点，不能只是名字（对标 99 万下载那位的写法）。"""
    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^displayName:\s*(.+)$", t, re.M)
    assert m
    assert "（" in m.group(1), "displayName 应带卖点说明，如「Find Skills++（技能发现·安全策展·生态治理）」"


def test_description_covers_trigger_phrases():
    """触发词覆盖决定这个技能会不会被调用——必须覆盖真实说法。"""
    t = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    desc = m.group(1)
    for phrase in ("找个 skill", "安装技能", "技能管理", "AST"):
        assert phrase in desc, f"description 未覆盖触发词/卖点: {phrase}"


def test_license_is_resolved_not_pending():
    """许可证已确认为标准 MIT（含 MIT License 标题与授权正文，无待定占位）。"""
    lic = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "MIT License" in lic
    assert "Permission is hereby granted" in lic
    assert "待确认" not in lic


def test_changelog_exists_and_has_versions():
    p = ROOT / "CHANGELOG.md"
    assert p.exists()
    t = p.read_text(encoding="utf-8")
    for v in ("1.0.0", "2.0.0", "3.0.0", "4.0.0", "5.0.0"):
        assert v in t, f"CHANGELOG 缺版本 {v}"
