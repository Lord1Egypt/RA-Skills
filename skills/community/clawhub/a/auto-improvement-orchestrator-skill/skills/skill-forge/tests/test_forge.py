"""Tests for forge.py CLI — integration tests for both modes."""

import pytest
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.forge import handle_from_skill, handle_from_spec
from interfaces.spec_schema import SkillSpec


class TestForgeFromSkill:
    """Test --from-skill mode (generate task suite for existing skill)."""

    def test_generates_task_suite_yaml(self, tmp_path):
        # Create a minimal skill
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: does stuff\n---\n"
            "# My Skill\n## When to Use\n- When doing stuff\n"
        )

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create a namespace mock for args
        class Args:
            mock = True
            evaluate = False
            auto_improve = False

        result = handle_from_skill(skill_dir, output_dir, Args())
        assert result == 0

        # Check output file exists
        suite_file = output_dir / "task_suite.yaml"
        assert suite_file.exists()

        # Check it's valid YAML
        suite = yaml.safe_load(suite_file.read_text())
        assert suite["skill_id"] == "my-skill"
        assert len(suite["tasks"]) >= 1

    def test_output_is_valid_yaml(self, tmp_path):
        skill_dir = tmp_path / "yaml-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: yaml-test\ndescription: tests yaml output\n---\n"
            "## When to Use\n- Testing YAML validity\n"
        )

        output_dir = tmp_path / "out"
        output_dir.mkdir()

        class Args:
            mock = True
            evaluate = False
            auto_improve = False

        handle_from_skill(skill_dir, output_dir, Args())

        suite_file = output_dir / "task_suite.yaml"
        # Should not raise
        suite = yaml.safe_load(suite_file.read_text())
        assert isinstance(suite, dict)
        assert "tasks" in suite
        for task in suite["tasks"]:
            assert isinstance(task, dict)

    def test_fails_for_nonexistent_dir(self, tmp_path):
        class Args:
            mock = True
            evaluate = False
            auto_improve = False

        result = handle_from_skill(
            tmp_path / "nonexistent", tmp_path, Args()
        )
        assert result == 1

    def test_fails_for_missing_skill_md(self, tmp_path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        class Args:
            mock = True
            evaluate = False
            auto_improve = False

        result = handle_from_skill(empty_dir, tmp_path, Args())
        assert result == 1


class TestForgeFromSpec:
    """Test --from-spec mode (generate skill + task suite from spec)."""

    def test_generates_skill_directory(self, tmp_path):
        spec_file = tmp_path / "spec.yaml"
        spec_file.write_text(
            yaml.dump(
                {
                    "name": "new-skill",
                    "purpose": "Test new skill generation",
                    "inputs": [
                        {"name": "data", "description": "input data"}
                    ],
                    "outputs": [
                        {"name": "report", "format": "markdown"}
                    ],
                }
            )
        )

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        class Args:
            mock = True
            evaluate = False
            auto_improve = False

        result = handle_from_spec(spec_file, output_dir, Args())
        assert result == 0

        # Check skill directory was created
        skill_dir = output_dir / "new-skill"
        assert skill_dir.is_dir()
        assert (skill_dir / "SKILL.md").exists()
        assert (skill_dir / "task_suite.yaml").exists()

    def test_generated_skill_has_frontmatter(self, tmp_path):
        spec_file = tmp_path / "spec.yaml"
        spec_file.write_text(
            yaml.dump(
                {
                    "name": "fm-test",
                    "purpose": "Test frontmatter generation",
                }
            )
        )

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        class Args:
            mock = True
            evaluate = False
            auto_improve = False

        handle_from_spec(spec_file, output_dir, Args())

        skill_md = (output_dir / "fm-test" / "SKILL.md").read_text()
        assert skill_md.startswith("---")
        assert "name: fm-test" in skill_md

    def test_fails_for_invalid_spec(self, tmp_path):
        spec_file = tmp_path / "bad.yaml"
        spec_file.write_text(yaml.dump({"name": "", "purpose": ""}))

        class Args:
            mock = True
            evaluate = False
            auto_improve = False

        result = handle_from_spec(spec_file, tmp_path, Args())
        assert result == 1

    def test_fails_for_missing_spec(self, tmp_path):
        class Args:
            mock = True
            evaluate = False
            auto_improve = False

        result = handle_from_spec(
            tmp_path / "nonexistent.yaml", tmp_path, Args()
        )
        assert result == 1


class TestSpecSchema:
    """Test SkillSpec validation."""

    def test_valid_spec(self, tmp_path):
        spec_file = tmp_path / "valid.yaml"
        spec_file.write_text(
            yaml.dump({"name": "test", "purpose": "Test skill"})
        )
        spec = SkillSpec.from_yaml(spec_file)
        assert spec.validate() == []

    def test_missing_name(self, tmp_path):
        spec_file = tmp_path / "no_name.yaml"
        spec_file.write_text(yaml.dump({"name": "", "purpose": "Test"}))
        spec = SkillSpec.from_yaml(spec_file)
        errors = spec.validate()
        assert any("name" in e for e in errors)

    def test_missing_purpose(self, tmp_path):
        spec_file = tmp_path / "no_purpose.yaml"
        spec_file.write_text(yaml.dump({"name": "test", "purpose": ""}))
        spec = SkillSpec.from_yaml(spec_file)
        errors = spec.validate()
        assert any("purpose" in e for e in errors)

    def test_name_too_long(self, tmp_path):
        spec_file = tmp_path / "long_name.yaml"
        spec_file.write_text(
            yaml.dump({"name": "a" * 51, "purpose": "Test"})
        )
        spec = SkillSpec.from_yaml(spec_file)
        errors = spec.validate()
        assert any("too long" in e for e in errors)

    def test_loads_all_fields(self, tmp_path):
        spec_file = tmp_path / "full.yaml"
        spec_file.write_text(
            yaml.dump(
                {
                    "name": "full-test",
                    "purpose": "Full test",
                    "inputs": [{"name": "a"}],
                    "outputs": [{"name": "b"}],
                    "quality_criteria": [{"name": "c"}],
                    "domain_knowledge": ["fact1"],
                    "reference_skills": ["skill1"],
                }
            )
        )
        spec = SkillSpec.from_yaml(spec_file)
        assert spec.name == "full-test"
        assert len(spec.inputs) == 1
        assert len(spec.outputs) == 1
        assert len(spec.quality_criteria) == 1
        assert spec.domain_knowledge == ["fact1"]
        assert spec.reference_skills == ["skill1"]
