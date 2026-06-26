#!/usr/bin/env python3
"""Agent Health Score — scan workspace and score agent architecture quality.

Usage: python3 health_score.py [workspace_path]
Default workspace: ~/.openclaw/workspace

Outputs a scored report (0-100) across 5 dimensions:
  Memory, Cron, Skills, Security, Continuity
"""

import sys, json, re, subprocess
from pathlib import Path
from datetime import datetime, timedelta

ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / ".openclaw" / "workspace"


def run_cmd(args, timeout=15):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except Exception:
        return "", 1


def get_all_jobs():
    out, code = run_cmd(["openclaw", "cron", "list", "--json"])
    if code == 0:
        try:
            data = json.loads(out)
            return {j["id"]: j for j in data.get("jobs", [])}
        except Exception:
            pass
    return {}


class Scorer:
    def __init__(self):
        self.results = {}
        self.issues = []
        self.suggestions = []

    def score_memory(self):
        score = 0
        max_score = 25
        mem = ws / "MEMORY.md"

        if mem.exists() and mem.stat().st_size > 100:
            score += 5
        else:
            self.issues.append("❌ MEMORY.md missing or empty")

        mem_dir = ws / "memory"
        if mem_dir.exists():
            daily_files = list(mem_dir.glob("????-??-??.md"))
            if daily_files:
                score += 3
                recent = [f for f in daily_files if f.stem >= (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")]
                if recent:
                    score += 3
                else:
                    self.suggestions.append("💡 No daily logs in last 3 days — agent may not be logging")
            else:
                self.issues.append("❌ No daily log files found in memory/")
        else:
            self.issues.append("❌ memory/ directory missing")

        if (ws / "memory" / "working-buffer.md").exists():
            score += 3
            self.suggestions.append("✅ Working buffer configured")
        else:
            self.suggestions.append("💡 No working-buffer.md — add WAL protocol for long sessions")

        if mem.exists():
            content = mem.read_text()
            imperative_patterns = [r"(?i)^- always ", r"(?i)^- never ", r"(?i)^- you must ", r"(?i)^- you should "]
            imperative_count = sum(len(re.findall(p, content, re.MULTILINE)) for p in imperative_patterns)
            if imperative_count == 0:
                score += 4
            elif imperative_count <= 3:
                score += 2
                self.suggestions.append(f"💡 {imperative_count} imperative rules in MEMORY.md — prefer declarative facts")
            else:
                self.issues.append(f"⚠️ {imperative_count} imperative rules in MEMORY.md — risk of memory poisoning")

            source_tagged = len(re.findall(r"\(source:|来源:", content, re.IGNORECASE))
            facts = len(re.findall(r"^-\s", content, re.MULTILINE))
            if facts > 0:
                ratio = source_tagged / max(facts, 1)
                if ratio > 0.3:
                    score += 4
                elif ratio > 0.1:
                    score += 2
                    self.suggestions.append("💡 Only {:.0%} of MEMORY.md facts have source tags".format(ratio))
                else:
                    self.suggestions.append("💡 Very few source tags in MEMORY.md — add them for high-value non-obvious facts")
            else:
                score += 3

        if (ws / "AGENTS.md").exists():
            score += 3
        else:
            self.issues.append("❌ AGENTS.md missing")

        self.results["🧠 Memory"] = (score, max_score)
        return score

    def score_cron(self):
        score = 0
        max_score = 25
        jobs = get_all_jobs()
        if not jobs:
            self.suggestions.append("💡 No cron jobs configured or could not read them")
            self.results["⏰ Cron"] = (score, max_score)
            return score

        score += 3

        error_count = sum(1 for j in jobs.values() if j.get("state", {}).get("lastStatus") == "error")
        if error_count == 0:
            score += 5
        elif error_count <= 1:
            score += 3
            self.suggestions.append(f"💡 {error_count} cron job in error state")
        else:
            self.issues.append(f"⚠️ {error_count} cron jobs in error state — investigate")

        with_stagger = sum(1 for j in jobs.values() if (j.get("schedule", {}).get("staggerMs", 0) or 0) > 0)
        without_stagger = len(jobs) - with_stagger
        if without_stagger == 0:
            score += 5
        elif with_stagger > 0:
            score += 3
            self.suggestions.append(f"💡 {without_stagger} jobs have no stagger — check only burst-prone recurring jobs")
        else:
            score += 1
            self.suggestions.append("💡 No jobs use stagger — consider it for bursty recurring schedules, not exact-time jobs")

        isolated_count = sum(1 for j in jobs.values() if j.get("sessionTarget") == "isolated")
        if isolated_count > 0:
            score += 4
        else:
            self.suggestions.append("💡 Consider using isolated sessions for background cron jobs")

        labels = []
        for j in jobs.values():
            s = j.get("schedule", {})
            kind = s.get("kind", "")
            if kind == "cron":
                labels.append((s.get("expr", ""), s.get("tz", "")))
        unique_exprs = len(set(labels))
        if len(labels) > 1:
            if unique_exprs == len(labels):
                score += 5
            elif unique_exprs > len(labels) * 0.5:
                score += 3
                self.suggestions.append("💡 Some cron jobs share the same schedule — review for load spikes")
            else:
                score += 1
                self.issues.append("⚠️ Many cron jobs share schedules — diversify if they hit the same APIs")
        else:
            score += 4

        missing_to = sum(
            1 for j in jobs.values()
            if (j.get("delivery", {}) or {}).get("mode") == "announce"
            and (j.get("delivery", {}) or {}).get("channel") not in (None, "", "last")
            and not (j.get("delivery", {}) or {}).get("to")
        )
        if missing_to == 0:
            score += 2
        else:
            self.issues.append(f"🚨 {missing_to} announce jobs are missing explicit 'to' targets")

        self.results["⏰ Cron"] = (min(score, max_score), max_score)
        return min(score, max_score)

    def score_skills(self):
        score = 0
        max_score = 20
        skills_dir = ws / "skills"
        if not skills_dir.exists():
            self.issues.append("❌ No skills directory")
            self.results["📦 Skills"] = (0, max_score)
            return 0

        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        if not skill_dirs:
            self.suggestions.append("💡 No skills installed")
            self.results["📦 Skills"] = (0, max_score)
            return 0

        score += 3
        names = [d.name for d in skill_dirs]

        keywords = {
            "stock": [], "news": [], "weather": [], "academic": [],
            "productivity": [], "monitor": [], "watcher": []
        }
        for name in names:
            for kw in keywords:
                if kw in name:
                    keywords[kw].append(name)

        redundant = {k: v for k, v in keywords.items() if len(v) > 2}
        if not redundant:
            score += 5
        else:
            for k, v in redundant.items():
                self.suggestions.append(f"💡 Possible overlap in '{k}' category: {', '.join(v)}")
            score += 2

        if len(skill_dirs) >= 5:
            score += 4
        else:
            self.suggestions.append(f"💡 Only {len(skill_dirs)} skills — explore ClawHub if you need more coverage")
            score += 2

        managed = sum(1 for d in skill_dirs if (d / ".clawhub").exists())
        if managed > len(skill_dirs) * 0.5:
            score += 4
        else:
            score += 2
            self.suggestions.append("💡 Many skills are not ClawHub-managed — updates may be manual")

        if any((d / "_meta.json").exists() or (d / "SKILL.md").read_text().strip() for d in skill_dirs):
            score += 4

        self.results["📦 Skills"] = (min(score, max_score), max_score)
        return min(score, max_score)

    def score_security(self):
        score = 0
        max_score = 15
        agents = ws / "AGENTS.md"
        if agents.exists():
            content = agents.read_text()
            if "safety" in content.lower() or "security" in content.lower():
                score += 3
            else:
                self.suggestions.append("💡 Add safety/security section to AGENTS.md")
            if "anti-poisoning" in content.lower() or "memory hygiene" in content.lower():
                score += 4
            else:
                self.suggestions.append("💡 Add memory anti-poisoning rules to AGENTS.md")
            if "wal protocol" in content.lower() or "write-ahead" in content.lower():
                score += 4
            else:
                self.suggestions.append("💡 Add WAL protocol for context safety")
            if "external" in content.lower() and ("ask" in content.lower() or "permission" in content.lower()):
                score += 4
            else:
                self.suggestions.append("💡 Add external action confirmation rules")

        self.results["🔒 Security"] = (score, max_score)
        return score

    def score_continuity(self):
        score = 0
        max_score = 15
        for f, pts, label in [
            ("SOUL.md", 3, "agent identity"),
            ("USER.md", 3, "know your human"),
            ("HEARTBEAT.md", 3, "periodic self-checks"),
            ("IDENTITY.md", 3, None),
        ]:
            if (ws / f).exists():
                score += pts
            elif label:
                self.suggestions.append(f"💡 Create {f} — {label}")
            else:
                score += 1

        if (ws / ".git").exists():
            score += 3
        else:
            self.suggestions.append("💡 Initialize git in workspace for version control")

        self.results["🔄 Continuity"] = (score, max_score)
        return score

    def run(self):
        total = sum([
            self.score_memory(),
            self.score_cron(),
            self.score_skills(),
            self.score_security(),
            self.score_continuity(),
        ])
        max_total = sum(v[1] for v in self.results.values())
        pct = int(total / max_total * 100)

        grade = "A+" if pct >= 90 else "A" if pct >= 80 else "B" if pct >= 70 else "C" if pct >= 60 else "D" if pct >= 50 else "F"

        print(f"\n🏥 Agent Health Score: {total}/{max_total} ({pct}%) — Grade: {grade}")
        print("=" * 50)
        for name, (s, m) in self.results.items():
            bar = "█" * int(s / m * 10) + "░" * (10 - int(s / m * 10))
            print(f"  {name}: {s}/{m} [{bar}]")

        if self.issues:
            print(f"\n🚨 Issues ({len(self.issues)}):")
            for i in self.issues:
                print(f"  {i}")

        if self.suggestions:
            print(f"\n💡 Suggestions ({len(self.suggestions)}):")
            for s in self.suggestions:
                print(f"  {s}")

        print(f"\n📅 Scanned: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"📁 Workspace: {ws}")

        report = {
            "score": total, "max": max_total, "pct": pct, "grade": grade,
            "dimensions": {k: {"score": v[0], "max": v[1]} for k, v in self.results.items()},
            "issues": self.issues, "suggestions": self.suggestions,
            "timestamp": datetime.now().isoformat()
        }
        report_path = ws / "memory" / "health-score.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"\n📊 Report saved: {report_path}")


if __name__ == "__main__":
    Scorer().run()
