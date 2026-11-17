"""Phase 3：环境感知的引用完整性（专治"引用了不存在工具"的假优）。"""
import tempfile
from pathlib import Path

import findskills


def _make(md_body, scripts=None):
    d = Path(tempfile.mkdtemp())
    (d / "SKILL.md").write_text(md_body, encoding="utf-8")
    if scripts:
        for name, body in scripts.items():
            p = d / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
    return d


def test_reference_dangling_lowers_score():
    d = _make("---\nname: bad\ndescription: d\n---\n见 scripts/missing.py 与 Skill(\"ghost\") 实现。\n")
    qf = findskills.gather_quality_fields(
        d, local_names=["real"], registry_names=["reg"])
    rep = findskills.rate_quality(qf)
    assert qf["ref_declared"] == 2
    assert qf["ref_local_missing"] + qf["ref_external_missing"] == 2
    assert rep["dims"]["reference_integrity"] == 0.0
    assert rep["score"] < 30  # 应被显著拉低


def test_reference_resolved_high():
    d = _make("---\nname: good\ndescription: d\n---\n见 scripts/ok.py 与 Skill(\"real\")。\n")
    (d / "scripts").mkdir()
    (d / "scripts" / "ok.py").write_text("print(1)\n", encoding="utf-8")
    qf = findskills.gather_quality_fields(
        d, local_names=["real"], registry_names=["reg"])
    rep = findskills.rate_quality(qf)
    assert qf["ref_declared"] == 2
    assert qf["ref_local_missing"] + qf["ref_external_missing"] == 0
    assert rep["dims"]["reference_integrity"] == 1.0


def test_no_reference_is_neutral():
    d = _make("---\nname: plain\ndescription: d\n---\n纯提示词技能。\n")
    qf = findskills.gather_quality_fields(d)
    rep = findskills.rate_quality(qf)
    assert qf["ref_declared"] == 0
    assert rep["dims"]["reference_integrity"] == 0.5
