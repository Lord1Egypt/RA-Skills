"""
Slacking Analyzer - Calculates developer "Slacking Index" (摸鱼指数).

This analyzer detects patterns that may indicate low engagement or
"slacking" behaviors by analyzing commit timing, frequency, consistency,
and output quality signals.

The Slacking Index is a composite score from 0 (hardworking) to 100 (slacking).
It is meant to be taken with a grain of humor, but backed by real data.

Signals analyzed:
  - Commit frequency vs active days (sparse = suspicious)
  - Single-line / trivial commit ratio (low-effort commits)
  - Large gaps between commits (disappearing acts)
  - Late-afternoon-only commits (deadline-driven behavior)
  - Low code output relative to active time span
  - Config-only / doc-only commit ratio (avoiding real code)
  - Copy-paste signals (very large additions with no deletions)
  - Friday-heavy / Monday-light patterns
"""

import logging
from collections import defaultdict, Counter
from typing import Dict

from src.analyzers.base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)

# Thresholds
TRIVIAL_COMMIT_LINE_THRESHOLD = 5  # commits with <= 5 lines changed
LARGE_GAP_HOURS = 72  # 3 days without commits
COPY_PASTE_RATIO = 10  # added/deleted ratio above this is suspicious


class SlackingAnalyzer(BaseAnalyzer):
    """
    Calculates a composite 'Slacking Index' for each developer.

    The index ranges from 0 to 100:
      - 0-20:  Highly engaged, consistent contributor
      - 21-40: Normal, healthy work pattern
      - 41-60: Some slacking signals detected
      - 61-80: Significant slacking indicators
      - 81-100: Professional slacker detected 🐟
    """

    def analyze(self) -> Dict:
        """
        Analyze slacking signals for each author.

        Returns:
            Dict keyed by author name with slacking metrics and index.
        """
        author_data = defaultdict(lambda: {
            "commit_times": [],
            "commit_dates": [],
            "lines_added": [],
            "lines_deleted": [],
            "files_changed": [],
            "commit_messages": [],
            "file_paths": [],
            "weekdays": [],
        })

        for commit in self._get_commits():
            author = commit.author.name
            data = author_data[author]
            data["commit_times"].append(commit.committer_date)
            data["commit_dates"].append(commit.committer_date.date())
            data["commit_messages"].append(commit.msg)
            data["weekdays"].append(commit.committer_date.weekday())

            total_added = 0
            total_deleted = 0
            files = 0
            paths = []
            for mod in commit.modified_files:
                total_added += mod.added_lines
                total_deleted += mod.deleted_lines
                files += 1
                if mod.new_path:
                    paths.append(mod.new_path)

            data["lines_added"].append(total_added)
            data["lines_deleted"].append(total_deleted)
            data["files_changed"].append(files)
            data["file_paths"].append(paths)

        result = {}
        for author, data in author_data.items():
            total = len(data["commit_times"])
            if total == 0:
                continue

            signals = {}

            # Signal 1: Commit sparsity (few commits over a long active span)
            dates = sorted(data["commit_dates"])
            if len(dates) >= 2:
                span_days = (dates[-1] - dates[0]).days or 1
            else:
                span_days = 1
            unique_days = len(set(dates))
            activity_ratio = unique_days / span_days if span_days > 0 else 1.0
            # Low activity ratio = high slacking signal
            signals["sparsity_score"] = max(0, min(25, round((1 - activity_ratio) * 30)))

            # Signal 2: Trivial commit ratio
            trivial_count = sum(
                1 for a, d in zip(data["lines_added"], data["lines_deleted"])
                if (a + d) <= TRIVIAL_COMMIT_LINE_THRESHOLD
            )
            trivial_ratio = trivial_count / total
            signals["trivial_commit_ratio"] = round(trivial_ratio, 3)
            signals["trivial_score"] = round(trivial_ratio * 20, 1)

            # Signal 3: Large gaps between commits
            sorted_times = sorted(data["commit_times"])
            gap_hours = []
            large_gap_count = 0
            for i in range(1, len(sorted_times)):
                gap = (sorted_times[i] - sorted_times[i - 1]).total_seconds() / 3600
                gap_hours.append(gap)
                if gap > LARGE_GAP_HOURS:
                    large_gap_count += 1
            avg_gap = sum(gap_hours) / len(gap_hours) if gap_hours else 0
            large_gap_ratio = large_gap_count / len(gap_hours) if gap_hours else 0
            signals["large_gap_ratio"] = round(large_gap_ratio, 3)
            signals["disappearance_score"] = round(large_gap_ratio * 20, 1)

            # Signal 4: Low output (total lines per active day)
            total_lines = sum(data["lines_added"]) + sum(data["lines_deleted"])
            lines_per_day = total_lines / unique_days if unique_days > 0 else 0
            # Very low output per day is a signal
            if lines_per_day < 20:
                signals["low_output_score"] = 15
            elif lines_per_day < 50:
                signals["low_output_score"] = 8
            elif lines_per_day < 100:
                signals["low_output_score"] = 3
            else:
                signals["low_output_score"] = 0

            # Signal 5: Config/doc-only commits (avoiding real code work)
            non_code_commits = 0
            for paths_list in data["file_paths"]:
                if paths_list and all(self._is_non_code(p) for p in paths_list):
                    non_code_commits += 1
            non_code_ratio = non_code_commits / total
            signals["non_code_ratio"] = round(non_code_ratio, 3)
            signals["non_code_score"] = round(non_code_ratio * 10, 1)

            # Signal 6: Friday-heavy / Monday-light pattern (procrastination)
            dow_counts = Counter(data["weekdays"])
            friday_count = dow_counts.get(4, 0)
            monday_count = dow_counts.get(0, 0)
            weekday_total = sum(1 for d in data["weekdays"] if d < 5) or 1
            friday_ratio = friday_count / weekday_total
            monday_ratio = monday_count / weekday_total
            # High Friday + Low Monday = deadline-driven
            procrastination = max(0, friday_ratio - monday_ratio)
            signals["procrastination_score"] = round(procrastination * 10, 1)

            # Signal 7: Copy-paste signal (very high added/deleted ratio)
            total_added = sum(data["lines_added"])
            total_deleted = sum(data["lines_deleted"])
            if total_deleted > 0:
                add_delete_ratio = total_added / total_deleted
            else:
                add_delete_ratio = total_added if total_added > 0 else 1
            copy_paste_signal = 1 if add_delete_ratio > COPY_PASTE_RATIO else 0
            signals["copy_paste_score"] = copy_paste_signal * 5

            # Composite Slacking Index (sum of all signals, capped at 100)
            slacking_index = min(100, round(
                signals["sparsity_score"]
                + signals["trivial_score"]
                + signals["disappearance_score"]
                + signals["low_output_score"]
                + signals["non_code_score"]
                + signals["procrastination_score"]
                + signals["copy_paste_score"]
            ))

            # Determine level
            if slacking_index <= 20:
                level = "🔥 Workaholic"
                level_cn = "🔥 工作狂"
            elif slacking_index <= 40:
                level = "✅ Normal"
                level_cn = "✅ 正常"
            elif slacking_index <= 60:
                level = "😏 Suspicious"
                level_cn = "😏 有嫌疑"
            elif slacking_index <= 80:
                level = "🐟 Slacker"
                level_cn = "🐟 摸鱼达人"
            else:
                level = "🏆 Professional Slacker"
                level_cn = "🏆 摸鱼大师"

            result[author] = {
                "slacking_index": slacking_index,
                "slacking_level": level,
                "slacking_level_cn": level_cn,
                "total_commits": total,
                "active_span_days": span_days,
                "unique_active_days": unique_days,
                "activity_ratio": round(activity_ratio, 3),
                "trivial_commit_ratio": signals["trivial_commit_ratio"],
                "large_gap_ratio": signals["large_gap_ratio"],
                "avg_gap_hours": round(avg_gap, 1),
                "lines_per_active_day": round(lines_per_day, 1),
                "non_code_commit_ratio": signals["non_code_ratio"],
                "friday_ratio": round(friday_ratio, 3),
                "monday_ratio": round(monday_ratio, 3),
                "signal_breakdown": {
                    "sparsity": signals["sparsity_score"],
                    "trivial_commits": signals["trivial_score"],
                    "disappearance": signals["disappearance_score"],
                    "low_output": signals["low_output_score"],
                    "non_code": signals["non_code_score"],
                    "procrastination": signals["procrastination_score"],
                    "copy_paste": signals["copy_paste_score"],
                },
            }

        return result

    @staticmethod
    def _is_non_code(filepath: str) -> bool:
        """Check if a file is a non-code file (config, docs, etc.)."""
        path_lower = filepath.lower()
        non_code_exts = [
            ".md", ".rst", ".txt", ".adoc", ".yml", ".yaml", ".json",
            ".toml", ".ini", ".cfg", ".env", ".lock", ".gitignore",
            ".editorconfig", ".prettierrc",
        ]
        non_code_names = [
            "readme", "changelog", "license", "contributing",
            "dockerfile", "makefile", ".github/",
        ]
        return (
            any(path_lower.endswith(ext) for ext in non_code_exts)
            or any(name in path_lower for name in non_code_names)
        )
