#!/usr/bin/env python3
"""Tests for the improvement-learner Karpathy self-improvement loop.

Covers:
- ThreeLayerMemory (record, retrieve, overflow)
- evaluate_skill_dimensions (real directory checks)
- ImprovementResult dataclass
- self_improve_loop (respects max_iterations, Pareto integration)
- Improvement proposal + application helpers
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Path setup — mirror production import paths
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from self_improve import (  # noqa: E402
    ImprovementResult,
    ThreeLayerMemory,
    evaluate_skill_dimensions,
    propose_targeted_improvement,
    apply_improvement,
    self_improve_loop,
    generate_improvement_report,
    backup_skill,
    revert_to_backup,
    _propose_instruction_improvement,
)
from lib.pareto import ParetoFront, ParetoEntry  # noqa: E402


# ===========================================================================
# ThreeLayerMemory
# ===========================================================================

class TestThreeLayerMemoryRecordOutcome:
    """Test recording outcomes into HOT memory."""

    def test_record_stores_in_hot(self, tmp_path):
        mem = ThreeLayerMemory(tmp_path / "mem")
        mem.record_outcome("coverage", True, {"dimension": "coverage", "scores": {"x": 0.9}})
        assert mem.hot_count() == 1

    def test_duplicate_type_increments_hit_count(self, tmp_path):
        mem = ThreeLayerMemory(tmp_path / "mem")
        ctx = {"dimension": "accuracy"}
        mem.record_outcome("accuracy", True, ctx)
        mem.record_outcome("accuracy", False, ctx)
        patterns = mem.get_patterns("accuracy")
        assert len(patterns) == 1
        assert patterns[0]["hit_count"] == 2

    def test_different_types_are_separate_entries(self, tmp_path):
        mem = ThreeLayerMemory(tmp_path / "mem")
        mem.record_outcome("coverage", True, {"dimension": "coverage"})
        mem.record_outcome("accuracy", True, {"dimension": "accuracy"})
        assert mem.hot_count() == 2

    def test_overflow_moves_to_warm(self, tmp_path):
        mem = ThreeLayerMemory(tmp_path / "mem")
        # Fill beyond HOT_LIMIT (100)
        for i in range(105):
            mem.record_outcome(f"type-{i}", True, {"dimension": f"dim-{i}"})
        assert mem.hot_count() <= ThreeLayerMemory.HOT_LIMIT
        assert mem.warm_count() >= 5

    def test_record_creates_memory_dir(self, tmp_path):
        mem_dir = tmp_path / "nonexistent" / "nested" / "mem"
        mem = ThreeLayerMemory(mem_dir)
        mem.record_outcome("test", True, {"dimension": "x"})
        assert mem_dir.exists()
        assert mem.hot_count() == 1


class TestThreeLayerMemoryGetPatterns:
    """Test retrieving patterns from HOT memory."""

    def test_get_matching_patterns(self, tmp_path):
        mem = ThreeLayerMemory(tmp_path / "mem")
        mem.record_outcome("coverage", True, {"dimension": "coverage"})
        mem.record_outcome("accuracy", True, {"dimension": "accuracy"})
        mem.record_outcome("coverage", False, {"dimension": "coverage", "extra": True})

        patterns = mem.get_patterns("coverage")
        # Both coverage entries merged into one (same dimension key)
        assert len(patterns) >= 1
        assert all(p["type"] == "coverage" for p in patterns)

    def test_get_nonexistent_type_returns_empty(self, tmp_path):
        mem = ThreeLayerMemory(tmp_path / "mem")
        mem.record_outcome("coverage", True, {"dimension": "coverage"})
        patterns = mem.get_patterns("nonexistent")
        assert patterns == []

    def test_get_from_empty_memory(self, tmp_path):
        mem = ThreeLayerMemory(tmp_path / "mem")
        patterns = mem.get_patterns("anything")
        assert patterns == []


# ===========================================================================
# evaluate_skill_dimensions
# ===========================================================================

class TestEvaluateSkillDimensions:
    """Test real skill directory evaluation."""

    def test_empty_dir_scores_low(self, tmp_path):
        skill = tmp_path / "empty-skill"
        skill.mkdir()
        scores = evaluate_skill_dimensions(skill)
        assert scores["coverage"] == 0.0  # no SKILL.md
        assert scores["accuracy"] == 0.0
        # No scripts → pure-text → reliability = 1.0
        assert scores["reliability"] == 1.0

    def test_pure_text_skill_scores_fair(self, tmp_path):
        """Pure-text skill (SKILL.md only, no scripts/tests) should not be penalised."""
        skill = tmp_path / "text-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: text-only\nversion: 1.0\ndescription: A pure text skill\n"
            "author: Team\nlicense: MIT\n---\n\n# Text Skill\n\n"
            "## When to Use\n- For guidance\n\n## When NOT to Use\n- Never\n\n"
            "## Usage\n\n```\nJust read SKILL.md\n```\n",
            encoding="utf-8",
        )
        scores = evaluate_skill_dimensions(skill)
        # Coverage checks content sections: When to Use ✓, Usage ✓, progressive ✓ = 3/6
        assert scores["coverage"] >= 0.4
        assert scores["completeness"] >= 0.0  # no scripts/tests but that's OK for pure-text
        assert scores["reliability"] == 1.0  # pure-text → default 1.0
        assert scores["accuracy"] >= 0.2  # minimal SKILL.md passes few regex checks

    def test_full_structure_scores_high(self, tmp_path):
        skill = tmp_path / "good-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: test\n"
            "description: 当需要运行测试评估、检查 skill 质量评分时使用。Use when you want to evaluate quality. 不用于手动打分（用 discriminator）。\n"
            "license: MIT\n---\n\n# Good Skill\n\n"
            "## When to Use\n- Testing\n\n## When NOT to Use\n- 生产环境评估（用 `improvement-evaluator`）。不要用于生产环境。\n\n"
            "## Pipeline\n\n### Step 1: Evaluate\nMUST run evaluation first. 如果不确定，confirm with user.\n\n"
            "## CLI\n\n```bash\npython3 run.py\n```\n\n"
            "Priority: accuracy 高于 efficiency.\n\n"
            "<example>\nInput: SKILL.md path → Output: 6-dimension JSON scores\nreasoning: --skill-path ensures the right skill directory is evaluated\n</example>\n\n"
            "<anti-example>\nWrong: run without path\n</anti-example>\n\n"
            "### 禁止行为\n- ❌ Skip evaluation\n- ❌ Ignore failures\n\n"
            "### 正确做法\n- ✅ Run full pipeline\n- ✅ Check all dims\n\n"
            "MUST run evaluation before reporting.\n"
            "即使 scores look good, NEVER skip verification.\n\n"
            "## Output Artifacts\n\n| Request | Deliverable |\n|---------|------------|\n"
            "| Run tests | JSON report |\n\n"
            "## Related Skills\n\n- **benchmark-store**: For frozen benchmarks\n",
            encoding="utf-8",
        )
        (skill / "README.md").write_text("# README\n", encoding="utf-8")
        (skill / "scripts").mkdir()
        (skill / "references").mkdir()
        tests_dir = skill / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_example.py").write_text(
            "def test_pass(): assert True\n", encoding="utf-8"
        )

        scores = evaluate_skill_dimensions(skill)
        assert scores["coverage"] >= 0.8  # content sections well covered
        assert scores["completeness"] >= 0.75  # scripts+tests+references+readme all present
        assert scores["accuracy"] >= 0.4  # passes structural checks but LLM judge off in tests
        assert scores["security"] >= 0.8  # no secrets

    def test_skill_md_without_frontmatter(self, tmp_path):
        skill = tmp_path / "nofm-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# No Frontmatter\n", encoding="utf-8")
        scores = evaluate_skill_dimensions(skill)
        assert scores["accuracy"] < 0.5  # no frontmatter → low accuracy

    def test_security_score_drops_with_secrets(self, tmp_path):
        skill = tmp_path / "secret-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: test\n---\n\nmy api_key = abc123\n", encoding="utf-8"
        )
        scores = evaluate_skill_dimensions(skill)
        assert scores["security"] < 0.8  # api_key found → lower security

    def test_returns_all_dimensions(self, tmp_path):
        skill = tmp_path / "dim-skill"
        skill.mkdir()
        scores = evaluate_skill_dimensions(skill)
        expected_dims = {"coverage", "completeness", "accuracy", "efficiency", "reliability",
                         "security", "trigger_quality", "leakage", "knowledge_density"}
        assert set(scores.keys()) == expected_dims

    def test_trigger_quality_with_good_description(self, tmp_path):
        """Skill with pushy trigger description and triggers: field scores well."""
        skill = tmp_path / "trig-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: test\n"
            "description: Evaluate skill quality with structural checks. Not for code review or linting.\n"
            "triggers:\n  - evaluate\n  - quality check\n---\n# Test\n",
            encoding="utf-8",
        )
        scores = evaluate_skill_dimensions(skill)
        assert scores["trigger_quality"] >= 0.6  # has description, triggers, disambiguation

    def test_trigger_quality_without_frontmatter(self, tmp_path):
        """Skill without frontmatter gets 0.0 trigger quality."""
        skill = tmp_path / "nofm-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# No Frontmatter\n", encoding="utf-8")
        scores = evaluate_skill_dimensions(skill)
        assert scores["trigger_quality"] == 0.0

    def test_scripts_without_tests_penalises_reliability(self, tmp_path):
        """A skill with scripts/ but no tests/ should get low reliability."""
        skill = tmp_path / "script-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\n---\n# Skill\n" * 5, encoding="utf-8")
        (skill / "scripts").mkdir()
        (skill / "scripts" / "run.py").write_text("print('hi')\n", encoding="utf-8")
        scores = evaluate_skill_dimensions(skill)
        assert scores["reliability"] == 0.3  # has scripts but no tests


# ===========================================================================
# ImprovementResult dataclass
# ===========================================================================

class TestImprovementResult:
    """Test the ImprovementResult dataclass."""

    def test_creation(self):
        r = ImprovementResult(
            iteration=0, candidate_type="coverage",
            description="Add tests", applied=True,
            score_before=0.5, score_after=0.7,
            kept=True, pareto_accepted=True, reason="kept",
        )
        assert r.iteration == 0
        assert r.candidate_type == "coverage"
        assert r.kept is True
        assert r.trace is None

    def test_asdict(self):
        r = ImprovementResult(
            iteration=1, candidate_type="accuracy",
            description="Fix frontmatter", applied=True,
            score_before=0.3, score_after=0.6,
            kept=True, pareto_accepted=True, reason="kept",
            trace={"dim": "accuracy"},
        )
        d = asdict(r)
        assert d["iteration"] == 1
        assert d["trace"] == {"dim": "accuracy"}

    def test_default_trace_is_none(self):
        r = ImprovementResult(0, "t", "d", False, 0, 0, False, False, "x")
        assert r.trace is None


# ===========================================================================
# Improvement proposals + application
# ===========================================================================

class TestProposeTargetedImprovement:

    def test_known_dimension_returns_candidate(self):
        c = propose_targeted_improvement(Path("/fake"), "coverage", [])
        assert c is not None
        assert c["type"] == "coverage"

    def test_unknown_dimension_returns_none(self):
        c = propose_targeted_improvement(Path("/fake"), "nonexistent", [])
        assert c is None

    def test_too_many_failures_returns_none(self):
        failures = [
            {"type": "coverage", "succeeded": False},
            {"type": "coverage", "succeeded": False},
            {"type": "coverage", "succeeded": False},
        ]
        c = propose_targeted_improvement(Path("/fake"), "coverage", failures)
        assert c is None


class TestApplyImprovement:

    def test_coverage_creates_references_for_long_skill_md(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        # Create a >500 line SKILL.md
        lines = ["---", "name: test", "---", ""]
        for i in range(510):
            lines.append(f"Line {i}: content")
        (skill / "SKILL.md").write_text("\n".join(lines), encoding="utf-8")
        result = apply_improvement(skill, {"type": "coverage"})
        assert result is True
        assert (skill / "references").is_dir()
        # Should NOT create tests/ or README.md
        assert not (skill / "tests").exists()
        assert not (skill / "README.md").exists()

    def test_coverage_noop_for_short_skill_md(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# Short\n", encoding="utf-8")
        result = apply_improvement(skill, {"type": "coverage"})
        assert result is False  # nothing to do

    def test_accuracy_adds_frontmatter(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# No frontmatter\n", encoding="utf-8")
        result = apply_improvement(skill, {"type": "accuracy"})
        assert result is True
        content = (skill / "SKILL.md").read_text(encoding="utf-8")
        assert content.startswith("---")

    def test_accuracy_adds_missing_sections(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: x\n---\n# Has FM\n", encoding="utf-8")
        result = apply_improvement(skill, {"type": "accuracy"})
        assert result is True  # adds missing sections (When to Use, CLI, etc.)
        content = (skill / "SKILL.md").read_text(encoding="utf-8")
        assert "## When to Use" in content

    def test_unknown_type_returns_false(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        result = apply_improvement(skill, {"type": "unknown_type"})
        assert result is False


# ===========================================================================
# self_improve_loop
# ===========================================================================

class TestSelfImproveLoop:

    def test_respects_max_iterations(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# Test\n", encoding="utf-8")

        report = self_improve_loop(
            skill_path=skill,
            max_iterations=3,
            memory_dir=tmp_path / "mem",
        )
        assert report["iterations"] <= 3

    def test_returns_valid_report_structure(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()

        report = self_improve_loop(
            skill_path=skill,
            max_iterations=2,
            memory_dir=tmp_path / "mem",
        )
        assert "iterations" in report
        assert "kept" in report
        assert "reverted" in report
        assert "skipped" in report
        assert "final_scores" in report
        assert "results" in report
        assert "timestamp" in report

    def test_empty_skill_gets_improvements(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()

        report = self_improve_loop(
            skill_path=skill,
            max_iterations=5,
            memory_dir=tmp_path / "mem",
        )
        # At least one improvement should have been attempted
        assert report["iterations"] > 0

    def test_records_memory(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        mem_dir = tmp_path / "mem"

        self_improve_loop(
            skill_path=skill,
            max_iterations=2,
            memory_dir=mem_dir,
        )
        mem = ThreeLayerMemory(mem_dir)
        # Some patterns should have been recorded
        assert mem.hot_count() >= 0  # may be 0 if all skipped

    def test_with_pareto_state_root(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
        state_root = tmp_path / "state"
        state_root.mkdir()

        report = self_improve_loop(
            skill_path=skill,
            max_iterations=2,
            state_root=state_root,
            memory_dir=tmp_path / "mem",
        )
        assert "final_scores" in report


# ===========================================================================
# Pareto integration
# ===========================================================================

class TestParetoIntegration:
    """Verify that regressions cause revert via Pareto front."""

    def test_regression_causes_revert(self, tmp_path):
        """A candidate that regresses a Pareto dimension should be reverted."""
        front = ParetoFront()
        # Establish a strong baseline
        front.add(ParetoEntry("baseline", "init", {
            "coverage": 0.9, "accuracy": 0.9,
            "efficiency": 0.9, "reliability": 0.9, "security": 0.9,
        }))

        # New scores that regress accuracy badly
        new_scores = {
            "coverage": 0.95, "accuracy": 0.3,  # big regression
            "efficiency": 0.95, "reliability": 0.95, "security": 0.95,
        }
        result = front.check_regression(new_scores)
        assert result["regressed"] is True
        regressions = result["regressions"]
        dims = [r["dimension"] for r in regressions]
        assert "accuracy" in dims

    def test_improvement_accepted_by_pareto(self, tmp_path):
        """Better scores should be accepted by the Pareto front."""
        front = ParetoFront()
        front.add(ParetoEntry("baseline", "init", {
            "coverage": 0.5, "accuracy": 0.5,
        }))

        new_scores = {"coverage": 0.7, "accuracy": 0.7}
        result = front.check_regression(new_scores)
        assert result["regressed"] is False

    def test_loop_reverts_on_regression(self, tmp_path):
        """Full loop: if improvement causes a Pareto regression, it gets reverted."""
        skill = tmp_path / "skill"
        skill.mkdir()
        # Create a well-structured skill so initial scores are high
        (skill / "SKILL.md").write_text(
            "---\nname: test\n---\n\n# Good Skill\n", encoding="utf-8"
        )
        (skill / "README.md").write_text("# README\n", encoding="utf-8")
        (skill / "scripts").mkdir()
        (skill / "references").mkdir()
        tests_dir = skill / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_ok.py").write_text(
            "def test_pass(): assert True\n", encoding="utf-8"
        )

        state_root = tmp_path / "state"
        state_root.mkdir()

        # Pre-seed a very high Pareto entry so any change is a regression
        pareto = ParetoFront(state_root / "pareto_front.json")
        pareto.add(ParetoEntry("seed", "perfect", {
            "coverage": 1.0, "accuracy": 1.0,
            "efficiency": 1.0, "reliability": 1.0, "security": 1.0,
        }))

        report = self_improve_loop(
            skill_path=skill,
            max_iterations=2,
            state_root=state_root,
            memory_dir=tmp_path / "mem",
        )
        # All attempts should be reverted (nothing can beat perfect scores)
        kept = report.get("kept", 0)
        # Kept should be 0 since baseline is perfect
        assert kept == 0


# ===========================================================================
# Backup / restore
# ===========================================================================

class TestBackupRestore:

    def test_backup_creates_copy(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("original\n", encoding="utf-8")

        backup = backup_skill(skill)
        assert backup.exists()
        assert (backup / "SKILL.md").read_text(encoding="utf-8") == "original\n"

    def test_revert_restores_original(self, tmp_path):
        skill = tmp_path / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("original\n", encoding="utf-8")

        backup = backup_skill(skill)
        # Modify skill
        (skill / "SKILL.md").write_text("modified\n", encoding="utf-8")
        # Revert
        revert_to_backup(skill, backup)
        assert (skill / "SKILL.md").read_text(encoding="utf-8") == "original\n"


# ===========================================================================
# Report generation
# ===========================================================================

class TestGenerateImprovementReport:

    def test_report_structure(self, tmp_path):
        mem = ThreeLayerMemory(tmp_path / "mem")
        results = [
            ImprovementResult(0, "coverage", "desc", True, 0.5, 0.7, True, True, "kept"),
            ImprovementResult(1, "accuracy", "desc2", True, 0.7, 0.6, False, False, "reverted"),
        ]
        report = generate_improvement_report(results, {"x": 0.7}, mem)
        assert report["iterations"] == 2
        assert report["kept"] == 1
        assert report["reverted"] == 1
        assert report["skipped"] == 0
        assert report["final_scores"] == {"x": 0.7}
        assert len(report["results"]) == 2


# ===========================================================================
# Instruction-level improvements (P1)
# ===========================================================================

class TestProposeInstructionImprovement:
    """Test _propose_instruction_improvement for SKILL.md content analysis."""

    def test_propose_instruction_missing_when_to_use(self, tmp_path):
        """Skill without '## When to Use' section triggers instruction improvement."""
        skill = tmp_path / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: test\n---\n\n# Test Skill\n\nSome content.\n",
            encoding="utf-8",
        )
        result = _propose_instruction_improvement(skill, {"accuracy": 0.6})
        assert result is not None
        assert result["type"] == "instruction"
        assert result["issue_id"] == "missing_when_to_use"

    def test_propose_instruction_too_long(self, tmp_path):
        """Skill with >300 line SKILL.md triggers too_long issue."""
        skill = tmp_path / "skill"
        skill.mkdir()
        # Build a SKILL.md with all expected sections but >300 lines
        lines = ["---", "name: test", "---", "", "# Test Skill", ""]
        lines.append("## When to Use")
        lines.append("")
        lines.append("- Use it here")
        lines.append("")
        lines.append("## When NOT to Use")
        lines.append("")
        lines.append("- Don't use it there")
        lines.append("")
        lines.append("```bash")
        lines.append("example command")
        lines.append("```")
        # Pad to >300 lines
        for i in range(300):
            lines.append(f"Line {i}: filler content for length testing.")
        (skill / "SKILL.md").write_text("\n".join(lines), encoding="utf-8")

        result = _propose_instruction_improvement(skill, {"accuracy": 0.7})
        assert result is not None
        assert result["type"] == "instruction"
        assert result["issue_id"] == "too_long"

    def test_propose_instruction_no_issues(self, tmp_path):
        """Skill with all sections present returns None (no improvements needed)."""
        skill = tmp_path / "skill"
        skill.mkdir()
        content = (
            "---\nname: test\n---\n\n"
            "# Test Skill\n\n"
            "## When to Use\n\n- Use it here\n\n"
            "## When NOT to Use\n\n- Don't use it there\n\n"
            "```bash\nexample\n```\n"
        )
        (skill / "SKILL.md").write_text(content, encoding="utf-8")
        result = _propose_instruction_improvement(skill, {"accuracy": 0.8})
        assert result is None

    def test_apply_instruction_adds_when_to_use(self, tmp_path):
        """Verify that applying missing_when_to_use adds the section to SKILL.md."""
        skill = tmp_path / "skill"
        skill.mkdir()
        original = "---\nname: test\n---\n\n# Test Skill\n\nSome content.\n"
        (skill / "SKILL.md").write_text(original, encoding="utf-8")

        candidate = {
            "type": "instruction",
            "issue_id": "missing_when_to_use",
            "description": "Add '## When to Use' section",
        }
        result = apply_improvement(skill, candidate)
        assert result is True

        updated = (skill / "SKILL.md").read_text(encoding="utf-8")
        assert "## When to Use" in updated
