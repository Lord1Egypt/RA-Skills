"""
Efficiency Analyzer - Measures development efficiency and productivity.

Metrics include:
  - Code churn rate (lines added then quickly deleted)
  - Rework ratio (changes to recently modified files)
  - Commit throughput over time
  - File ownership concentration
  - Bus factor estimation
  - Lines of code per commit (productivity proxy)
"""

import logging
from collections import defaultdict, Counter
from datetime import timedelta
from typing import Dict, List

from src.analyzers.base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)


class EfficiencyAnalyzer(BaseAnalyzer):
    """Measures development efficiency and productivity per author."""

    # If a file is modified again within this many days, count it as rework
    REWORK_WINDOW_DAYS = 7

    def analyze(self) -> Dict:
        """
        Analyze development efficiency for each author.

        Returns:
            Dict keyed by author name with efficiency metrics.
        """
        author_data = defaultdict(lambda: {
            "commits": [],
            "total_added": 0,
            "total_deleted": 0,
            "files_touched": Counter(),
            "file_mod_dates": defaultdict(list),  # file -> [dates]
        })

        # Global file modification tracking for rework detection
        global_file_history = defaultdict(list)  # file -> [(date, author)]

        for commit in self._get_commits():
            author = commit.author.name
            data = author_data[author]
            data["commits"].append(commit)

            for mod in commit.modified_files:
                filepath = mod.new_path or mod.old_path
                if not filepath:
                    continue

                data["total_added"] += mod.added_lines
                data["total_deleted"] += mod.deleted_lines
                data["files_touched"][filepath] += 1
                data["file_mod_dates"][filepath].append(commit.committer_date)

                global_file_history[filepath].append(
                    (commit.committer_date, author)
                )

        # Compute bus factor (number of unique authors per file)
        file_owners = defaultdict(set)
        for filepath, entries in global_file_history.items():
            for _, author in entries:
                file_owners[filepath].add(author)

        result = {}
        for author, data in author_data.items():
            commits = data["commits"]
            total = len(commits)
            if total == 0:
                continue

            total_added = data["total_added"]
            total_deleted = data["total_deleted"]
            churn_rate = round(total_deleted / total_added, 3) if total_added > 0 else 0

            # Calculate rework ratio
            rework_count = self._calculate_rework(data["file_mod_dates"])
            total_file_mods = sum(data["files_touched"].values())
            rework_ratio = round(rework_count / total_file_mods, 3) if total_file_mods else 0

            # File ownership: files where this author made >50% of total modifications
            owned_files = 0
            for filepath, count in data["files_touched"].items():
                total_mods = sum(
                    1 for _, a in global_file_history.get(filepath, [])
                )
                if total_mods > 0 and (count / total_mods) > 0.5:
                    owned_files += 1

            total_unique_files = len(data["files_touched"])

            # Productivity: lines per commit
            lines_per_commit = round(
                (total_added + total_deleted) / total, 1
            )

            # Commit throughput by week
            weekly_throughput = self._weekly_throughput(commits)

            result[author] = {
                "total_commits": total,
                "total_lines_added": total_added,
                "total_lines_deleted": total_deleted,
                "churn_rate": churn_rate,
                "rework_ratio": rework_ratio,
                "lines_per_commit": lines_per_commit,
                "unique_files_touched": total_unique_files,
                "owned_files_count": owned_files,
                "ownership_ratio": round(owned_files / total_unique_files, 3) if total_unique_files else 0,
                "weekly_throughput": weekly_throughput,
            }

        # Add global bus factor
        bus_factors = []
        for filepath, owners in file_owners.items():
            bus_factors.append(len(owners))
        avg_bus_factor = round(sum(bus_factors) / len(bus_factors), 2) if bus_factors else 0

        # Attach bus factor to each author's result
        for author in result:
            result[author]["repo_avg_bus_factor"] = avg_bus_factor

        return result

    def _calculate_rework(self, file_mod_dates: Dict[str, List]) -> int:
        """Count file modifications that happened within the rework window."""
        rework_count = 0
        for filepath, dates in file_mod_dates.items():
            sorted_dates = sorted(dates)
            for i in range(1, len(sorted_dates)):
                delta = (sorted_dates[i] - sorted_dates[i - 1]).days
                if delta <= self.REWORK_WINDOW_DAYS:
                    rework_count += 1
        return rework_count

    @staticmethod
    def _weekly_throughput(commits) -> Dict[str, int]:
        """Calculate commit counts per ISO week."""
        weekly = Counter()
        for c in commits:
            iso = c.committer_date.isocalendar()
            week_key = f"{iso[0]}-W{iso[1]:02d}"
            weekly[week_key] += 1
        return dict(sorted(weekly.items()))
