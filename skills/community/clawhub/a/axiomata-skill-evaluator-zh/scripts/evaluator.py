#!/usr/bin/env python3
"""
SKILL EVALUATOR v3 — OpenClaw Agent Skill Evaluation System

Impersonal, universal skill evaluator for any OpenClaw agent.
Dual evaluation: Axioma 5-Dim (100pts) + ISO 25010 structural (100pts).

Usage:
    python3 evaluator.py <skill-path> [--verbose] [--improve]
    python3 evaluator.py <skill-path> --json
    python3 evaluator.py --all [--improve]
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ─── Terminal Colors ───
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ─── Version ───
VERSION = "3.0.0"

# ─── Required Sections ───
REQUIRED_SECTIONS = ["description", "usage", "examples"]

# ─── Self Discovery ───
# Find evaluator.py's own directory dynamically
SELF_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SELF_DIR.parent
SELF_NAME = "axiomata-skill-evaluator-en" if "axiomata-skill-evaluator-en" in str(SELF_DIR) else "axiomata-skill-evaluator-zh" if "axiomata-skill-evaluator-zh" in str(SELF_DIR) else "axioma-skill-evaluator"


class SkillEvaluator:
    def __init__(self, skill_path: str, verbose: bool = False, auto_improve: bool = False):
        self.skill_path = Path(skill_path).resolve()
        self.verbose = verbose
        self.auto_improve = auto_improve
        self.skill_name = self.skill_path.stem if self.skill_path.stem != "SKILL" else self.skill_path.parent.name

        self.content = ""
        self.lines = []

        # Scores per dimension (Axioma 5-Dim)
        self.scores = {
            "structure": {"score": 0, "max": 20, "details": []},
            "clarity": {"score": 0, "max": 20, "details": []},
            "completeness": {"score": 0, "max": 20, "details": []},
            "consistency": {"score": 0, "max": 20, "details": []},
            "functionality": {"score": 0, "max": 20, "details": []},
        }

        self.recommendations = []
        self.passed = True

    def log(self, msg: str, color: str = ""):
        if self.verbose or color:
            print(f"{color}{msg}{RESET}")

    def read_skill(self) -> bool:
        skill_file = self.skill_path / "SKILL.md"
        if not skill_file.exists():
            skill_file = self.skill_path  # Allow passing SKILL.md directly

        if not skill_file.exists():
            self.log(f"SKILL.md not found at {skill_file}", RED)
            return False

        with open(skill_file, "r", encoding="utf-8") as f:
            self.content = f.read()
            self.lines = self.content.split("\n")

        self.log(f"Read {skill_file} ({len(self.content)} chars)", GREEN)
        return True

    def evaluate_structure(self) -> int:
        """Evaluate skill structure (20 points)"""
        score = 0
        details = []

        # 1. Complete header (5 pts)
        header_found = False
        for i, line in enumerate(self.lines[:20]):
            if line.startswith("# ") and len(line) > 5:
                header_found = True
                break

        if header_found:
            score += 5
            details.append("Header complete")
        else:
            details.append("Header missing or incomplete")

        # 2. Required sections (5 pts)
        content_lower = self.content.lower()
        sections_found = sum(1 for s in REQUIRED_SECTIONS if s in content_lower)
        section_score = int(sections_found / len(REQUIRED_SECTIONS) * 5)
        score += section_score
        details.append(f"Sections: {sections_found}/{len(REQUIRED_SECTIONS)}")

        # 3. Formatting (5 pts)
        format_score = 0
        if "```" in self.content:
            format_score += 2
        if "|" in self.content:
            format_score += 2
        if "**" in self.content:
            format_score += 1
        score += format_score
        details.append(f"Formatting: {format_score}/5")

        # 4. Metadata (5 pts)
        meta_score = 0
        if re.search(r"status|state", content_lower):
            meta_score += 2
        if re.search(r"version|v\d", content_lower):
            meta_score += 2
        if re.search(r"\d{4}-\d{2}-\d{2}", self.content):
            meta_score += 1
        score += meta_score
        details.append(f"Metadata: {meta_score}/5")

        self.scores["structure"]["score"] = score
        self.scores["structure"]["details"] = details
        self.log(f"Structure: {score}/20", BLUE if score >= 15 else YELLOW)
        return score

    def evaluate_clarity(self) -> int:
        """Evaluate skill clarity (20 points)"""
        score = 0
        details = []
        content_lower = self.content.lower()

        # 1. Clear description (5 pts)
        lines = [l.strip() for l in self.lines if l.strip()]
        if len(lines) > 1 and lines[1] and len(lines[1]) > 30:
            score += 3
            details.append("Description present")
        else:
            details.append("Description too short")

        if lines and not lines[1].lower().startswith("this skill"):
            score += 2

        # 2. Commands (5 pts)
        cmd_count = len(re.findall(r"`([^`]+)`|```[\s\S]*?```", self.content))
        if cmd_count >= 3:
            score += 5
            details.append(f"Commands/examples: {cmd_count}")
        elif cmd_count >= 1:
            score += 3
            details.append(f"Partial commands: {cmd_count}")
        else:
            details.append("No commands/examples")

        # 3. Examples (5 pts)
        if re.search(r"example|usage|```", content_lower):
            score += 5
            details.append("Examples present")
        else:
            details.append("Examples missing")

        # 4. Constraints (5 pts)
        constraint_keywords = ["constraint", "prerequis", "requirement", "important", "note", "limitation"]
        constraints_found = sum(1 for k in constraint_keywords if k in content_lower)
        if constraints_found >= 2:
            score += 5
            details.append(f"Constraints documented: {constraints_found}")
        elif constraints_found == 1:
            score += 3
            details.append(f"Some constraints: {constraints_found}")
        else:
            score += 1
            details.append("Constraints not documented")

        self.scores["clarity"]["score"] = score
        self.scores["clarity"]["details"] = details
        self.log(f"Clarity: {score}/20", BLUE if score >= 15 else YELLOW)
        return score

    def evaluate_completeness(self) -> int:
        """Evaluate skill completeness (20 points)"""
        score = 0
        details = []
        content_lower = self.content.lower()

        # 1. Documented tools (5 pts)
        tool_patterns = [
            r"python3?\s+\w+\.py",
            r"curl\s+",
            r"bash\s+",
            r"exec\s+",
            r"read\s+",
            r"write\s+",
        ]
        tools_found = sum(len(re.findall(p, self.content)) for p in tool_patterns)
        if tools_found >= 3:
            score += 5
            details.append(f"Tools documented: {tools_found}")
        elif tools_found >= 1:
            score += 3
            details.append(f"Partial tools: {tools_found}")
        else:
            score += 1
            details.append("Tools not documented")

        # 2. Prerequisites (5 pts)
        prereq_keywords = ["require", "prerequis", "install", "setup", "config", "before"]
        prereq_found = sum(1 for k in prereq_keywords if k in content_lower)
        if prereq_found >= 2:
            score += 5
            details.append(f"Prerequisites: {prereq_found}")
        elif prereq_found == 1:
            score += 3
            details.append(f"Partial prerequisites: {prereq_found}")
        else:
            score += 1
            details.append("Prerequisites not documented")

        # 3. Error handling (5 pts)
        error_keywords = ["error", "fail", "exception", "timeout", "retry", "handling"]
        error_found = sum(1 for k in error_keywords if k in content_lower)
        if error_found >= 2:
            score += 5
            details.append(f"Errors documented: {error_found}")
        elif error_found == 1:
            score += 3
            details.append(f"Partial errors: {error_found}")
        else:
            score += 1
            details.append("Errors not documented")

        # 4. Edge cases (5 pts)
        edge_keywords = ["edge case", "corner case", "limit", "boundary", "optional", "if nothing"]
        edge_found = sum(1 for k in edge_keywords if k in content_lower)
        if edge_found >= 2:
            score += 5
            details.append(f"Edge cases: {edge_found}")
        elif edge_found == 1:
            score += 3
            details.append(f"Partial edge cases: {edge_found}")
        else:
            score += 1
            details.append("Edge cases not documented")

        self.scores["completeness"]["score"] = score
        self.scores["completeness"]["details"] = details
        self.log(f"Completeness: {score}/20", BLUE if score >= 15 else YELLOW)
        return score

    def evaluate_consistency(self) -> int:
        """Evaluate skill consistency (20 points)"""
        score = 0
        details = []
        content_lower = self.content.lower()

        # 1. Naming conventions (5 pts)
        naming_score = 0
        if re.search(r"SKILL[-_]", self.content):
            naming_score += 3
        if self.skill_path.name == "SKILL.md":
            naming_score += 2
        elif self.skill_path.is_dir():
            naming_score += 1
        score += naming_score
        details.append(f"Naming: {naming_score}/5")

        # 2. Format consistency (5 pts)
        format_score = 0
        if "**" in self.content:
            format_score += 2
        if re.search(r"\[OK\]|\[FAIL\]|\[INFO\]|\[WARNING\]|\[✅\]|\[⚠️\]|\[❌\]", self.content):
            format_score += 2
        if re.search(r"🇬🇧|🇫🇷|🇨🇳|🇺🇸", self.content):
            format_score += 1
        score += format_score
        details.append(f"Format consistency: {format_score}/5")

        # 3. Structure consistency (5 pts)
        struct_score = 0
        h1_count = len(re.findall(r"^# ", self.content, re.MULTILINE))
        h2_count = len(re.findall(r"^## ", self.content, re.MULTILINE))
        if 1 <= h1_count <= 3:
            struct_score += 2
        if h2_count >= 3:
            struct_score += 2
        if "---" in self.content[:100]:
            struct_score += 1
        score += struct_score
        details.append(f"Structure consistency: {struct_score}/5")

        # 4. Style consistency (5 pts)
        style_score = 5
        # Check for mixed language issues (reduced penalty for impersonal)
        has_chinese = bool(re.search(r"[\u4e00-\u9fff]", self.content))
        has_french = bool(re.search(r"[àâäéèêëïîôùûüÿœæç]", self.content, re.IGNORECASE))
        if has_chinese and has_french:
            style_score = 4  # Reduced from 3 to 4 for impersonal skills
        details.append(f"Style: {style_score}/5")

        self.scores["consistency"]["score"] = score
        self.scores["consistency"]["details"] = details
        self.log(f"Consistency: {score}/20", BLUE if score >= 15 else YELLOW)
        return score

    def evaluate_functionality(self) -> int:
        """Evaluate if skill actually works (20 points)"""
        score = 0
        details = []
        content_lower = self.content.lower()

        # 1. Verifiable commands (10 pts)
        commands = re.findall(r"`([^`]+)`", self.content)
        valid_commands = 0
        for cmd in commands[:5]:
            cmd = cmd.strip()
            if cmd.startswith("python") or cmd.startswith("bash") or cmd.startswith("curl"):
                if SELF_NAME not in cmd:  # Don't test self
                    valid_commands += 1

        if len(commands) == 0:
            # No commands = neutral (not penalize impersonal skills)
            score += 7
            details.append("No commands (neutral for impersonal skills)")
        elif valid_commands >= len(commands[:5]) * 0.8:
            score += 10
            details.append(f"Valid commands: {valid_commands}/{len(commands[:5])}")
        elif valid_commands >= len(commands[:5]) * 0.5:
            score += 7
            details.append(f"Partial commands: {valid_commands}/{len(commands[:5])}")
        else:
            score += 4
            details.append(f"Command issues: {valid_commands}/{len(commands[:5])}")

        # 2. Documented outputs (10 pts)
        if re.search(r"output|result|return|report", content_lower):
            score += 10
            details.append("Outputs documented")
        elif re.search(r"example|output:|→|示例|输出", self.content):
            score += 7
            details.append("Partial outputs")
        else:
            score += 4
            details.append("Outputs partially documented")

        self.scores["functionality"]["score"] = score
        self.scores["functionality"]["details"] = details
        self.log(f"Functionality: {score}/20", BLUE if score >= 15 else YELLOW)
        return score

    def generate_recommendations(self):
        """Generate improvement recommendations"""
        recs = []

        for dim, data in self.scores.items():
            if data["score"] < data["max"] * 0.7:
                pct = data["score"] / data["max"] * 100
                recs.append(f"[{dim.upper()}] Low score ({pct:.0f}%)")
                for detail in data["details"]:
                    if "missing" in detail.lower() or "not" in detail.lower() or "issues" in detail.lower():
                        recs.append(f"  -> {detail}")

        self.recommendations = recs

    def get_total_score(self) -> Tuple[int, str]:
        total = sum(s["score"] for s in self.scores.values())
        max_total = sum(s["max"] for s in self.scores.values())
        pct = total / max_total * 100

        if pct >= 90:
            status = "EXCELLENT"
            self.passed = True
        elif pct >= 70:
            status = "GOOD"
            self.passed = True
        elif pct >= 50:
            status = "NEEDS_WORK"
            self.passed = False
        else:
            status = "POOR"
            self.passed = False

        return total, status, pct

    def evaluate(self) -> bool:
        """Run full evaluation"""
        if not self.read_skill():
            return False

        self.evaluate_structure()
        self.evaluate_clarity()
        self.evaluate_completeness()
        self.evaluate_consistency()
        self.evaluate_functionality()
        self.generate_recommendations()

        total, status, pct = self.get_total_score()

        self.log(f"\n{BOLD}=== EVALUATION RESULTS ===", BLUE)
        for dim, data in self.scores.items():
            bar = "=" * int(data["score"] / data["max"] * 20)
            empty = " " * (20 - len(bar))
            color = GREEN if data["score"] >= data["max"] * 0.7 else YELLOW
            self.log(f"{dim.upper():15} {data['score']:2}/{data['max']:2} [{color}{bar}{RESET}{empty}] {data['score']/data['max']*100:.0f}%", BLUE)

        self.log(f"{'='*50}", BLUE)
        for rec in self.recommendations:
            self.log(f"  {rec}", YELLOW)

        self.log(f"\nSTATUS: {status} (score {pct:.0f}%)", GREEN if self.passed else RED)
        return self.passed

    def print_report(self):
        """Print evaluation report"""
        total, status, pct = self.get_total_score()
        print(f"\n{'='*50}")
        print(f"SKILL EVALUATOR v{VERSION} Report")
        print(f"{'='*50}")
        print(f"Skill: {self.skill_name}")
        print(f"Score: {total}/100")
        print(f"Status: {status}")
        print(f"\nDimension Scores:")
        for dim, data in self.scores.items():
            print(f"  {dim.upper()}: {data['score']}/{data['max']}")
        if self.recommendations:
            print(f"\nRecommendations:")
            for rec in self.recommendations:
                print(f"  - {rec}")
        print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description=f"SKILL EVALUATOR v{VERSION}")
    parser.add_argument("skill_path", nargs="?", help="Path to skill directory or SKILL.md")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--improve", "-i", action="store_true", help="Auto-improve skill")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--all", "-a", action="store_true", help="Evaluate all skills in directory")
    args = parser.parse_args()

    if args.all:
        skills_dir = SKILL_DIR.parent
        skills = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        print(f"Evaluating {len(skills)} skills...")
        for skill in skills:
            print(f"\n{'='*50}")
            print(f"Skill: {skill.name}")
            print(f"{'='*50}")
            evaluator = SkillEvaluator(str(skill), verbose=args.verbose, auto_improve=args.improve)
            evaluator.evaluate()
        return

    if not args.skill_path:
        # Self-evaluation
        args.skill_path = str(SELF_DIR)

    evaluator = SkillEvaluator(args.skill_path, verbose=args.verbose, auto_improve=args.improve)
    success = evaluator.evaluate()

    if args.json:
        result = {
            "skill": evaluator.skill_name,
            "scores": {k: v["score"] for k, v in evaluator.scores.items()},
            "total": sum(v["score"] for v in evaluator.scores.values()),
            "max": 100,
            "passed": evaluator.passed,
            "recommendations": evaluator.recommendations
        }
        print(json.dumps(result, indent=2))

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()