#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Review Script - Daily reflection script
Helps agents conduct structured end-of-day reflection and documentation
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional


class DailyReview:
    """Core daily review class"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace = Path(workspace_path) if workspace_path else Path.home() / ".qclaw" / "workspace"
        self.memory_dir = self.workspace / "memory"
        self.review_dir = self.workspace / "reviews"
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Ensure directories exist
        self.review_dir.mkdir(parents=True, exist_ok=True)
    
    def scan_today_records(self) -> Dict[str, Any]:
        """Scan today's records"""
        records = {
            "date": self.today,
            "daily_note": None,
            "artifacts": [],
            "memory_entries": [],
            "task_count": 0,
            "decisions": [],
            "learnings": []
        }
        
        # 1. Read today's memory file
        today_memory = self.memory_dir / f"{self.today}.md"
        if today_memory.exists():
            content = today_memory.read_text(encoding='utf-8')
            records["daily_note"] = content
            records["memory_entries"] = self._extract_entries(content)
        
        # 2. Scan today's artifacts
        records["artifacts"] = self._scan_artifacts()
        
        # 3. Scan today's entries in MEMORY.md
        main_memory = self.workspace / "MEMORY.md"
        if main_memory.exists():
            content = main_memory.read_text(encoding='utf-8')
            records["decisions"] = self._extract_decisions(content, self.today)
            records["learnings"] = self._extract_learnings(content, self.today)
        
        return records
    
    def _extract_entries(self, content: str) -> List[Dict]:
        """Extract entries from memory content"""
        entries = []
        # Match timestamp entries, e.g., "- 10:30 completed xxx"
        time_pattern = r'^-?\s*(\d{1,2}:\d{2})\s+(.+)$'
        for line in content.split('\n'):
            match = re.match(time_pattern, line.strip())
            if match:
                entries.append({
                    "time": match.group(1),
                    "content": match.group(2)
                })
        return entries
    
    def _scan_artifacts(self) -> List[Dict]:
        """Scan artifacts generated today"""
        artifacts = []
        today_prefix = self.today.replace("-", "")
        
        for file in self.workspace.glob("*.md"):
            if today_prefix in file.name and file.name != f"{self.today}.md":
                stat = file.stat()
                artifacts.append({
                    "name": file.name,
                    "type": "artifact",
                    "created": datetime.fromtimestamp(stat.st_ctime).strftime("%H:%M")
                })
        return artifacts
    
    def _extract_decisions(self, content: str, date: str) -> List[str]:
        """Extract decision records"""
        decisions = []
        # Find lines containing decision-related keywords
        decision_keywords = ['decision', 'decided', 'chose', 'confirmed', 'adopted']
        for line in content.split('\n'):
            if date in line or any(kw in line.lower() for kw in decision_keywords):
                if any(kw in line.lower() for kw in decision_keywords):
                    decisions.append(line.strip())
        return decisions[:10]  # Limit quantity
    
    def _extract_learnings(self, content: str, date: str) -> List[str]:
        """Extract learning/lesson records"""
        learnings = []
        learning_keywords = ['learned', 'lesson', 'experience', 'note', 'improve']
        for line in content.split('\n'):
            if date in line or any(kw in line.lower() for kw in learning_keywords):
                if any(kw in line.lower() for kw in learning_keywords):
                    learnings.append(line.strip())
        return learnings[:10]
    
    def categorize_activities(self, records: Dict) -> Dict[str, List]:
        """Categorize activities"""
        categories = {
            "completed_tasks": [],
            "in_progress": [],
            "blockers": [],
            "meetings": [],
            "learning": [],
            "other": []
        }
        
        # Analyze memory entries
        if records["daily_note"]:
            content = records["daily_note"]
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                # Identify completed tasks
                if any(kw in line.lower() for kw in ['completed', 'done', 'resolved', '✅', '✓', 'finished']):
                    categories["completed_tasks"].append(line)
                # Identify in-progress tasks
                elif any(kw in line.lower() for kw in ['in progress', 'working on', '🔄', 'pending']):
                    categories["in_progress"].append(line)
                # Identify blockers/issues
                elif any(kw in line.lower() for kw in ['issue', 'blocked', 'stuck', 'bug', 'error', '❌']):
                    categories["blockers"].append(line)
                # Identify meetings/communication
                elif any(kw in line.lower() for kw in ['meeting', 'discussed', 'sync', 'report', 'aligned']):
                    categories["meetings"].append(line)
                # Identify learning
                elif any(kw in line.lower() for kw in ['learned', 'understood', 'researched', 'studied', 'read']):
                    categories["learning"].append(line)
                else:
                    categories["other"].append(line)
        
        # Statistics
        categories["stats"] = {
            "total_entries": len(records["memory_entries"]),
            "artifacts_created": len(records["artifacts"]),
            "decisions": len(records["decisions"]),
            "learnings": len(records["learnings"])
        }
        
        return categories
    
    def reflect_and_analyze(self, categories: Dict, records: Dict) -> Dict[str, Any]:
        """Reflect and analyze"""
        reflection = {
            "productivity_score": 0,
            "highlights": [],
            "challenges": [],
            "patterns": [],
            "suggestions": []
        }
        
        stats = categories["stats"]
        
        # Calculate productivity score (simple algorithm)
        score = min(100, stats["total_entries"] * 5 + stats["artifacts_created"] * 10 + 50)
        reflection["productivity_score"] = score
        
        # Extract highlights
        if categories["completed_tasks"]:
            reflection["highlights"].append(f"Completed {len(categories['completed_tasks'])} tasks")
        if stats["artifacts_created"] > 0:
            reflection["highlights"].append(f"Generated {stats['artifacts_created']} artifacts")
        if records["decisions"]:
            reflection["highlights"].append(f"Made {len(records['decisions'])} important decisions")
        
        # Extract challenges
        if categories["blockers"]:
            reflection["challenges"].append(f"Encountered {len(categories['blockers'])} issues/blockers")
        if categories["in_progress"]:
            reflection["challenges"].append(f"Have {len(categories['in_progress'])} pending tasks")
        
        # Generate suggestions
        if stats["total_entries"] < 3:
            reflection["suggestions"].append("Few records today; consider increasing daily journaling habit")
        if not categories["learning"]:
            reflection["suggestions"].append("No learning records today; consider scheduling learning time")
        if len(categories["blockers"]) > 2:
            reflection["suggestions"].append("Many issues today; prioritize resolving blockers")
        
        return reflection
    
    def generate_report(self, records: Dict, categories: Dict, reflection: Dict) -> str:
        """Generate review report"""
        report_lines = [
            f"# Daily Review Report - {self.today}",
            "",
            "## 📊 Today's Overview",
            "",
            f"- **Date**: {self.today}",
            f"- **Record Entries**: {categories['stats']['total_entries']}",
            f"- **Artifacts Generated**: {categories['stats']['artifacts_created']}",
            f"- **Productivity Score**: {reflection['productivity_score']}/100",
            "",
            "## ✅ Completed",
            ""
        ]
        
        if categories["completed_tasks"]:
            for task in categories["completed_tasks"][:10]:
                report_lines.append(f"- {task}")
        else:
            report_lines.append("- No completed records")
        
        report_lines.extend(["", "## 🔄 In Progress", ""])
        if categories["in_progress"]:
            for task in categories["in_progress"][:5]:
                report_lines.append(f"- {task}")
        else:
            report_lines.append("- No tasks in progress")
        
        report_lines.extend(["", "## ⚠️ Issues/Blockers", ""])
        if categories["blockers"]:
            for blocker in categories["blockers"][:5]:
                report_lines.append(f"- {blocker}")
        else:
            report_lines.append("- No blockers today 🎉")
        
        report_lines.extend(["", "## 📚 Learning/Growth", ""])
        if categories["learning"]:
            for item in categories["learning"][:5]:
                report_lines.append(f"- {item}")
        elif records["learnings"]:
            for learning in records["learnings"][:5]:
                report_lines.append(f"- {learning}")
        else:
            report_lines.append("- No learning records")
        
        report_lines.extend(["", "## 🎯 Today's Highlights", ""])
        if reflection["highlights"]:
            for highlight in reflection["highlights"]:
                report_lines.append(f"- {highlight}")
        else:
            report_lines.append("- Keep up the good work!")
        
        report_lines.extend(["", "## 💭 Reflection and Suggestions", ""])
        if reflection["suggestions"]:
            for suggestion in reflection["suggestions"]:
                report_lines.append(f"- {suggestion}")
        else:
            report_lines.append("- Good performance today, maintain momentum!")
        
        report_lines.extend(["", "## 📝 Tomorrow's Plan", "", "- [ ] To be filled...", ""])
        
        report_lines.extend(["---", "", f"*Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])
        
        return '\n'.join(report_lines)
    
    def save_to_memory(self, report: str):
        """Save review to MEMORY.md"""
        memory_file = self.workspace / "MEMORY.md"
        
        entry = f"\n\n## {self.today} Review\n\n"
        entry += f"**Productivity Score**: {self.reflection.get('productivity_score', 0)}/100\n\n"
        entry += "**Completed Today**: "
        if self.categories.get("completed_tasks"):
            entry += f"{len(self.categories['completed_tasks'])} tasks"
        else:
            entry += "None"
        entry += "\n\n"
        
        if memory_file.exists():
            content = memory_file.read_text(encoding='utf-8')
            # Append at the end of file
            content += entry
        else:
            content = f"# Long-Term Memory\n\n{entry}"
        
        memory_file.write_text(content, encoding='utf-8')
        print(f"✅ Review appended to MEMORY.md")
    
    def run(self, save_to_memory: bool = True, output_path: str = None) -> str:
        """Execute full review workflow"""
        print(f"🔍 Scanning records for {self.today}...")
        
        # 1. Scan today's records
        records = self.scan_today_records()
        print(f"  ✓ Found {len(records['memory_entries'])} record entries")
        print(f"  ✓ Found {len(records['artifacts'])} artifacts")
        
        # 2. Categorize
        print("📂 Categorizing activities...")
        categories = self.categorize_activities(records)
        self.categories = categories  # Save for later use
        
        # 3. Reflect and analyze
        print("💭 Reflecting and analyzing...")
        reflection = self.reflect_and_analyze(categories, records)
        self.reflection = reflection  # Save for later use
        
        # 4. Generate report
        print("📝 Generating review report...")
        report = self.generate_report(records, categories, reflection)
        
        # 5. Save report
        if output_path:
            output_file = Path(output_path)
        else:
            output_file = self.review_dir / f"review_{self.today}.md"
        
        output_file.write_text(report, encoding='utf-8')
        print(f"✅ Review report saved: {output_file}")
        
        # 6. Append to MEMORY.md
        if save_to_memory:
            self.save_to_memory(report)
        
        return report


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily Review Tool')
    parser.add_argument('--workspace', '-w', help='Workspace directory path')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--no-memory', action='store_true', help='Do not save to MEMORY.md')
    parser.add_argument('--date', '-d', help='Specify date (YYYY-MM-DD), defaults to today')
    
    args = parser.parse_args()
    
    # Create review instance
    review = DailyReview(args.workspace)
    
    # If date specified, override today's date
    if args.date:
        review.today = args.date
        review.yesterday = (datetime.strptime(args.date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Execute review
    report = review.run(
        save_to_memory=not args.no_memory,
        output_path=args.output
    )
    
    print("\n" + "="*50)
    print("Review Complete!")
    print("="*50)


if __name__ == "__main__":
    main()