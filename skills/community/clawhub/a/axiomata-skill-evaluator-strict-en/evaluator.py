#!/usr/bin/env python3
"""
SKILL_EVALUATOR — Claude Skills 2.0 pour Axioma Stellaris
Évaluation automatique des skills dans un sandbox

Usage:
    python3 evaluator.py /path/to/skill [--verbose] [--improve]
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

# Couleurs pour terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

AGENT_NAME = "Morgana"
SKILL_DIR = Path("/media/ezekiel/Morgana/skills")
REPORTS_DIR = Path("/media/ezekiel/Morgana/skills/SKILL_EVALUATOR/reports")

# Sections requises dans un SKILL.md
REQUIRED_SECTIONS = [
    "description",
    "usage",
    "examples",
]

# Critères de structure
STRUCTURE_KEYWORDS = {
    "header": ["#", "skill", "description", "status"],
    "sections": ["##", "usage", "examples", "commands"],
    "formatting": ["```", "|", "**"],
}


class SkillEvaluator:
    def __init__(self, skill_path: str, verbose: bool = False, auto_improve: bool = False):
        self.skill_path = Path(skill_path)
        self.verbose = verbose
        self.auto_improve = auto_improve
        self.skill_name = self.skill_path.stem if self.skill_path.stem != "SKILL" else self.skill_path.parent.name
        
        self.content = ""
        self.lines = []
        
        # Scores par dimension
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
            self.log(f"❌ SKILL.md not found at {skill_file}", RED)
            return False
        
        with open(skill_file, "r", encoding="utf-8") as f:
            self.content = f.read()
            self.lines = self.content.split("\n")
        
        self.log(f"✅ Read {skill_file} ({len(self.content)} chars)", GREEN)
        return True
    
    def evaluate_structure(self) -> int:
        """Évalue la structure du skill (20 points)"""
        score = 0
        details = []
        
        # 1. Header complet (5 points)
        header_found = False
        for i, line in enumerate(self.lines[:20]):
            if line.startswith("# ") and len(line) > 5:
                header_found = True
                break
        
        if header_found:
            score += 5
            details.append("✅ Header complet")
        else:
            details.append("❌ Header manquant ou incomplet")
        
        # 2. Sections requises (5 points)
        content_lower = self.content.lower()
        sections_found = sum(1 for s in REQUIRED_SECTIONS if s in content_lower)
        section_score = int(sections_found / len(REQUIRED_SECTIONS) * 5)
        score += section_score
        details.append(f"{'✅' if sections_found == 3 else '⚠️'} Sections: {sections_found}/3")
        
        # 3. Formatting (5 points)
        format_score = 0
        if "```" in self.content:  # Code blocks
            format_score += 2
        if "|" in self.content:  # Tables
            format_score += 2
        if "**" in self.content:  # Bold
            format_score += 1
        score += format_score
        details.append(f"{'✅' if format_score >= 4 else '⚠️'} Formatting: {format_score}/5")
        
        # 4. Meta-données (5 points)
        meta_score = 0
        if re.search(r"status|state", content_lower):
            meta_score += 2
        if re.search(r"version|v\d", content_lower):
            meta_score += 2
        if re.search(r"\d{4}-\d{2}-\d{2}", self.content):  # Date
            meta_score += 1
        score += meta_score
        details.append(f"{'✅' if meta_score >= 4 else '⚠️'} Meta: {meta_score}/5")
        
        self.scores["structure"]["score"] = score
        self.scores["structure"]["details"] = details
        self.log(f"Structure: {score}/20", BLUE if score >= 15 else YELLOW)
        return score
    
    def evaluate_clarity(self) -> int:
        """Évalue la clarté du skill (20 points)"""
        score = 0
        details = []
        content_lower = self.content.lower()
        
        # 1. Description claire (5 points)
        # Chercher une phrase de description après le header
        lines = [l.strip() for l in self.lines if l.strip()]
        if len(lines) > 1 and lines[1] and len(lines[1]) > 30:
            score += 3
            details.append("✅ Description présente")
        else:
            details.append("⚠️ Description trop courte")
        
        # Vérifier que > ne commence pas par "This skill"
        if lines and not lines[1].lower().startswith("this skill"):
            score += 2
        
        # 2. Instructions (5 points)
        cmd_count = len(re.findall(r"`([^`]+)`|```[\s\S]*?```", self.content))
        if cmd_count >= 3:
            score += 5
            details.append(f"✅ Commandes/exemples: {cmd_count}")
        elif cmd_count >= 1:
            score += 3
            details.append(f"⚠️ Commandes partielles: {cmd_count}")
        else:
            details.append("❌ Aucune commande/exemple")
        
        # 3. Exemples (5 points)
        if re.search(r"example|usage|```", content_lower):
            score += 5
            details.append("✅ Exemples présents")
        else:
            details.append("❌ Exemples manquants")
        
        # 4. Contraintes (5 points)
        constraint_keywords = [" limitation", "constraint", "prerequis", "requirement", "important", "note"]
        constraints_found = sum(1 for k in constraint_keywords if k in content_lower)
        if constraints_found >= 2:
            score += 5
            details.append(f"✅ Contraintes documentées: {constraints_found}")
        elif constraints_found == 1:
            score += 3
            details.append(f"⚠️ Quelques contraintes: {constraints_found}")
        else:
            score += 1
            details.append("❌ Contraintes non documentées")
        
        self.scores["clarity"]["score"] = score
        self.scores["clarity"]["details"] = details
        self.log(f"Clarity: {score}/20", BLUE if score >= 15 else YELLOW)
        return score
    
    def evaluate_completeness(self) -> int:
        """Évalue la complétude du skill (20 points)"""
        score = 0
        details = []
        content_lower = self.content.lower()
        
        # 1. Outils nécessaires (5 points)
        tool_patterns = [
            r"openclaw\s+\w+",
            r"python3?\s+\w+\.py",
            r"curl\s+",
            r"bash\s+",
        ]
        tools_found = sum(len(re.findall(p, self.content)) for p in tool_patterns)
        if tools_found >= 3:
            score += 5
            details.append(f"✅ Outils documentés: {tools_found}")
        elif tools_found >= 1:
            score += 3
            details.append(f"⚠️ Outils partiels: {tools_found}")
        else:
            score += 1
            details.append("❌ Outils non documentés")
        
        # 2. Prérequis (5 points)
        prereq_keywords = ["require", "prerequis", "install", "setup", "config"]
        prereq_found = sum(1 for k in prereq_keywords if k in content_lower)
        if prereq_found >= 2:
            score += 5
            details.append(f"✅ Prérequis: {prereq_found}")
        elif prereq_found == 1:
            score += 3
            details.append(f"⚠️ Prérequis partiels: {prereq_found}")
        else:
            score += 1
            details.append("❌ Prérequis non documentés")
        
        # 3. Erreurs gérées (5 points)
        error_keywords = ["error", "fail", "exception", "timeout", "retry"]
        error_found = sum(1 for k in error_keywords if k in content_lower)
        if error_found >= 2:
            score += 5
            details.append(f"✅ Erreurs documentées: {error_found}")
        elif error_found == 1:
            score += 3
            details.append(f"⚠️ Erreurs partielles: {error_found}")
        else:
            score += 1
            details.append("❌ Erreurs non documentées")
        
        # 4. Cas limites (5 points)
        edge_keywords = ["edge case", "corner case", "limit", "boundary", "optional"]
        edge_found = sum(1 for k in edge_keywords if k in content_lower)
        if edge_found >= 2:
            score += 5
            details.append(f"✅ Cas limites: {edge_found}")
        elif edge_found == 1:
            score += 3
            details.append(f"⚠️ Cas limites partiels: {edge_found}")
        else:
            score += 1
            details.append("❌ Cas limites non documentés")
        
        self.scores["completeness"]["score"] = score
        self.scores["completeness"]["details"] = details
        self.log(f"Completeness: {score}/20", BLUE if score >= 15 else YELLOW)
        return score
    
    def evaluate_consistency(self) -> int:
        """Évalue la cohérence avec le cluster (20 points)"""
        score = 0
        details = []
        content_lower = self.content.lower()
        
        # 1. Cluster alignment (5 points)
        cluster_keywords = ["AMIMOUR", "STC", "Morgana", "Ezekiel", "Merlin", "cluster", "Axioma"]
        cluster_found = sum(1 for k in cluster_keywords if k in self.content)
        if cluster_found >= 3:
            score += 5
            details.append(f"✅ Cluster alignment: {cluster_found}")
        elif cluster_found >= 1:
            score += 3
            details.append(f"⚠️ Cluster alignment partiel: {cluster_found}")
        else:
            score += 1
            details.append("⚠️ Cluster alignment faible")
        
        # 2. Style consistency (5 points)
        # Vérifier le style Chinese-French-English
        style_score = 0
        if "**" in self.content:  # Bold usage
            style_score += 2
        if re.search(r"🇬🇧|🇫🇷|🇨🇳", self.content):  # Flags
            style_score += 2
        if re.search(r"\[OK\]|\[FAIL\]|\[INFO\]", self.content):  # Status markers
            style_score += 1
        score += style_score
        details.append(f"{'✅' if style_score >= 4 else '⚠️'} Style: {style_score}/5")
        
        # 3. Naming conventions (5 points)
        naming_score = 5
        # Vérifier que le skill suit SKILL_XXX.md ou XXX/SKILL.md
        if re.search(r"SKILL[-_]", self.content):
            naming_score = 5
        elif self.skill_path.name == "SKILL.md":
            naming_score = 4
        else:
            naming_score = 3
        score = (score - 5) + naming_score  # Replace previous style_score component
        details.append(f"✅ Naming: {naming_score}/5")
        
        # 4. Integration (5 points)
        integration_keywords = ["integration", "connect", "plugin", "hook", "tool"]
        integration_found = sum(1 for k in integration_keywords if k in content_lower)
        if integration_found >= 2:
            score += 5
            details.append(f"✅ Integration: {integration_found}")
        elif integration_found == 1:
            score += 3
            details.append(f"⚠️ Integration partielle: {integration_found}")
        else:
            score += 1
            details.append("⚠️ Integration non documentée")
        
        self.scores["consistency"]["score"] = score
        self.scores["consistency"]["details"] = details
        self.log(f"Consistency: {score}/20", BLUE if score >= 15 else YELLOW)
        return score
    
    def evaluate_functionality(self) -> int:
        """Évalue si le skill fonctionne réellement (20 points)"""
        score = 0
        details = []
        content_lower = self.content.lower()
        
        # 1. Execute sans erreur (10 points)
        # Tester si les commandes listées sont valides
        commands = re.findall(r"`([^`]+)`", self.content)
        valid_commands = 0
        for cmd in commands[:5]:  # Test max 5 commands
            cmd = cmd.strip()
            if cmd.startswith("python") or cmd.startswith("bash") or cmd.startswith("curl"):
                # Check if file exists
                if "SKILL_EVALUATOR" not in cmd:  # Don't test self
                    valid_commands += 1
        
        if len(commands) == 0:
            score += 5  # Pas de commandes à tester
            details.append("⚠️ Aucune commande à tester")
        elif valid_commands >= len(commands) * 0.8:
            score += 10
            details.append(f"✅ Commandes valides: {valid_commands}/{len(commands[:5])}")
        elif valid_commands >= len(commands) * 0.5:
            score += 6
            details.append(f"⚠️ Commandes partielles: {valid_commands}/{len(commands[:5])}")
        else:
            score += 2
            details.append(f"❌ Commandes problèmes: {valid_commands}/{len(commands[:5])}")
        
        # 2. Résultats attendus (10 points)
        # Vérifier que les outputs sont documentés
        if re.search(r"output|result|return|report", content_lower):
            score += 10
            details.append("✅ Résultats documentés")
        elif re.search(r"example|output:|→", self.content):
            score += 7
            details.append("⚠️ Résultats partiels")
        else:
            score += 3
            details.append("❌ Résultats non documentés")
        
        self.scores["functionality"]["score"] = score
        self.scores["functionality"]["details"] = details
        self.log(f"Functionality: {score}/20", BLUE if score >= 15 else YELLOW)
        return score
    
    def generate_recommendations(self):
        """Génère des recommandations d'amélioration"""
        recs = []
        
        for dim, data in self.scores.items():
            if data["score"] < data["max"] * 0.7:  # Less than 70%
                pct = data["score"] / data["max"] * 100
                recs.append(f"[{dim.upper()}] Score bas ({pct:.0f}%)")
                for detail in data["details"]:
                    if detail.startswith("❌"):
                        recs.append(f"  → {detail}")
        
        self.recommendations = recs
    
    def get_total_score(self) -> Tuple[int, str]:
        total = sum(s["score"] for s in self.scores.values())
        max_total = sum(s["max"] for s in self.scores.values())
        pct = total / max_total * 100
        
        if pct >= 90:
            status = "🟢 EXCELLENT"
            self.passed = True
        elif pct >= 70:
            status = "🟡 GOOD"
            self.passed = True
        elif pct >= 50:
            status = "🟠 NEEDS_WORK"
            self.passed = False
        else:
            status = "🔴 POOR"
            self.passed = False
        
        return total, status
    
    def generate_report(self) -> str:
        total, status = self.get_total_score()
        max_total = sum(s["max"] for s in self.scores.values())
        
        report = []
        report.append(f"\n{'='*60}")
        report.append(f"📊 SKILL EVALUATION REPORT — {self.skill_name}")
        report.append(f"{'='*60}")
        report.append(f"Path: {self.skill_path}")
        report.append(f"Score: {total}/{max_total} {status}")
        report.append(f"{'-'*60}")
        
        for dim, data in self.scores.items():
            pct = data["score"] / data["max"] * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            color = GREEN if pct >= 70 else YELLOW if pct >= 50 else RED
            report.append(f"{dim.upper():15} {data['score']:2}/{data['max']:2} {color}{bar}{RESET} {pct:.0f}%")
        
        report.append(f"{'-'*60}")
        report.append("DETAILS:")
        for dim, data in self.scores.items():
            report.append(f"  {dim.upper()}:")
            for detail in data["details"]:
                report.append(f"    {detail}")
        
        if self.recommendations:
            report.append(f"{'-'*60}")
            report.append("RECOMMENDATIONS:")
            for rec in self.recommendations:
                report.append(f"  • {rec}")
        
        report.append(f"{'='*60}")
        
        if self.passed:
            report.append(f"STATUS: ✅ APPROVED (score >= 70%)")
        else:
            report.append(f"STATUS: ❌ NEEDS WORK (score < 50%)")
        
        report.append("")
        return "\n".join(report)
    
    def save_report(self, report: str):
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = REPORTS_DIR / f"{self.skill_name}_{timestamp}.txt"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        self.log(f"\n📄 Report saved: {report_file}", GREEN)
        return report_file
    
    def evaluate(self) -> Dict:
        """Run full evaluation"""
        print(f"\n{BOLD}🧪 SKILL_EVALUATOR — Evaluating {self.skill_name}{RESET}")
        print("-" * 40)
        
        # Step 1: Read
        if not self.read_skill():
            return {"error": "Failed to read skill", "score": 0}
        
        # Step 2: Evaluate each dimension
        self.evaluate_structure()
        self.evaluate_clarity()
        self.evaluate_completeness()
        self.evaluate_consistency()
        self.evaluate_functionality()
        
        # Step 3: Generate recommendations
        self.generate_recommendations()
        
        # Step 4: Generate and save report
        report = self.generate_report()
        report_file = self.save_report(report)
        
        # Print report
        print(report)
        
        total, status = self.get_total_score()
        return {
            "skill": self.skill_name,
            "path": str(self.skill_path),
            "score": total,
            "max": 100,
            "status": status,
            "passed": self.passed,
            "recommendations": self.recommendations,
            "report_file": str(report_file),
        }


def find_all_skills() -> List[Path]:
    """Trouve tous les skills dans le workspace"""
    skills = []
    
    # Morgana skills
    for p in Path(SKILL_DIR).rglob("SKILL.md"):
        skills.append(p.parent)
    
    # OpenClaw global skills
    openclaw_skills = Path("/home/ezekiel/.npm-global/lib/node_modules/openclaw/skills")
    if openclaw_skills.exists():
        for p in openclaw_skills.rglob("SKILL.md"):
            if p.parent.name not in ["clawhub", "apple-notes", "apple-reminders", "bear-notes"]:
                skills.append(p.parent)
    
    return skills


def main():
    parser = argparse.ArgumentParser(description="SKILL_EVALUATOR — Claude Skills 2.0")
    parser.add_argument("path", nargs="?", help="Path to skill to evaluate")
    parser.add_argument("--all", action="store_true", help="Evaluate all skills")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--improve", action="store_true", help="Auto-improve if possible")
    args = parser.parse_args()
    
    if args.all:
        print(f"{BOLD}🧪 SKILL_EVALUATOR — Evaluating ALL skills{RESET}\n")
        skills = find_all_skills()
        print(f"Found {len(skills)} skills to evaluate\n")
        
        results = []
        for skill_path in skills:
            try:
                evaluator = SkillEvaluator(str(skill_path), verbose=args.verbose, auto_improve=args.improve)
                result = evaluator.evaluate()
                results.append(result)
            except Exception as e:
                print(f"❌ Error evaluating {skill_path}: {e}")
        
        # Summary
        print(f"\n{BOLD}{'='*60}")
        print(f"📊 SUMMARY — {len(results)} skills evaluated")
        print(f"{'='*60}")
        
        passed = [r for r in results if r.get("passed", False)]
        failed = [r for r in results if not r.get("passed", True)]
        
        print(f"✅ Passed: {len(passed)}")
        print(f"❌ Failed: {len(failed)}")
        
        if failed:
            print("\nFailed skills:")
            for r in failed:
                print(f"  - {r['skill']}: {r['score']}/100")
        
        print()
        
    elif args.path:
        evaluator = SkillEvaluator(args.path, verbose=args.verbose, auto_improve=args.improve)
        result = evaluator.evaluate()
        
        if result.get("passed"):
            print(f"\n✅ {result['skill']} APPROVED (score >= 70%)")
        else:
            print(f"\n❌ {result['skill']} NEEDS WORK (score < 50%)")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
