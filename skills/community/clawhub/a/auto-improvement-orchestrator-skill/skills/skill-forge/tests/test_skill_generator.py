"""Tests for skill_generator — SKILL.md generation from spec."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.skill_generator import (
    generate_skill_from_spec,
    derive_triggers,
    derive_description,
)


class TestGenerateSkillFromSpec:
    def test_basic_generation(self):
        spec = {
            "name": "test-skill",
            "purpose": "Test things",
            "inputs": [{"name": "code", "description": "source code to test"}],
            "outputs": [{"name": "report", "format": "markdown"}],
        }
        result = generate_skill_from_spec(spec)
        assert "---" in result
        assert "name: test-skill" in result
        assert "When to Use" in result
        assert "When NOT to Use" in result
        assert "Output Artifacts" in result

    def test_includes_domain_knowledge(self):
        spec = {
            "name": "test-skill",
            "purpose": "Test things",
            "domain_knowledge": ["Fact one", "Fact two"],
        }
        result = generate_skill_from_spec(spec)
        assert "Domain Knowledge" in result
        assert "Fact one" in result
        assert "Fact two" in result

    def test_includes_quality_criteria_examples(self):
        spec = {
            "name": "test-skill",
            "purpose": "Test things",
            "quality_criteria": [
                {"name": "accuracy", "description": "Must be accurate"},
            ],
        }
        result = generate_skill_from_spec(spec)
        assert "<example>" in result
        assert "<anti-example>" in result
        assert "accuracy" in result.lower() or "accurate" in result.lower()

    def test_includes_reference_skills(self):
        spec = {
            "name": "test-skill",
            "purpose": "Test things",
            "reference_skills": ["other-skill", "another-skill"],
        }
        result = generate_skill_from_spec(spec)
        assert "Related Skills" in result
        assert "other-skill" in result

    def test_minimal_spec(self):
        spec = {"name": "minimal", "purpose": "Do minimal things"}
        result = generate_skill_from_spec(spec)
        assert "---" in result
        assert "name: minimal" in result
        assert "Do minimal things" in result

    def test_title_formatting(self):
        spec = {"name": "my-cool-skill", "purpose": "Be cool"}
        result = generate_skill_from_spec(spec)
        assert "# My Cool Skill" in result

    def test_empty_inputs_fallback(self):
        spec = {"name": "test", "purpose": "Do testing work"}
        result = generate_skill_from_spec(spec)
        assert "When to Use" in result
        # Should use purpose-based fallback
        assert "do testing work" in result.lower()


class TestDeriveTriggers:
    def test_includes_name(self):
        triggers = derive_triggers("my-skill", "analyze code quality")
        assert "my-skill" in triggers

    def test_includes_name_without_hyphens(self):
        triggers = derive_triggers("my-skill", "analyze code quality")
        assert "my skill" in triggers

    def test_filters_short_words(self):
        triggers = derive_triggers("test", "do it now")
        # "do", "it", "now" are all <= 3 chars
        assert len(triggers) <= 2  # just name variants

    def test_max_six_triggers(self):
        triggers = derive_triggers(
            "test",
            "word1234 word2345 word3456 word4567 word5678 word6789 word7890",
        )
        assert len(triggers) <= 6

    def test_deduplicates(self):
        triggers = derive_triggers("analyze", "Analyze things carefully")
        # "analyze" appears in both name and purpose
        assert triggers.count("analyze") <= 1

    def test_filters_stop_words(self):
        triggers = derive_triggers("test", "this that with from into")
        # All purpose words are stop words
        assert len(triggers) <= 2  # just name + "test"


class TestDeriveDescription:
    def test_with_inputs(self):
        desc = derive_description(
            "Analyze code",
            [{"description": "source code"}, {"description": "config file"}],
        )
        assert "Analyze code" in desc
        assert "source code" in desc

    def test_without_inputs(self):
        desc = derive_description("Analyze code", [])
        assert desc == "Analyze code"

    def test_truncates_long_input_descriptions(self):
        desc = derive_description(
            "Test",
            [{"description": "a" * 100}],
        )
        # Should truncate at 30 chars
        assert len(desc) < 150
