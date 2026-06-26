"""
Markdown Reporter - Generates comprehensive analysis reports in Markdown format.

Includes:
  - Per-developer metrics across all 5 analysis dimensions
  - Slacking Index (摸鱼指数)
  - Developer Evaluation (score, grade, strengths, weaknesses, suggestions, verdict)
  - Cross-developer comparison table
"""

from typing import Dict

from src.reporters.base_reporter import BaseReporter


class MarkdownReporter(BaseReporter):
    """Generates beautiful Markdown reports from analysis metrics."""

    def generate(self, metrics: Dict) -> str:
        """Generate a Markdown report."""
        lines = []
        lines.append("# 📊 Code Analysis Report\n")

        for repo_name, repo_metrics in metrics.items():
            lines.append(f"## 📁 Repository: {repo_name}\n")

            # Collect all authors across analyzers
            all_authors = set()
            for key, analyzer_data in repo_metrics.items():
                if isinstance(analyzer_data, dict) and key != "evaluations":
                    all_authors.update(analyzer_data.keys())

            if not all_authors:
                lines.append("_No data available for this repository._\n")
                continue

            for author in sorted(all_authors):
                lines.append(f"### 👤 {author}\n")

                # ── Developer Evaluation (if available) ──
                eval_data = repo_metrics.get("evaluations", {}).get(author, {})
                if eval_data:
                    lines.append("#### 🏆 Developer Evaluation\n")
                    score = eval_data.get("overall_score", 0)
                    grade = eval_data.get("grade", "?")
                    verdict = eval_data.get("verdict", "")
                    lines.append(f"**Overall Score: {score}/100 (Grade: {grade})**\n")
                    lines.append(f"> {verdict}\n")

                    # Dimension scores
                    dim_scores = eval_data.get("dimension_scores", {})
                    if dim_scores:
                        lines.append("**Dimension Scores:**\n")
                        lines.append("| Dimension | Score |")
                        lines.append("|-----------|-------|")
                        dim_name_map = {
                            "commit_discipline": "📝 Commit Discipline",
                            "work_consistency": "⏰ Work Consistency",
                            "efficiency": "🚀 Efficiency",
                            "code_quality": "🔍 Code Quality",
                            "code_style": "🎨 Code Style",
                            "engagement": "💪 Engagement",
                        }
                        for dim, s in dim_scores.items():
                            name = dim_name_map.get(dim, dim)
                            bar = self._score_bar(s)
                            lines.append(f"| {name} | {s:.0f}/100 {bar} |")
                        lines.append("")

                    # Strengths
                    strengths = eval_data.get("strengths", [])
                    if strengths:
                        lines.append("**✅ Strengths:**\n")
                        for s in strengths:
                            lines.append(f"- {s}")
                        lines.append("")

                    # Weaknesses
                    weaknesses = eval_data.get("weaknesses", [])
                    if weaknesses:
                        lines.append("**❌ Weaknesses:**\n")
                        for w in weaknesses:
                            lines.append(f"- {w}")
                        lines.append("")

                    # Suggestions
                    suggestions = eval_data.get("suggestions", [])
                    if suggestions:
                        lines.append("**💡 Suggestions:**\n")
                        for sg in suggestions:
                            lines.append(f"- {sg}")
                        lines.append("")

                # ── Slacking Index ──
                slacking_data = repo_metrics.get("slacking", {}).get(author, {})
                if slacking_data:
                    lines.append("#### 🐟 Slacking Index (摸鱼指数)\n")
                    idx = slacking_data.get("slacking_index", 0)
                    level = slacking_data.get("slacking_level_cn", "")
                    level_en = slacking_data.get("slacking_level", "")
                    lines.append(f"**Slacking Index: {idx}/100 — {level} ({level_en})**\n")

                    lines.append("| Signal | Value |")
                    lines.append("|--------|-------|")
                    lines.append(f"| Activity Ratio | {slacking_data.get('activity_ratio', 0):.1%} |")
                    lines.append(f"| Trivial Commit Ratio | {slacking_data.get('trivial_commit_ratio', 0):.1%} |")
                    lines.append(f"| Large Gap Ratio | {slacking_data.get('large_gap_ratio', 0):.1%} |")
                    lines.append(f"| Avg Gap (hours) | {slacking_data.get('avg_gap_hours', 0)} |")
                    lines.append(f"| Lines/Active Day | {slacking_data.get('lines_per_active_day', 0)} |")
                    lines.append(f"| Non-code Commit Ratio | {slacking_data.get('non_code_commit_ratio', 0):.1%} |")
                    lines.append(f"| Friday Ratio | {slacking_data.get('friday_ratio', 0):.1%} |")
                    lines.append(f"| Monday Ratio | {slacking_data.get('monday_ratio', 0):.1%} |")
                    lines.append("")

                    breakdown = slacking_data.get("signal_breakdown", {})
                    if breakdown:
                        lines.append("**Signal Breakdown:**\n")
                        lines.append("| Signal | Score |")
                        lines.append("|--------|-------|")
                        signal_names = {
                            "sparsity": "Commit Sparsity",
                            "trivial_commits": "Trivial Commits",
                            "disappearance": "Disappearance Acts",
                            "low_output": "Low Output",
                            "non_code": "Non-code Only",
                            "procrastination": "Procrastination",
                            "copy_paste": "Copy-paste Signal",
                        }
                        for key, val in breakdown.items():
                            name = signal_names.get(key, key)
                            lines.append(f"| {name} | {val} |")
                        lines.append("")

                # ── Commit Patterns ──
                commit_data = repo_metrics.get("commit_patterns", {}).get(author, {})
                if commit_data:
                    lines.append("#### 📝 Commit Patterns\n")
                    lines.append("| Metric | Value |")
                    lines.append("|--------|-------|")
                    lines.append(f"| Total Commits | {commit_data.get('total_commits', 0)} |")
                    lines.append(f"| Non-merge Commits | {commit_data.get('non_merge_commits', 0)} |")
                    lines.append(f"| Merge Ratio | {commit_data.get('merge_ratio', 0):.1%} |")
                    lines.append(f"| Active Span (days) | {commit_data.get('active_span_days', 0)} |")
                    lines.append(f"| Unique Active Days | {commit_data.get('unique_active_days', 0)} |")
                    lines.append(f"| Avg Commits/Active Day | {commit_data.get('avg_commits_per_active_day', 0)} |")
                    lines.append(f"| Avg Message Length | {commit_data.get('avg_message_length', 0)} |")
                    lines.append(f"| Avg Lines Added | {commit_data.get('avg_lines_added', 0)} |")
                    lines.append(f"| Avg Lines Deleted | {commit_data.get('avg_lines_deleted', 0)} |")
                    lines.append(f"| Avg Files Changed | {commit_data.get('avg_files_changed', 0)} |")
                    lines.append(f"| Total Lines Added | {commit_data.get('total_lines_added', 0):,} |")
                    lines.append(f"| Total Lines Deleted | {commit_data.get('total_lines_deleted', 0):,} |")
                    lines.append("")

                # ── Work Habits ──
                habit_data = repo_metrics.get("work_habits", {}).get(author, {})
                if habit_data:
                    lines.append("#### ⏰ Work Habits\n")
                    lines.append("| Metric | Value |")
                    lines.append("|--------|-------|")
                    lines.append(f"| Peak Hour | {habit_data.get('peak_hour', 'N/A')}:00 |")
                    lines.append(f"| Weekday Commits | {habit_data.get('weekday_commits', 0)} |")
                    lines.append(f"| Weekend Commits | {habit_data.get('weekend_commits', 0)} |")
                    lines.append(f"| Weekend Ratio | {habit_data.get('weekend_ratio', 0):.1%} |")
                    lines.append(f"| Late Night Ratio | {habit_data.get('late_night_ratio', 0):.1%} |")
                    lines.append(f"| Longest Streak (days) | {habit_data.get('longest_streak_days', 0)} |")
                    lines.append(f"| Avg Gap Between Commits (hrs) | {habit_data.get('avg_gap_between_commits_hours', 0)} |")
                    lines.append("")

                    # Time slot distribution
                    slots = habit_data.get("time_slot_distribution", {})
                    if slots:
                        lines.append("**Time Slot Distribution:**\n")
                        lines.append("| Time Slot | Commits |")
                        lines.append("|-----------|---------|")
                        for slot, count in sorted(slots.items()):
                            lines.append(f"| {slot.replace('_', ' ').title()} | {count} |")
                        lines.append("")

                    # Day of week distribution
                    dow = habit_data.get("day_of_week_distribution", {})
                    if dow:
                        lines.append("**Day of Week Distribution:**\n")
                        lines.append("| Day | Commits |")
                        lines.append("|-----|---------|")
                        for day, count in dow.items():
                            lines.append(f"| {day} | {count} |")
                        lines.append("")

                # ── Efficiency ──
                eff_data = repo_metrics.get("efficiency", {}).get(author, {})
                if eff_data:
                    lines.append("#### 🚀 Development Efficiency\n")
                    lines.append("| Metric | Value |")
                    lines.append("|--------|-------|")
                    lines.append(f"| Churn Rate | {eff_data.get('churn_rate', 0):.1%} |")
                    lines.append(f"| Rework Ratio | {eff_data.get('rework_ratio', 0):.1%} |")
                    lines.append(f"| Lines per Commit | {eff_data.get('lines_per_commit', 0)} |")
                    lines.append(f"| Unique Files Touched | {eff_data.get('unique_files_touched', 0)} |")
                    lines.append(f"| Owned Files | {eff_data.get('owned_files_count', 0)} |")
                    lines.append(f"| Ownership Ratio | {eff_data.get('ownership_ratio', 0):.1%} |")
                    lines.append(f"| Repo Avg Bus Factor | {eff_data.get('repo_avg_bus_factor', 0)} |")
                    lines.append("")

                # ── Code Style ──
                style_data = repo_metrics.get("code_style", {}).get(author, {})
                if style_data:
                    lines.append("#### 🎨 Code Style\n")
                    lines.append("| Metric | Value |")
                    lines.append("|--------|-------|")
                    lines.append(f"| Conventional Commit Ratio | {style_data.get('conventional_commit_ratio', 0):.1%} |")
                    lines.append(f"| Issue Reference Ratio | {style_data.get('issue_reference_ratio', 0):.1%} |")
                    lines.append(f"| Avg Change Size (lines) | {style_data.get('avg_change_size_lines', 0)} |")
                    lines.append("")

                    lang_dist = style_data.get("language_distribution", {})
                    if lang_dist:
                        lines.append("**Language Distribution:**\n")
                        lines.append("| Extension | Modifications |")
                        lines.append("|-----------|---------------|")
                        for ext, count in sorted(lang_dist.items(), key=lambda x: -x[1]):
                            lines.append(f"| {ext} | {count} |")
                        lines.append("")

                    cat_dist = style_data.get("file_category_distribution", {})
                    if cat_dist:
                        lines.append("**File Category Distribution:**\n")
                        lines.append("| Category | Count |")
                        lines.append("|----------|-------|")
                        for cat, count in sorted(cat_dist.items(), key=lambda x: -x[1]):
                            lines.append(f"| {cat} | {count} |")
                        lines.append("")

                # ── Code Quality ──
                quality_data = repo_metrics.get("code_quality", {}).get(author, {})
                if quality_data:
                    lines.append("#### 🔍 Code Quality\n")
                    lines.append("| Metric | Value |")
                    lines.append("|--------|-------|")
                    lines.append(f"| Bug Fix Ratio | {quality_data.get('bug_fix_ratio', 0):.1%} |")
                    lines.append(f"| Revert Ratio | {quality_data.get('revert_ratio', 0):.1%} |")
                    lines.append(f"| Large Commit Ratio | {quality_data.get('large_commit_ratio', 0):.1%} |")
                    lines.append(f"| Test Modification Ratio | {quality_data.get('test_modification_ratio', 0):.1%} |")
                    lines.append(f"| Doc Modification Ratio | {quality_data.get('doc_modification_ratio', 0):.1%} |")
                    lines.append(f"| Avg Commit Size | {quality_data.get('avg_commit_size', 0)} |")
                    lines.append(f"| Median Commit Size | {quality_data.get('median_commit_size', 0)} |")
                    if quality_data.get("avg_python_complexity", 0) > 0:
                        lines.append(f"| Avg Python Complexity | {quality_data.get('avg_python_complexity', 0)} |")
                    lines.append("")

                lines.append("---\n")

        # Comparison summary if multiple authors
        lines.append(self._generate_comparison_summary(metrics))

        # Evaluation leaderboard
        lines.append(self._generate_evaluation_leaderboard(metrics))

        # Slacking leaderboard
        lines.append(self._generate_slacking_leaderboard(metrics))

        return "\n".join(lines)

    def _generate_comparison_summary(self, metrics: Dict) -> str:
        """Generate a comparison summary table across all authors."""
        author_summary = {}
        for repo_name, repo_metrics in metrics.items():
            commit_data = repo_metrics.get("commit_patterns", {})
            habit_data = repo_metrics.get("work_habits", {})
            eff_data = repo_metrics.get("efficiency", {})
            quality_data = repo_metrics.get("code_quality", {})

            for author in commit_data:
                if author not in author_summary:
                    author_summary[author] = {
                        "total_commits": 0,
                        "total_lines": 0,
                        "avg_commits_day": 0,
                        "weekend_ratio": 0,
                        "late_night_ratio": 0,
                        "bug_fix_ratio": 0,
                        "churn_rate": 0,
                    }

                cd = commit_data.get(author, {})
                hd = habit_data.get(author, {})
                ed = eff_data.get(author, {})
                qd = quality_data.get(author, {})

                author_summary[author]["total_commits"] += cd.get("total_commits", 0)
                author_summary[author]["total_lines"] += cd.get("total_lines_added", 0) + cd.get("total_lines_deleted", 0)
                author_summary[author]["avg_commits_day"] = cd.get("avg_commits_per_active_day", 0)
                author_summary[author]["weekend_ratio"] = hd.get("weekend_ratio", 0)
                author_summary[author]["late_night_ratio"] = hd.get("late_night_ratio", 0)
                author_summary[author]["bug_fix_ratio"] = qd.get("bug_fix_ratio", 0)
                author_summary[author]["churn_rate"] = ed.get("churn_rate", 0)

        if len(author_summary) < 2:
            return ""

        lines = []
        lines.append("## 📋 Author Comparison Summary\n")
        lines.append("| Author | Commits | Lines Changed | Commits/Day | Weekend % | Late Night % | Bug Fix % | Churn Rate |")
        lines.append("|--------|---------|---------------|-------------|-----------|-------------|-----------|------------|")

        for author, data in sorted(author_summary.items(), key=lambda x: -x[1]["total_commits"]):
            lines.append(
                f"| {author} "
                f"| {data['total_commits']} "
                f"| {data['total_lines']:,} "
                f"| {data['avg_commits_day']} "
                f"| {data['weekend_ratio']:.1%} "
                f"| {data['late_night_ratio']:.1%} "
                f"| {data['bug_fix_ratio']:.1%} "
                f"| {data['churn_rate']:.1%} |"
            )

        lines.append("")
        return "\n".join(lines)

    def _generate_evaluation_leaderboard(self, metrics: Dict) -> str:
        """Generate a leaderboard ranked by overall evaluation score."""
        all_evals = {}
        for repo_name, repo_metrics in metrics.items():
            evals = repo_metrics.get("evaluations", {})
            for author, ev in evals.items():
                all_evals[author] = ev

        if not all_evals:
            return ""

        lines = []
        lines.append("## 🏆 Developer Leaderboard\n")
        lines.append("| Rank | Developer | Score | Grade | Verdict |")
        lines.append("|------|-----------|-------|-------|---------|")

        ranked = sorted(all_evals.items(), key=lambda x: -x[1].get("overall_score", 0))
        for i, (author, ev) in enumerate(ranked, 1):
            score = ev.get("overall_score", 0)
            grade = ev.get("grade", "?")
            verdict = ev.get("verdict", "")
            lines.append(f"| {i} | {author} | {score} | {grade} | {verdict} |")

        lines.append("")
        return "\n".join(lines)

    def _generate_slacking_leaderboard(self, metrics: Dict) -> str:
        """Generate a slacking index leaderboard."""
        all_slacking = {}
        for repo_name, repo_metrics in metrics.items():
            slacking = repo_metrics.get("slacking", {})
            for author, sd in slacking.items():
                all_slacking[author] = sd

        if not all_slacking:
            return ""

        lines = []
        lines.append("## 🐟 Slacking Index Leaderboard (摸鱼排行榜)\n")
        lines.append("| Rank | Developer | Slacking Index | Level | Lines/Day |")
        lines.append("|------|-----------|----------------|-------|-----------|")

        ranked = sorted(all_slacking.items(), key=lambda x: -x[1].get("slacking_index", 0))
        for i, (author, sd) in enumerate(ranked, 1):
            idx = sd.get("slacking_index", 0)
            level = sd.get("slacking_level_cn", "")
            lpd = sd.get("lines_per_active_day", 0)
            lines.append(f"| {i} | {author} | {idx}/100 | {level} | {lpd} |")

        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _score_bar(score: float) -> str:
        """Generate a text-based score bar."""
        filled = int(score / 10)
        empty = 10 - filled
        return "█" * filled + "░" * empty
