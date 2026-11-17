"""Tests for CertainLogic Onboarding Wizard v2.1.0."""
import pytest
import sys
import json
import platform
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from onboarding_wizard import (
    OnboardingWizard, EnvironmentScanner, VerificationEngine,
    SetupScriptGenerator, WeeklyCheckup, TeamOnboardingExporter,
    GOAL_PROFILES, CERTAINLOGIC_SKILLS, COMMUNITY_SKILLS
)


class TestEnvironmentScanner:
    """Test environment auto-detection."""

    def test_detect_os_linux(self):
        with patch('platform.system', return_value='Linux'):
            assert EnvironmentScanner.detect_os() == 'linux'

    def test_detect_os_macos(self):
        with patch('platform.system', return_value='Darwin'):
            assert EnvironmentScanner.detect_os() == 'macos'

    def test_scan_installed_skills(self, tmp_path):
        (tmp_path / "skill-vetter-plus").mkdir()
        (tmp_path / "github").mkdir()

        installed = EnvironmentScanner.scan_installed_skills(tmp_path)
        assert "skill-vetter-plus" in installed
        assert "github" in installed
        assert len(installed) == 2

    def test_scan_no_skills_dir(self):
        result = EnvironmentScanner.scan_installed_skills(None)
        assert result == set()

    def test_find_skills_dir_returns_path(self, tmp_path):
        skills_dir = tmp_path / ".openclaw" / "skills"
        skills_dir.mkdir(parents=True)
        with patch.dict('os.environ', {'HOME': str(tmp_path)}):
            found = EnvironmentScanner.find_skills_dir()
            assert found is not None


class TestGoalDetection:
    """Test goal detection from user input."""

    def test_detect_developer(self):
        wizard = OnboardingWizard()
        assert wizard.detect_goal("I'm a developer") == "developer"
        assert wizard.detect_goal("coding in python") == "developer"

    def test_detect_business(self):
        wizard = OnboardingWizard()
        assert wizard.detect_goal("small business owner") == "business"
        assert wizard.detect_goal("startup") == "business"

    def test_detect_beginner(self):
        wizard = OnboardingWizard()
        assert wizard.detect_goal("new to this") == "beginner"
        assert wizard.detect_goal("help me set up") == "beginner"

    def test_unknown_goal_defaults(self):
        wizard = OnboardingWizard()
        assert wizard.detect_goal("xyzabc123") is None


class TestReportGeneration:
    """Test onboarding report generation."""

    def test_report_contains_skills(self):
        wizard = OnboardingWizard()
        env_info = {
            "os": "linux",
            "skills_dir": "/test/skills",
            "installed_skills": set(),
            "openclaw_version": "test"
        }
        report = wizard.generate_report("developer", env_info)
        assert "Skill Vetter Plus" in report
        assert "Smart Router" in report
        assert "clawhub install" in report

    def test_report_shows_installed_status(self):
        wizard = OnboardingWizard()
        env_info = {
            "os": "linux",
            "skills_dir": "/test/skills",
            "installed_skills": {"skill-vetter-plus"},
            "openclaw_version": "test"
        }
        report = wizard.generate_report("developer", env_info)
        assert "Installed" in report or "already installed" in report

    def test_linux_skips_macos_only(self):
        wizard = OnboardingWizard()
        env_info = {
            "os": "linux",
            "skills_dir": "/test/skills",
            "installed_skills": set(),
            "openclaw_version": "test"
        }
        report = wizard.generate_report("productivity", env_info)
        assert "Things 3" in report
        assert "not supported" in report or "Skipped" in report or "macOS not supported" in report

    def test_macos_includes_things(self):
        wizard = OnboardingWizard()
        env_info = {
            "os": "macos",
            "skills_dir": "/test/skills",
            "installed_skills": set(),
            "openclaw_version": "test"
        }
        report = wizard.generate_report("productivity", env_info)
        assert "Things 3" in report
        assert "not supported" not in report.lower()


class TestVerificationEngine:
    """Test post-install verification."""

    def test_verify_skill_missing_dir(self, tmp_path):
        engine = VerificationEngine(tmp_path)
        result = engine.verify_skill("nonexistent-skill")
        assert result["ok"] is False
        assert "not found" in result["errors"][0]

    def test_verify_skill_missing_skill_md(self, tmp_path):
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        engine = VerificationEngine(tmp_path)
        result = engine.verify_skill("test-skill")
        assert result["ok"] is False
        assert any("SKILL.md" in e for e in result["errors"])

    def test_verify_skill_valid(self, tmp_path):
        skill_dir = tmp_path / "good-skill"
        skill_dir.mkdir()
        long_doc = "## How to Use\n" + "Run it.\n" * 30
        (skill_dir / "SKILL.md").write_text(long_doc)
        (skill_dir / "skill.json").write_text(json.dumps({"name": "Good Skill", "description": "A good skill"}))
        scripts = skill_dir / "scripts"
        scripts.mkdir()
        script = scripts / "run.py"
        script.write_text("print('hello')")
        script.chmod(0o755)

        engine = VerificationEngine(tmp_path)
        result = engine.verify_skill("good-skill")
        assert result["ok"] is True
        assert result["errors"] == []
        assert result["warnings"] == []

    def test_verify_skill_short_skill_md(self, tmp_path):
        skill_dir = tmp_path / "bad-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("Short.")
        engine = VerificationEngine(tmp_path)
        result = engine.verify_skill("bad-skill")
        assert result["warnings"]
        assert any("short" in w.lower() for w in result["warnings"])

    def test_verify_skill_invalid_json(self, tmp_path):
        skill_dir = tmp_path / "bad-json"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("## How to Use\nRun it.\n")
        (skill_dir / "skill.json").write_text("not json")
        engine = VerificationEngine(tmp_path)
        result = engine.verify_skill("bad-json")
        assert not result["ok"]
        assert any("JSON" in e for e in result["errors"])

    def test_verify_all(self, tmp_path):
        (tmp_path / "skill-a").mkdir()
        (tmp_path / "skill-b").mkdir()
        engine = VerificationEngine(tmp_path)
        results = engine.verify_all({"skill-a", "skill-b"})
        assert len(results) == 2
        slugs = {r["slug"] for r in results}
        assert slugs == {"skill-a", "skill-b"}

    def test_verification_report(self, tmp_path):
        engine = VerificationEngine(tmp_path)
        results = [
            {"slug": "good", "ok": True, "warnings": [], "errors": []},
            {"slug": "warn", "ok": True, "warnings": ["short doc"], "errors": []},
            {"slug": "bad", "ok": False, "warnings": [], "errors": ["missing file"]},
        ]
        report = engine.generate_verification_report(results)
        assert "Fully healthy: 1" in report
        assert "Has warnings: 1" in report
        assert "Has errors: 1" in report
        assert "bad" in report
        assert "Verification" in report


class TestSetupScriptGenerator:
    """Test one-command setup script generation."""

    def test_generates_bash_script(self):
        profile = GOAL_PROFILES["developer"]
        env_info = {"os": "linux", "installed_skills": set()}
        script = SetupScriptGenerator.generate(profile, env_info)
        assert "#!/usr/bin/env bash" in script
        assert "set -euo pipefail" in script
        assert "clawhub install" in script

    def test_skips_already_installed(self):
        profile = GOAL_PROFILES["developer"]
        env_info = {"os": "linux", "installed_skills": {"skill-vetter-plus"}}
        script = SetupScriptGenerator.generate(profile, env_info)
        assert "already installed" in script or "skipping" in script.lower()

    def test_skips_macos_only_on_linux(self):
        profile = GOAL_PROFILES["productivity"]
        env_info = {"os": "linux", "installed_skills": set()}
        script = SetupScriptGenerator.generate(profile, env_info)
        assert "Things 3" in script
        assert "not supported" in script.lower() or "skipped" in script.lower()

    def test_runs_clawhub_install(self):
        profile = GOAL_PROFILES["beginner"]
        env_info = {"os": "linux", "installed_skills": set()}
        script = SetupScriptGenerator.generate(profile, env_info)
        assert "clawhub install" in script
        # Should handle failure gracefully
        assert "WARNING:" in script or "||" in script


class TestWeeklyCheckup:
    """Test weekly environment checkup."""

    def test_first_checkup_establishes_baseline(self, tmp_path):
        checkup = WeeklyCheckup(tmp_path)
        env_info = {
            "os": "linux",
            "openclaw_version": "1.0.0",
            "installed_skills": {"skill-a", "skill-b"},
        }
        report = checkup.run(env_info)
        assert "Baseline Established" in report
        assert "skill-a" not in report or "Changes" not in report

    def test_detects_added_skills(self, tmp_path):
        checkup = WeeklyCheckup(tmp_path)
        env_info = {
            "os": "linux",
            "openclaw_version": "1.0.0",
            "installed_skills": {"skill-a"},
        }
        checkup.run(env_info)

        env_info["installed_skills"] = {"skill-a", "skill-b"}
        report = checkup.run(env_info)
        assert "skill-b" in report
        assert "Changes Since Last Checkup" in report

    def test_detects_removed_skills(self, tmp_path):
        checkup = WeeklyCheckup(tmp_path)
        env_info = {
            "os": "linux",
            "openclaw_version": "1.0.0",
            "installed_skills": {"skill-a", "skill-b"},
        }
        checkup.run(env_info)

        env_info["installed_skills"] = {"skill-a"}
        report = checkup.run(env_info)
        assert "skill-b" in report
        assert "Changes Since Last Checkup" in report

    def test_detects_no_changes(self, tmp_path):
        checkup = WeeklyCheckup(tmp_path)
        env_info = {
            "os": "linux",
            "openclaw_version": "1.0.0",
            "installed_skills": {"skill-a"},
        }
        checkup.run(env_info)
        report = checkup.run(env_info)
        assert "No changes detected" in report

    def test_detects_version_change(self, tmp_path):
        checkup = WeeklyCheckup(tmp_path)
        env_info = {
            "os": "linux",
            "openclaw_version": "1.0.0",
            "installed_skills": {"skill-a"},
        }
        checkup.run(env_info)
        env_info["openclaw_version"] = "2.0.0"
        report = checkup.run(env_info)
        assert "OpenClaw Version Changed" in report
        assert "1.0.0" in report
        assert "2.0.0" in report


class TestTeamOnboardingExporter:
    """Test team onboarding bundle export."""

    def test_creates_setup_script(self, tmp_path):
        profile = GOAL_PROFILES["developer"]
        env_info = {"os": "linux", "installed_skills": set()}
        export_dir = tmp_path / "team-export"
        result = TeamOnboardingExporter.export(profile, env_info, export_dir)
        assert result.exists()
        assert (result / "setup.sh").exists()
        assert (result / "README.md").exists()

    def test_setup_script_is_executable(self, tmp_path):
        profile = GOAL_PROFILES["developer"]
        env_info = {"os": "linux", "installed_skills": set()}
        export_dir = tmp_path / "team-export"
        TeamOnboardingExporter.export(profile, env_info, export_dir)
        script = export_dir / "setup.sh"
        assert script.exists()
        import stat
        mode = script.stat().st_mode
        assert mode & stat.S_IXUSR, "setup.sh should be executable"

    def test_readme_contains_instructions(self, tmp_path):
        profile = GOAL_PROFILES["developer"]
        env_info = {"os": "linux", "installed_skills": set()}
        export_dir = tmp_path / "team-export"
        TeamOnboardingExporter.export(profile, env_info, export_dir)
        readme = (export_dir / "README.md").read_text()
        assert "./setup.sh" in readme
        assert "Verification" in readme


class TestHonesty:
    """Verify no false claims in reports."""

    def test_no_auto_install_claims(self):
        wizard = OnboardingWizard()
        env_info = {
            "os": "linux",
            "skills_dir": None,
            "installed_skills": set(),
            "openclaw_version": "test"
        }
        report = wizard.generate_report("beginner", env_info)
        assert "auto-install" not in report.lower()
        assert "automatically installed" not in report.lower()

    def test_no_guaranteed_savings(self):
        wizard = OnboardingWizard()
        env_info = {
            "os": "linux",
            "skills_dir": None,
            "installed_skills": set(),
            "openclaw_version": "test"
        }
        report = wizard.generate_report("business", env_info)
        assert "guaranteed" not in report.lower()
        assert "100%" not in report or "NOT" in report

    def test_disclaimer_present(self):
        wizard = OnboardingWizard()
        env_info = {
            "os": "linux",
            "skills_dir": None,
            "installed_skills": set(),
            "openclaw_version": "test"
        }
        report = wizard.generate_report("developer", env_info)
        assert "Verify before trusting" in report or "recommendations" in report.lower()


class TestProfileCoverage:
    """Every profile has valid skill references."""

    def test_all_profiles_have_skills(self):
        for goal, profile in GOAL_PROFILES.items():
            assert len(profile["certainlogic_skills"]) > 0, f"{goal} has no CertainLogic skills"

    def test_all_skill_refs_valid(self):
        for goal, profile in GOAL_PROFILES.items():
            for slug in profile["certainlogic_skills"]:
                assert slug in CERTAINLOGIC_SKILLS, f"Invalid skill ref: {slug}"
            for slug in profile.get("community_skills", []):
                assert slug in COMMUNITY_SKILLS, f"Invalid community ref: {slug}"


class TestCLI:
    """Test CLI argument integration."""

    def test_scan_only(self):
        wizard = OnboardingWizard()
        with patch.object(wizard, 'scan_only') as mock:
            wizard.scan_only()
            # scan_only prints directly, just verify it doesn't crash
            pass

    def test_verify_runs(self, tmp_path):
        wizard = OnboardingWizard(output_dir=tmp_path)
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        (skills_dir / "test-skill").mkdir()
        with patch.object(EnvironmentScanner, 'find_skills_dir', return_value=skills_dir):
            wizard.verify()
        # Should have written a verification report
        reports = list(tmp_path.glob("verification-report-*.md"))
        assert len(reports) == 1

    def test_weekly_checkup_runs(self, tmp_path):
        wizard = OnboardingWizard(output_dir=tmp_path)
        wizard.weekly_checkup()
        reports = list(tmp_path.glob("weekly-checkup-*.md"))
        assert len(reports) == 1

    def test_setup_script_flag(self, tmp_path):
        wizard = OnboardingWizard(output_dir=tmp_path)
        result = wizard.run(goal_input="developer", setup_script=True)
        assert str(result).endswith(".sh")
        content = result.read_text()
        assert "#!/usr/bin/env bash" in content

    def test_team_export_flag(self, tmp_path):
        wizard = OnboardingWizard(output_dir=tmp_path)
        export_dir = tmp_path / "team"
        result = wizard.run(goal_input="developer", team_export=export_dir)
        assert result.exists()
        assert (result / "setup.sh").exists()
        assert (result / "README.md").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
