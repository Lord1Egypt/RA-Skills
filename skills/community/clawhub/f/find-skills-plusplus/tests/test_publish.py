"""测试发布就绪校验器 `publish`。

核心是「上架闸门」：上架前必须把市场门槛逐项查清楚，缺一项就拦。
用临时技能目录验证各项校验逻辑（--no-smoke 跳过完整冒烟，保持测试快且独立）。
"""

from __future__ import annotations

from pathlib import Path

import pytest

import findskills as fk


def _write_skill(d: Path, *, with_license=True, with_card=True, fm_extra="",
                 readme="", scripts=None, extra_md=None):
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(
        "---\nname: demo-skill\nversion: 1.0.0\nauthor: Tester\n"
        "license: MIT\ndescription: 用于测试的干净技能\n"
        f"metadata:\n  slug: demo-skill\n  displayName: Demo Skill（测试）\n{fm_extra}---\n"
        "# Demo\n\n一个干净样例。\n", encoding="utf-8")
    if with_license:
        (d / "LICENSE").write_text("MIT License\n", encoding="utf-8")
    if with_card:
        (d / "market-card.md").write_text("# Demo Skill Card\n", encoding="utf-8")
    (d / "README.md").write_text(readme or "# Demo\n\n干净技能。\n", encoding="utf-8")
    if scripts:
        sd = d / "scripts"
        sd.mkdir(exist_ok=True)
        for name, content in scripts.items():
            (sd / name).write_text(content, encoding="utf-8")
    if extra_md:
        for name, content in extra_md.items():
            (d / name).write_text(content, encoding="utf-8")


def test_publish_clean_skill_passes():
    d = Path(__file__).resolve().parent.parent / ".tmp-pub" / "clean"
    _write_skill(d)
    rc = fk.main(["publish", "--path", str(d), "--no-smoke"])
    assert rc == 0


def test_publish_missing_license_fails():
    d = Path(__file__).resolve().parent.parent / ".tmp-pub" / "nolic"
    _write_skill(d, with_license=False)
    rc = fk.main(["publish", "--path", str(d), "--no-smoke"])
    assert rc == 2


def test_publish_missing_frontmatter_field_fails():
    d = Path(__file__).resolve().parent.parent / ".tmp-pub" / "nofm"
    # 缺 license 字段（fm_extra 不补，且把 license 从 frontmatter 去掉）
    _write_skill(d, fm_extra="")
    # 直接改写 SKILL.md 去掉 license 行
    sk = d / "SKILL.md"
    lines = [l for l in sk.read_text(encoding="utf-8").splitlines() if not l.startswith("license:")]
    sk.write_text("\n".join(lines) + "\n", encoding="utf-8")
    rc = fk.main(["publish", "--path", str(d), "--no-smoke"])
    assert rc == 2


def test_publish_readme_placeholder_fails():
    d = Path(__file__).resolve().parent.parent / ".tmp-pub" / "ph"
    _write_skill(d, readme="# Demo\n\nclone: https://github.com/<你的用户名>/demo\n")
    rc = fk.main(["publish", "--path", str(d), "--no-smoke"])
    assert rc == 2


def test_publish_hardcoded_path_fails():
    d = Path(__file__).resolve().parent.parent / ".tmp-pub" / "hard"
    _write_skill(d, scripts={"run.py": "open('C:\\\\Users\\\\x\\\\secret.txt').read()\n"})
    rc = fk.main(["publish", "--path", str(d), "--no-smoke"])
    assert rc == 2


def test_publish_missing_skill_card_is_warn_not_block():
    d = Path(__file__).resolve().parent.parent / ".tmp-pub" / "nocard"
    _write_skill(d, with_card=False)
    rc = fk.main(["publish", "--path", str(d), "--no-smoke"])
    # 缺 market-card 是 WARN（不阻塞），纯警告返回 0（非 strict）
    assert rc == 0


def test_publish_strict_mode_fails_on_warn():
    d = Path(__file__).resolve().parent.parent / ".tmp-pub" / "nocard2"
    _write_skill(d, with_card=False)
    rc = fk.main(["publish", "--path", str(d), "--no-smoke", "--strict"])
    assert rc == 1


def test_publish_secrets_warn():
    d = Path(__file__).resolve().parent.parent / ".tmp-pub" / "secret"
    _write_skill(d, scripts={"cfg.py": "TOKEN = 'sk-' + 'a'*24 + 'b'*4  # 24+ chars\n"})
    rc = fk.main(["publish", "--path", str(d), "--no-smoke"])
    # 疑似的密钥是 WARN，不阻塞（rc 0）
    assert rc == 0
