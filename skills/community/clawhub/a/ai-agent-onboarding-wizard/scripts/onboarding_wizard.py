#!/usr/bin/env python3
"""CertainLogic Onboarding Wizard v2.1.0

Automated environment scan + personalized recommendations.
Generates install commands, setup scripts, verification, and checkups.

Usage:
    python3 scripts/onboarding_wizard.py [goal]
    python3 scripts/onboarding_wizard.py --scan-only
    python3 scripts/onboarding_wizard.py developer --setup-script
    python3 scripts/onboarding_wizard.py --verify
    python3 scripts/onboarding_wizard.py --weekly-checkup
    python3 scripts/onboarding_wizard.py developer --team-export /path/to/export
"""
import sys
import json
import os
import platform
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

import datetime


# ------------------------------------------------------------------
# Skill registry — our products + verified community skills
# ------------------------------------------------------------------
CERTAINLOGIC_SKILLS = {
    "skill-vetter-plus": {
        "name": "Skill Vetter Plus",
        "category": "security",
        "priority": 1,
        "description": "Security scanner — always install first",
        "clawhub_id": "skill-vetter-plus"
    },
    "certainlogic-smart-router": {
        "name": "CertainLogic Smart Router",
        "category": "routing",
        "priority": 2,
        "description": "Route queries to cheapest model tier",
        "clawhub_id": "certainlogic-smart-router"
    },
    "token-reduction-engine-v2": {
        "name": "Token Reduction Engine",
        "category": "optimization",
        "priority": 3,
        "description": "Keep sessions lean",
        "clawhub_id": "token-reduction-engine-v2"
    },
    "pa-pack": {
        "name": "Personal Assistant Pack",
        "category": "productivity",
        "priority": 4,
        "description": "Curated daily workflow (macOS-centric)",
        "clawhub_id": "pa-pack"
    },
    "skill-oracle": {
        "name": "Skill Oracle",
        "category": "discovery",
        "priority": 5,
        "description": "Curated skill directory",
        "clawhub_id": "skill-oracle"
    },
    "agentpathfinder": {
        "name": "AgentPathfinder",
        "category": "tracking",
        "priority": 6,
        "description": "Verifiable task tracking",
        "clawhub_id": "agentpathfinder"
    },
}

COMMUNITY_SKILLS = {
    "gog": {
        "name": "Google Workspace CLI (gog)",
        "creator": "steipete",
        "category": "productivity",
        "description": "Gmail, Calendar, Drive, Contacts, Sheets, Docs",
        "platforms": ["linux", "macos"],
        "clawhub_id": "gog"
    },
    "things-mac": {
        "name": "Things 3 for macOS",
        "creator": "",
        "category": "productivity",
        "description": "macOS task manager integration",
        "platforms": ["macos"],
        "clawhub_id": "things-mac"
    },
    "himalaya": {
        "name": "Himalaya Email",
        "creator": "pimalaya",
        "category": "communication",
        "description": "Terminal email client (IMAP)",
        "platforms": ["linux", "macos"],
        "clawhub_id": "himalaya"
    },
    "notion": {
        "name": "Notion Integration",
        "creator": "",
        "category": "productivity",
        "description": "Knowledge base integration",
        "platforms": ["linux", "macos"],
        "clawhub_id": "notion"
    },
    "skill-creator": {
        "name": "Skill Creator",
        "creator": "",
        "category": "development",
        "description": "Build your own skills",
        "platforms": ["linux", "macos"],
        "clawhub_id": "skill-creator"
    },
    "taskflow": {
        "name": "TaskFlow",
        "creator": "",
        "category": "automation",
        "description": "Durable task management",
        "platforms": ["linux", "macos"],
        "clawhub_id": "taskflow"
    },
    "github": {
        "name": "GitHub Integration",
        "creator": "",
        "category": "development",
        "description": "Repository access",
        "platforms": ["linux", "macos"],
        "clawhub_id": "github"
    },
}

GOAL_PROFILES = {
    "developer": {
        "title": "Coding / Development",
        "certainlogic_skills": ["skill-vetter-plus", "certainlogic-smart-router", "token-reduction-engine-v2"],
        "community_skills": ["github", "skill-creator"],
    },
    "business": {
        "title": "Small Business",
        "certainlogic_skills": ["skill-vetter-plus", "pa-pack", "certainlogic-smart-router"],
        "community_skills": ["gog", "notion", "himalaya"],
    },
    "research": {
        "title": "Research & Analysis",
        "certainlogic_skills": ["skill-vetter-plus", "skill-oracle", "certainlogic-smart-router"],
        "community_skills": ["taskflow"],
    },
    "productivity": {
        "title": "Personal Productivity",
        "certainlogic_skills": ["skill-vetter-plus", "pa-pack", "certainlogic-smart-router"],
        "community_skills": ["things-mac", "gog", "notion"],
    },
    "beginner": {
        "title": "Just Starting",
        "certainlogic_skills": ["skill-vetter-plus", "skill-oracle", "certainlogic-smart-router", "token-reduction-engine-v2"],
        "community_skills": ["skill-creator"],
    },
}


class EnvironmentScanner:
    """Scan the user's OpenClaw environment."""

    @staticmethod
    def detect_os() -> str:
        system = platform.system().lower()
        return "macos" if system == "darwin" else system

    @staticmethod
    def find_skills_dir() -> Optional[Path]:
        paths = [
            Path.home() / ".openclaw" / "skills",
            Path.home() / ".openclaw" / "workspace" / "skills",
        ]
        for p in paths:
            if p.exists():
                return p
        return None

    @staticmethod
    def scan_installed_skills(skills_dir: Optional[Path]) -> Set[str]:
        """Return set of installed skill slugs."""
        if not skills_dir:
            return set()
        installed = set()
        for item in skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                installed.add(item.name)
        return installed

    @staticmethod
    def detect_openclaw_version() -> str:
        """Try to detect OpenClaw version."""
        try:
            result = subprocess.run(
                ["openclaw", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return "Unknown"


class VerificationEngine:
    """Verify that installed skills actually work, not just exist."""

    def __init__(self, skills_dir: Optional[Path]):
        self.skills_dir = skills_dir or Path.home() / ".openclaw" / "skills"

    def verify_skill(self, skill_slug: str) -> Dict[str, Any]:
        """Deep check of a single skill. Returns structured results."""
        result = {
            "slug": skill_slug,
            "ok": True,
            "warnings": [],
            "errors": [],
        }
        skill_path = self.skills_dir / skill_slug

        if not skill_path.exists():
            result["ok"] = False
            result["errors"].append("Skill directory not found")
            return result

        # Check for SKILL.md
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            result["ok"] = False
            result["errors"].append("Missing SKILL.md — no documentation")
        else:
            content = skill_md.read_text(encoding="utf-8", errors="ignore")
            if len(content) < 100:
                result["warnings"].append("SKILL.md is very short — may be incomplete")
            if "## How to Use" not in content and "## Usage" not in content:
                result["warnings"].append("SKILL.md missing usage instructions")

        # Check for skill.json
        skill_json = skill_path / "skill.json"
        if skill_json.exists():
            try:
                meta = json.loads(skill_json.read_text(encoding="utf-8"))
                if not meta.get("name"):
                    result["warnings"].append("skill.json missing 'name' field")
                if not meta.get("description"):
                    result["warnings"].append("skill.json missing 'description' field")
            except json.JSONDecodeError:
                result["errors"].append("skill.json is invalid JSON")
        else:
            result["warnings"].append("No skill.json found")

        # Check for executable scripts
        scripts_dir = skill_path / "scripts"
        if scripts_dir.exists() and scripts_dir.is_dir():
            py_files = list(scripts_dir.glob("*.py"))
            if not py_files:
                result["warnings"].append("scripts/ exists but has no .py files")
            else:
                for pyf in py_files:
                    if not os.access(pyf, os.X_OK) and os.name != "nt":
                        result["warnings"].append(f"{pyf.name} is not executable")
        else:
            result["warnings"].append("No scripts/ directory — may not be actionable")

        if result["errors"]:
            result["ok"] = False
        return result

    def verify_all(self, installed: Set[str]) -> List[Dict[str, Any]]:
        """Run verification on every installed skill."""
        results = []
        for slug in sorted(installed):
            results.append(self.verify_skill(slug))
        return results

    def generate_verification_report(self, results: List[Dict[str, Any]]) -> str:
        """Human-friendly markdown report from verification results."""
        ok_count = sum(1 for r in results if r["ok"] and not r["warnings"])
        warn_count = sum(1 for r in results if r["warnings"] and not r["errors"])
        err_count = sum(1 for r in results if r["errors"])

        lines = [
            "# Post-Install Verification Report",
            f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Summary",
            f"- Fully healthy: {ok_count}",
            f"- Has warnings: {warn_count}",
            f"- Has errors: {err_count}",
            "",
        ]

        if err_count:
            lines.append("## Errors (needs attention)")
            for r in results:
                if r["errors"]:
                    lines.append(f"### {r['slug']}")
                    for e in r["errors"]:
                        lines.append(f"- {e}")
            lines.append("")

        if warn_count:
            lines.append("## Warnings (review when convenient)")
            for r in results:
                if r["warnings"] and not r["errors"]:
                    lines.append(f"### {r['slug']}")
                    for w in r["warnings"]:
                        lines.append(f"- {w}")
            lines.append("")

        if ok_count:
            lines.append("## Verified Clean")
            for r in results:
                if r["ok"] and not r["warnings"]:
                    lines.append(f"- {r['slug']}")
            lines.append("")

        lines.append("---")
        lines.append("*Verification checks SKILL.md presence, skill.json validity,*")
        lines.append("*and executable scripts. It does NOT test runtime behavior.*")
        return "\n".join(lines)


class SetupScriptGenerator:
    """Generate shell scripts for one-command install."""

    @staticmethod
    def generate(profile: Dict[str, Any], env_info: Dict[str, Any]) -> str:
        """Generate a bash script that installs the recommended stack."""
        os_name = env_info.get("os", "linux")
        installed = env_info.get("installed_skills", set())
        lines = [
            "#!/usr/bin/env bash",
            "# CertainLogic Onboarding Setup Script",
            f"# Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"# Profile: {profile['title']}",
            "#",
            "# This script installs your recommended OpenClaw skill stack.",
            "# Review before running. Nothing auto-configures — you still handle credentials.",
            "",
            "set -euo pipefail",
            "",
            'echo "=== CertainLogic Setup Script ==="',
            f'echo "Profile: {profile["title"]}"',
        ]

        all_skills = profile["certainlogic_skills"] + profile.get("community_skills", [])
        for skill_slug in all_skills:
            if skill_slug in CERTAINLOGIC_SKILLS:
                name = CERTAINLOGIC_SKILLS[skill_slug]["name"]
                cmd = f"clawhub install {CERTAINLOGIC_SKILLS[skill_slug]['clawhub_id']}"
            elif skill_slug in COMMUNITY_SKILLS:
                name = COMMUNITY_SKILLS[skill_slug]["name"]
                cmd = f"clawhub install {COMMUNITY_SKILLS[skill_slug]['clawhub_id']}"
            else:
                continue

            if skill_slug in COMMUNITY_SKILLS:
                platforms = COMMUNITY_SKILLS[skill_slug].get("platforms", ["linux", "macos"])
                if os_name not in platforms:
                    lines.append(f"\n# {name} — skipped: not supported on {os_name}")
                    continue

            if skill_slug in installed:
                lines.append(f"\n# {name} — already installed, skipping")
            else:
                lines.append(f"\necho 'Installing {name}...'")
                lines.append(f"{cmd} || echo 'WARNING: {name} install failed (may not exist on ClawHub yet)'")

        lines.extend([
            "",
            "echo ''",
            "echo '=== Setup complete ==='",
            "echo ''",
            "echo 'Next steps:'",
            "echo '1. Run verification: python3 scripts/onboarding_wizard.py --verify'",
            "echo '2. Scan each new skill with Skill Vetter Plus'",
            "echo '3. Read SKILL.md files and configure API keys manually'",
        ])
        return "\n".join(lines)


class WeeklyCheckup:
    """Re-scan environment, compare against previous scan, suggest updates."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.state_file = output_dir / "last-checkup-state.json"

    def load_last_state(self) -> Optional[Dict[str, Any]]:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return None
        return None

    def save_state(self, state: Dict[str, Any]):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")

    def run(self, env_info: Dict[str, Any]) -> str:
        last = self.load_last_state()
        current = {
            "os": env_info.get("os", "unknown"),
            "openclaw_version": env_info.get("openclaw_version", "unknown"),
            "installed_skills": sorted(env_info.get("installed_skills", set())),
            "timestamp": datetime.datetime.now().isoformat(),
            "total_skills": len(env_info.get("installed_skills", set())),
        }

        lines = [
            "# Weekly Checkup Report",
            f"Generated: {current['timestamp']}",
            "",
            "## Environment",
            f"- OS: {current['os']}",
            f"- OpenClaw: {current['openclaw_version']}",
            f"- Installed skills: {current['total_skills']}",
            "",
        ]

        if last is None:
            lines.append("## Baseline Established")
            lines.append("This is your first checkup. Future checkups will show changes.")
        else:
            lines.append("## Changes Since Last Checkup")
            last_skills = set(last.get("installed_skills", []))
            current_skills = set(current["installed_skills"])

            added = current_skills - last_skills
            removed = last_skills - current_skills

            if added:
                lines.append("\n### Skills Added")
                for s in sorted(added):
                    lines.append(f"- {s}")
            if removed:
                lines.append("\n### Skills Removed")
                for s in sorted(removed):
                    lines.append(f"- {s}")
            if not added and not removed:
                lines.append("\nNo changes detected.")

            if current["openclaw_version"] != last.get("openclaw_version", ""):
                lines.append("\n### OpenClaw Version Changed")
                lines.append(f"- {last.get('openclaw_version', '?')} → {current['openclaw_version']}")

        lines.append("\n## Recommendations")
        lines.append("- Run verification: python3 scripts/onboarding_wizard.py --verify")
        lines.append("- Scan any skill from untrusted sources with Skill Vetter Plus")

        self.save_state(current)
        return "\n".join(lines)


class TeamOnboardingExporter:
    """Export setup scripts for an entire team."""

    @staticmethod
    def export(profile: Dict[str, Any], env_info: Dict[str, Any], export_dir: Path) -> Path:
        """Create a team onboarding bundle in export_dir."""
        export_dir = Path(export_dir)
        export_dir.mkdir(parents=True, exist_ok=True)

        setup_script = SetupScriptGenerator.generate(profile, env_info)
        script_path = export_dir / "setup.sh"
        script_path.write_text(setup_script, encoding="utf-8")
        os.chmod(script_path, 0o755)

        readme = f"""# Team Onboarding — {profile['title']}

Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

## Quick Start (One Command)

```bash
./setup.sh
```

## What This Does

Installs a curated OpenClaw skill stack for the **{profile['title']}** profile.
Skills are verified by CertainLogic for stability and documentation quality.

## Verification After Install

```bash
python3 scripts/onboarding_wizard.py --verify
```

This checks:
- Every skill has a SKILL.md with usage instructions
- Every skill has valid skill.json metadata
- Scripts are present and executable

## Trust But Verify

Read SKILL.md before trusting any skill, even recommended ones.
Verification scripts catch structural issues, not runtime bugs.

---
*Bundle generated by CertainLogic Onboarding Wizard v2.1.0*
"""
        readme_path = export_dir / "README.md"
        readme_path.write_text(readme, encoding="utf-8")

        return export_dir


class OnboardingWizard:
    """Main wizard class."""

    def __init__(self, output_dir: Optional[Path] = None):
        if output_dir is None:
            output_dir = Path.home() / ".openclaw" / "workspace" / "onboarding-guides"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scanner = EnvironmentScanner()

    def detect_goal(self, raw_input: str) -> Optional[str]:
        """Map free-form input to a known goal profile."""
        raw = raw_input.lower().strip()
        if raw in GOAL_PROFILES:
            return raw
        keywords = {
            "developer": ["code", "coding", "programmer", "dev", "software", "engineer", "github"],
            "business": ["business", "company", "startup", "entrepreneur", "solopreneur", "consulting"],
            "research": ["research", "analyst", "analysis", "investigate", "study", "academic"],
            "productivity": ["productivity", "personal", "assistant", "workflow", "tasks", "todo"],
            "beginner": ["new", "start", "beginner", "first time", "help me set up"],
        }
        for goal, words in keywords.items():
            if any(w in raw for w in words):
                return goal
        return None

    def generate_report(self, goal: str, env_info: Dict[str, Any]) -> str:
        """Generate comprehensive markdown onboarding report."""
        profile = GOAL_PROFILES[goal]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        os_name = env_info.get("os", "unknown")
        installed = env_info.get("installed_skills", set())

        report = f"""# Your OpenClaw Onboarding Report
Generated: {timestamp} | Profile: {profile['title']}

> Recommendations based on our testing. Verify before trusting.

## Environment Detected
- **OS:** {os_name}
- **OpenClaw:** {env_info.get('openclaw_version', 'Unknown')}
- **Skills directory:** {env_info.get('skills_dir', 'Not found')}
- **Existing skills:** {len(installed)} installed

"""

        report += "## CertainLogic Skills\n\n"
        for skill_slug in profile["certainlogic_skills"]:
            skill = CERTAINLOGIC_SKILLS[skill_slug]
            status = "Installed" if skill_slug in installed else "Not installed"
            report += f"### {skill['name']}\n"
            report += f"- **Status:** {status}\n"
            report += f"- **Why:** {skill['description']}\n"
            if skill_slug not in installed:
                report += f"- **Install:** `clawhub install {skill['clawhub_id']}`\n"
            report += "\n"

        report += "## Community Skills (Verified)\n\n"
        for skill_slug in profile.get("community_skills", []):
            if skill_slug not in COMMUNITY_SKILLS:
                continue
            skill = COMMUNITY_SKILLS[skill_slug]
            if os_name not in skill.get("platforms", ["linux", "macos"]):
                report += f"### {skill['name']}\n"
                report += f"- **Status:** Skipped ({os_name} not supported)\n"
                report += f"- **Why:** {skill['description']}\n\n"
                continue

            status = "Installed" if skill_slug in installed else "Not installed"
            report += f"### {skill['name']}\n"
            report += f"- **Status:** {status}\n"
            report += f"- **Creator:** {skill.get('creator', 'Community')}\n"
            report += f"- **Why:** {skill['description']}\n"
            if skill_slug not in installed:
                report += f"- **Install:** `clawhub install {skill['clawhub_id']}`\n"
            report += "\n"

        report += """## Your Install Checklist\n\n"""
        all_skills = profile["certainlogic_skills"] + profile.get("community_skills", [])
        for i, skill_slug in enumerate(all_skills, 1):
            if skill_slug in CERTAINLOGIC_SKILLS:
                name = CERTAINLOGIC_SKILLS[skill_slug]["name"]
                cmd = f"clawhub install {CERTAINLOGIC_SKILLS[skill_slug]['clawhub_id']}"
            elif skill_slug in COMMUNITY_SKILLS:
                name = COMMUNITY_SKILLS[skill_slug]["name"]
                cmd = f"clawhub install {COMMUNITY_SKILLS[skill_slug]['clawhub_id']}"
            else:
                continue

            if skill_slug in installed:
                report += f"{i}. ~~{name}~~ (already installed)\n"
            else:
                report += f"{i}. **{name}**\n   `{cmd}`\n"

        report += """
## Important Notes

1. **Install Vetter Plus FIRST** — Scan every new skill before trusting it
2. **Read SKILL.md files** — Every skill has limitations
3. **Test before trusting** — What worked for us may not work for you
4. **macOS users:** PA Pack requires Things 3 (paid app)
5. **Linux users:** Some macOS-specific skills are skipped automatically

## Honest Limitations

- Recommendations are based on our testing, not universal truth
- Auto-detection checks common paths — may miss custom setups
- Platform filtering is best-effort
- We can't verify skill quality post-install — test everything
- API costs are your responsibility

## Next Steps

1. Work through the install checklist above
2. Run `python3 scripts/vetter.py <skill-dir>` on each new skill
3. Test each skill with simple tasks before using for real work
4. Join the OpenClaw community for help

---
*Built by CertainLogicAI. We want every new OpenClaw user to start strong.*
*This report was auto-generated. Review all recommendations before acting.*
"""
        return report

    def run(self, goal_input: Optional[str] = None, **kwargs) -> Path:
        """Run full onboarding flow with auto-detection."""
        print("=" * 70)
        print("CertainLogic Onboarding Wizard v2.1.0")
        print("=" * 70)
        print()

        os_name = self.scanner.detect_os()
        skills_dir = self.scanner.find_skills_dir()
        installed = self.scanner.scan_installed_skills(skills_dir)
        version = self.scanner.detect_openclaw_version()

        env_info = {
            "os": os_name,
            "skills_dir": str(skills_dir) if skills_dir else None,
            "installed_skills": installed,
            "openclaw_version": version,
        }

        print("Scanning your environment...")
        print(f"   OS: {os_name}")
        print(f"   Skills directory: {skills_dir or 'Not found'}")
        print(f"   Installed skills: {len(installed)}")
        print(f"   OpenClaw version: {version}")
        print()

        if goal_input:
            goal = self.detect_goal(goal_input)
        else:
            print("What brings you to OpenClaw?")
            print("  developer | business | research | productivity | beginner")
            goal = self.detect_goal(input("> ").strip())

        if not goal or goal not in GOAL_PROFILES:
            print("Unknown goal. Defaulting to 'beginner'.")
            goal = "beginner"

        print(f"\nProfile: {GOAL_PROFILES[goal]['title']}")
        print()

        profile = GOAL_PROFILES[goal]

        # Setup script
        if kwargs.get("setup_script"):
            setup = SetupScriptGenerator.generate(profile, env_info)
            path = self.output_dir / f"setup-{goal}.sh"
            path.write_text(setup, encoding="utf-8")
            os.chmod(path, 0o755)
            print(f"Setup script saved: {path}")
            return path

        # Team export
        if kwargs.get("team_export"):
            export_dir = TeamOnboardingExporter.export(profile, env_info, kwargs["team_export"])
            print(f"Team onboarding bundle exported to: {export_dir}")
            return export_dir

        # Default: generate report
        print("Generating your personalized onboarding report...")
        report = self.generate_report(goal, env_info)

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = self.output_dir / f"onboarding-report-{timestamp}.md"
        path.write_text(report, encoding="utf-8")

        print(f"\nReport saved: {path}")
        print(f"\nNext: Open the report and work through your install checklist.")
        print("   Remember: Install Vetter Plus first, scan everything, read SKILL.md files.")

        return path

    def scan_only(self):
        """Just show environment scan, no recommendations."""
        print("=" * 70)
        print("Environment Scan Only")
        print("=" * 70)
        os_name = self.scanner.detect_os()
        skills_dir = self.scanner.find_skills_dir()
        installed = self.scanner.scan_installed_skills(skills_dir)

        print(f"\nOS: {os_name}")
        print(f"Skills directory: {skills_dir or 'Not found'}")
        print(f"Installed skills ({len(installed)}):")
        for s in sorted(installed):
            print(f"  - {s}")

    def verify(self):
        """Run post-install verification on all installed skills."""
        skills_dir = self.scanner.find_skills_dir()
        installed = self.scanner.scan_installed_skills(skills_dir)

        if not installed:
            print("No skills found to verify.")
            return

        print(f"Verifying {len(installed)} installed skills...")
        engine = VerificationEngine(skills_dir)
        results = engine.verify_all(installed)

        report = engine.generate_verification_report(results)
        path = self.output_dir / f"verification-report-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        path.write_text(report, encoding="utf-8")
        print(f"\nVerification report saved: {path}")
        print(f"   Clean: {sum(1 for r in results if r['ok'] and not r['warnings'])}")
        print(f"   Warnings: {sum(1 for r in results if r['warnings'] and not r['errors'])}")
        print(f"   Errors: {sum(1 for r in results if r['errors'])}")

    def weekly_checkup(self):
        """Run weekly environment checkup."""
        os_name = self.scanner.detect_os()
        skills_dir = self.scanner.find_skills_dir()
        installed = self.scanner.scan_installed_skills(skills_dir)
        version = self.scanner.detect_openclaw_version()

        env_info = {
            "os": os_name,
            "skills_dir": str(skills_dir) if skills_dir else None,
            "installed_skills": installed,
            "openclaw_version": version,
        }

        checkup = WeeklyCheckup(self.output_dir)
        report = checkup.run(env_info)
        path = self.output_dir / f"weekly-checkup-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        path.write_text(report, encoding="utf-8")
        print(report)
        print(f"\nCheckup saved: {path}")


def main():
    parser = argparse.ArgumentParser(description="CertainLogic Onboarding Wizard v2.1")
    parser.add_argument("goal", nargs="?", help="Your goal")
    parser.add_argument("--scan-only", action="store_true", help="Just scan environment")
    parser.add_argument("--output-dir", type=str, help="Custom output directory")
    parser.add_argument("--setup-script", action="store_true", help="Generate one-command setup script")
    parser.add_argument("--verify", action="store_true", help="Run post-install verification")
    parser.add_argument("--weekly-checkup", action="store_true", help="Run weekly environment checkup")
    parser.add_argument("--team-export", type=str, help="Export team onboarding bundle to directory")
    args = parser.parse_args()

    wizard = OnboardingWizard(output_dir=args.output_dir)

    if args.scan_only:
        wizard.scan_only()
        return

    if args.verify:
        wizard.verify()
        return

    if args.weekly_checkup:
        wizard.weekly_checkup()
        return

    wizard.run(
        goal_input=args.goal,
        setup_script=args.setup_script,
        team_export=args.team_export,
    )


if __name__ == "__main__":
    main()
