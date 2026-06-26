"""
Developer Evaluator - Generates honest, direct evaluations for each developer.

Produces per-developer:
  - Overall score (0-100, with letter grade)
  - Strengths list (sharp, specific)
  - Weaknesses list (blunt, actionable)
  - Personalized suggestions
  - A one-line "verdict" summary

The tone is serious, direct, and constructive — no sugarcoating.
"""

import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


# Scoring weights for each dimension (total = 100)
DIMENSION_WEIGHTS = {
    "commit_discipline": 15,    # Commit habits, message quality, conventions
    "work_consistency": 15,     # Regular hours, streak, not bursty
    "efficiency": 20,           # Churn, rework, output
    "code_quality": 25,         # Bug fix ratio, revert, complexity, tests
    "code_style": 10,           # Conventional commits, issue refs
    "engagement": 15,           # Slacking index inverse
}


class DeveloperEvaluator:
    """
    Synthesizes all analyzer metrics into a brutally honest developer evaluation.

    Each developer gets:
      - A composite score with letter grade
      - A list of strengths and weaknesses
      - Concrete suggestions
      - A one-line verdict
    """

    def evaluate(self, repo_metrics: Dict) -> Dict:
        """
        Evaluate all developers in a repository.

        Args:
            repo_metrics: Dict with keys like 'commit_patterns', 'work_habits',
                          'efficiency', 'code_style', 'code_quality', 'slacking'.

        Returns:
            Dict keyed by author with evaluation results.
        """
        # Collect all authors
        all_authors = set()
        for analyzer_data in repo_metrics.values():
            if isinstance(analyzer_data, dict):
                all_authors.update(analyzer_data.keys())

        results = {}
        for author in sorted(all_authors):
            commit = repo_metrics.get("commit_patterns", {}).get(author, {})
            habit = repo_metrics.get("work_habits", {}).get(author, {})
            eff = repo_metrics.get("efficiency", {}).get(author, {})
            style = repo_metrics.get("code_style", {}).get(author, {})
            quality = repo_metrics.get("code_quality", {}).get(author, {})
            slacking = repo_metrics.get("slacking", {}).get(author, {})

            if not commit:
                continue

            # Calculate dimension scores (each 0-100, then weighted)
            dim_scores = {}
            dim_scores["commit_discipline"] = self._score_commit_discipline(commit, style)
            dim_scores["work_consistency"] = self._score_work_consistency(habit)
            dim_scores["efficiency"] = self._score_efficiency(eff)
            dim_scores["code_quality"] = self._score_code_quality(quality)
            dim_scores["code_style"] = self._score_code_style(style)
            dim_scores["engagement"] = self._score_engagement(slacking)

            # Weighted composite
            total_score = 0
            for dim, score in dim_scores.items():
                weight = DIMENSION_WEIGHTS.get(dim, 0)
                total_score += score * (weight / 100.0)
            total_score = round(total_score, 1)

            grade = self._letter_grade(total_score)

            # Generate strengths, weaknesses, suggestions
            strengths = self._identify_strengths(
                commit, habit, eff, style, quality, slacking, dim_scores
            )
            weaknesses = self._identify_weaknesses(
                commit, habit, eff, style, quality, slacking, dim_scores
            )
            suggestions = self._generate_suggestions(
                commit, habit, eff, style, quality, slacking, dim_scores
            )
            verdict = self._generate_verdict(total_score, dim_scores, slacking)

            results[author] = {
                "overall_score": total_score,
                "grade": grade,
                "dimension_scores": dim_scores,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "suggestions": suggestions,
                "verdict": verdict,
            }

        return results

    # ─── Dimension Scorers ────────────────────────────────────────────────

    def _score_commit_discipline(self, commit: Dict, style: Dict) -> float:
        """Score commit discipline (0-100)."""
        score = 50.0  # baseline

        # Commit frequency
        avg_per_day = commit.get("avg_commits_per_active_day", 0)
        if 2 <= avg_per_day <= 8:
            score += 15
        elif avg_per_day > 8:
            score += 5  # too many micro-commits
        elif avg_per_day > 0:
            score += 8

        # Message quality
        avg_msg_len = commit.get("avg_message_length", 0)
        if 30 <= avg_msg_len <= 100:
            score += 15
        elif avg_msg_len > 100:
            score += 10
        elif avg_msg_len > 15:
            score += 5

        # Merge ratio (too high is bad)
        merge_ratio = commit.get("merge_ratio", 0)
        if merge_ratio < 0.3:
            score += 10
        elif merge_ratio < 0.5:
            score += 5

        # Conventional commits
        conv_ratio = style.get("conventional_commit_ratio", 0)
        if conv_ratio > 0.8:
            score += 10
        elif conv_ratio > 0.5:
            score += 5

        return min(100, max(0, score))

    def _score_work_consistency(self, habit: Dict) -> float:
        """Score work pattern consistency (0-100)."""
        score = 50.0

        # Weekend ratio (some is ok, too much is bad)
        weekend_ratio = habit.get("weekend_ratio", 0)
        if weekend_ratio < 0.1:
            score += 15  # healthy work-life balance
        elif weekend_ratio < 0.2:
            score += 10
        else:
            score -= 5  # working too many weekends

        # Late night ratio
        late_night = habit.get("late_night_ratio", 0)
        if late_night < 0.1:
            score += 15
        elif late_night < 0.2:
            score += 5
        else:
            score -= 10  # unhealthy pattern

        # Streak (consistency)
        streak = habit.get("longest_streak_days", 0)
        if streak >= 10:
            score += 15
        elif streak >= 5:
            score += 10
        elif streak >= 3:
            score += 5

        # Average gap
        gap = habit.get("avg_gap_between_commits_hours", 999)
        if gap < 24:
            score += 5
        elif gap < 48:
            score += 2

        return min(100, max(0, score))

    def _score_efficiency(self, eff: Dict) -> float:
        """Score development efficiency (0-100)."""
        score = 50.0

        # Churn rate
        churn = eff.get("churn_rate", 0)
        if churn < 0.3:
            score += 20
        elif churn < 0.5:
            score += 10
        elif churn < 0.8:
            score += 0
        else:
            score -= 10

        # Rework ratio
        rework = eff.get("rework_ratio", 0)
        if rework < 0.15:
            score += 15
        elif rework < 0.3:
            score += 5
        else:
            score -= 10

        # Lines per commit (sweet spot)
        lpc = eff.get("lines_per_commit", 0)
        if 20 <= lpc <= 300:
            score += 15
        elif lpc > 300:
            score += 5  # large but may be fine
        elif lpc > 0:
            score += 3  # very small commits

        return min(100, max(0, score))

    def _score_code_quality(self, quality: Dict) -> float:
        """Score code quality (0-100)."""
        score = 50.0

        # Bug fix ratio (lower is better)
        bug_fix = quality.get("bug_fix_ratio", 0)
        if bug_fix < 0.15:
            score += 15
        elif bug_fix < 0.3:
            score += 5
        elif bug_fix > 0.5:
            score -= 10

        # Revert ratio
        revert = quality.get("revert_ratio", 0)
        if revert < 0.02:
            score += 10
        elif revert < 0.05:
            score += 5
        else:
            score -= 10

        # Large commit ratio
        large = quality.get("large_commit_ratio", 0)
        if large < 0.1:
            score += 10
        elif large < 0.2:
            score += 5
        else:
            score -= 5

        # Test modification ratio (higher is better)
        test_ratio = quality.get("test_modification_ratio", 0)
        if test_ratio > 0.2:
            score += 15
        elif test_ratio > 0.1:
            score += 10
        elif test_ratio > 0.05:
            score += 5

        # Complexity
        complexity = quality.get("avg_python_complexity", 0)
        if 0 < complexity <= 5:
            score += 10
        elif complexity <= 10:
            score += 5
        elif complexity > 15:
            score -= 10

        return min(100, max(0, score))

    def _score_code_style(self, style: Dict) -> float:
        """Score code style adherence (0-100)."""
        score = 50.0

        conv = style.get("conventional_commit_ratio", 0)
        if conv > 0.8:
            score += 25
        elif conv > 0.5:
            score += 15
        elif conv > 0.2:
            score += 5

        issue_ref = style.get("issue_reference_ratio", 0)
        if issue_ref > 0.5:
            score += 20
        elif issue_ref > 0.3:
            score += 10
        elif issue_ref > 0.1:
            score += 5

        return min(100, max(0, score))

    def _score_engagement(self, slacking: Dict) -> float:
        """Score engagement (inverse of slacking index)."""
        idx = slacking.get("slacking_index", 50)
        return max(0, min(100, 100 - idx))

    # ─── Strength / Weakness / Suggestion Generators ──────────────────────

    def _identify_strengths(
        self, commit, habit, eff, style, quality, slacking, dim_scores
    ) -> List[str]:
        """Identify concrete strengths based on metrics."""
        strengths = []

        if commit.get("avg_commits_per_active_day", 0) >= 3:
            strengths.append("Consistent committer — maintains a healthy commit rhythm")

        if commit.get("avg_message_length", 0) >= 40:
            strengths.append("Writes descriptive commit messages — good traceability")

        if habit.get("weekend_ratio", 1) < 0.05:
            strengths.append("Healthy work-life balance — rarely works weekends")

        if habit.get("longest_streak_days", 0) >= 7:
            strengths.append(
                f"Strong consistency — {habit['longest_streak_days']}-day coding streak"
            )

        if eff.get("churn_rate", 1) < 0.3:
            strengths.append("Low code churn — writes stable, well-thought-out code")

        if eff.get("rework_ratio", 1) < 0.15:
            strengths.append("Low rework rate — gets it right the first time")

        if quality.get("test_modification_ratio", 0) > 0.2:
            strengths.append("Strong testing discipline — regularly updates tests")

        if quality.get("bug_fix_ratio", 1) < 0.15:
            strengths.append("Low bug-fix ratio — code quality is high from the start")

        if quality.get("revert_ratio", 1) < 0.02:
            strengths.append("Near-zero reverts — careful and deliberate commits")

        if style.get("conventional_commit_ratio", 0) > 0.7:
            strengths.append("Follows Conventional Commits standard — team-friendly")

        if style.get("issue_reference_ratio", 0) > 0.5:
            strengths.append("Links commits to issues — excellent traceability")

        if slacking.get("slacking_index", 100) <= 20:
            strengths.append("Highly engaged — no slacking signals detected")

        if eff.get("ownership_ratio", 0) > 0.5:
            strengths.append("Strong code ownership — deeply invested in the codebase")

        return strengths[:8]  # cap at 8

    def _identify_weaknesses(
        self, commit, habit, eff, style, quality, slacking, dim_scores
    ) -> List[str]:
        """Identify concrete weaknesses — blunt and actionable."""
        weaknesses = []

        if commit.get("avg_message_length", 999) < 20:
            weaknesses.append(
                "Lazy commit messages — average length under 20 chars. "
                "This makes git history useless for debugging."
            )

        if commit.get("merge_ratio", 0) > 0.5:
            weaknesses.append(
                f"Merge ratio at {commit['merge_ratio']:.0%} — "
                "are you actually writing code or just merging?"
            )

        if habit.get("late_night_ratio", 0) > 0.2:
            weaknesses.append(
                f"Late-night coding at {habit['late_night_ratio']:.0%} — "
                "this isn't sustainable and leads to buggy code."
            )

        if habit.get("weekend_ratio", 0) > 0.25:
            weaknesses.append(
                f"Weekend work at {habit['weekend_ratio']:.0%} — "
                "either poor time management or unreasonable workload."
            )

        if eff.get("churn_rate", 0) > 0.6:
            weaknesses.append(
                f"High code churn ({eff['churn_rate']:.0%}) — "
                "you're deleting almost as much as you write. "
                "Stop coding before you think."
            )

        if eff.get("rework_ratio", 0) > 0.3:
            weaknesses.append(
                f"Rework ratio at {eff['rework_ratio']:.0%} — "
                "constantly re-editing the same files within a week. "
                "Plan better before you start."
            )

        if quality.get("bug_fix_ratio", 0) > 0.4:
            weaknesses.append(
                f"Bug fix ratio at {quality['bug_fix_ratio']:.0%} — "
                "nearly half your commits are fixing bugs. "
                "Write tests. Review your own code."
            )

        if quality.get("revert_ratio", 0) > 0.05:
            weaknesses.append(
                f"Revert ratio at {quality['revert_ratio']:.0%} — "
                "too many rollbacks. Test before pushing."
            )

        if quality.get("large_commit_ratio", 0) > 0.2:
            weaknesses.append(
                f"Large commits ({quality['large_commit_ratio']:.0%} over 500 lines) — "
                "impossible to review. Break them down."
            )

        if quality.get("test_modification_ratio", 0) < 0.05:
            weaknesses.append(
                "Almost never touches test files — "
                "either no tests exist or you're ignoring them."
            )

        if style.get("conventional_commit_ratio", 0) < 0.2:
            weaknesses.append(
                "Ignores commit conventions — "
                "makes automated changelogs impossible."
            )

        if slacking.get("slacking_index", 0) > 60:
            weaknesses.append(
                f"Slacking index at {slacking['slacking_index']} — "
                "multiple low-engagement signals detected. "
                "Time to have an honest conversation."
            )

        if eff.get("lines_per_commit", 0) < 10 and commit.get("total_commits", 0) > 20:
            weaknesses.append(
                "Average less than 10 lines per commit — "
                "micro-commits that add noise, not value."
            )

        return weaknesses[:8]

    def _generate_suggestions(
        self, commit, habit, eff, style, quality, slacking, dim_scores
    ) -> List[str]:
        """Generate actionable suggestions."""
        suggestions = []

        if dim_scores.get("commit_discipline", 0) < 60:
            suggestions.append(
                "📝 Adopt Conventional Commits format (feat/fix/docs...) "
                "and write messages > 50 chars explaining WHY, not WHAT."
            )

        if dim_scores.get("work_consistency", 0) < 60:
            suggestions.append(
                "⏰ Establish a regular coding routine. "
                "Commit small batches daily instead of large dumps before deadlines."
            )

        if dim_scores.get("efficiency", 0) < 60:
            suggestions.append(
                "🚀 Reduce rework by spending 10 minutes planning before coding. "
                "High churn suggests you're building without a clear picture."
            )

        if dim_scores.get("code_quality", 0) < 60:
            suggestions.append(
                "🔍 Add unit tests for every new feature. "
                "Your bug-fix ratio suggests code ships with too many defects."
            )

        if quality.get("large_commit_ratio", 0) > 0.15:
            suggestions.append(
                "✂️ Break large changes into smaller, reviewable PRs. "
                "Aim for < 200 lines per commit."
            )

        if habit.get("late_night_ratio", 0) > 0.15:
            suggestions.append(
                "🌙 Reduce late-night coding. Sleep-deprived code has 2x the bug rate. "
                "Shift your productive hours earlier."
            )

        if slacking.get("slacking_index", 0) > 50:
            suggestions.append(
                "🐟 Your engagement metrics are below team average. "
                "Set daily micro-goals and commit work-in-progress to stay on track."
            )

        if style.get("issue_reference_ratio", 0) < 0.3:
            suggestions.append(
                "🔗 Reference issue/ticket numbers in every commit. "
                "This is non-negotiable for project traceability."
            )

        if eff.get("ownership_ratio", 0) > 0.8:
            suggestions.append(
                "🤝 Your file ownership is too concentrated. "
                "Pair-program and share knowledge to reduce bus factor risk."
            )

        return suggestions[:6]

    def _generate_verdict(self, score, dim_scores, slacking) -> str:
        """Generate a one-line, no-BS verdict."""
        idx = slacking.get("slacking_index", 50)

        if score >= 85:
            return "⭐ Top-tier contributor. Reliable, disciplined, and productive. Keep it up."
        elif score >= 75:
            return "👍 Solid developer. A few rough edges, but fundamentally strong."
        elif score >= 65:
            return "🙂 Decent contributor with clear areas for improvement. Focus on the weaknesses."
        elif score >= 50:
            if idx > 60:
                return "😐 Mediocre output with notable slacking patterns. Needs a wake-up call."
            return "😐 Average. Not bad, not good. Needs to level up on consistency and quality."
        elif score >= 35:
            return "⚠️ Below expectations. Significant quality and engagement issues need addressing."
        else:
            return "🚨 Serious concerns. This developer needs mentoring, clearer goals, or a frank conversation."

    @staticmethod
    def _letter_grade(score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return "S"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        elif score >= 35:
            return "E"
        else:
            return "F"
