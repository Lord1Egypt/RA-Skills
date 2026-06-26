"""Rule engine for directory analysis."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from ...models import (
    AnalysisContext,
    AnalysisResult,
    DirectoryInfo,
    DirectoryType,
    RecommendedAction,
    RiskLevel,
)


@dataclass
class Rule:
    """
    A rule for analyzing directories.

    Each rule has:
    - A match function to determine if it applies
    - Properties defining the analysis result
    """

    name: str
    directory_type: DirectoryType
    risk_level: RiskLevel
    action: RecommendedAction
    reason: str
    confidence: float
    patterns: list[str]  # Directory name patterns to match
    match_func: Callable[[str, DirectoryInfo], bool] | None = None

    def matches(self, directory: DirectoryInfo) -> bool:
        """Check if this rule matches a directory."""
        path = Path(directory.path)
        name = path.name.lower()

        # Pattern matching
        for pattern in self.patterns:
            if pattern.lower() == name:
                return True
            if pattern.startswith("*") and name.endswith(pattern[1:].lower()):
                return True
            if pattern.endswith("*") and name.startswith(pattern[:-1].lower()):
                return True

        # Custom match function
        if self.match_func:
            return self.match_func(name, directory)

        return False

    def to_result(self, directory: DirectoryInfo) -> AnalysisResult:
        """Convert rule to analysis result."""
        return AnalysisResult(
            path=directory.path,
            directory_type=self.directory_type,
            risk_level=self.risk_level,
            recommended_action=self.action,
            reason=self.reason,
            confidence=self.confidence,
        )


class RuleEngine:
    """
    Engine that applies rules to analyze directories.

    Rules are checked in order; first match wins.
    """

    def __init__(self, rules: list[Rule] | None = None):
        """
        Initialize rule engine.

        Args:
            rules: List of rules to use (default: built-in rules)
        """
        from .builtin import BUILTIN_RULES

        self.rules = rules or BUILTIN_RULES

    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the engine."""
        self.rules.insert(0, rule)  # New rules have priority

    def match(
        self,
        directory: DirectoryInfo,
        context: AnalysisContext | None = None,
    ) -> AnalysisResult | None:
        """
        Find matching rule and return analysis result.

        Args:
            directory: Directory to analyze
            context: Analysis context

        Returns:
            AnalysisResult if rule matches, None otherwise
        """
        for rule in self.rules:
            if rule.matches(directory):
                result = rule.to_result(directory)

                # Adjust based on context
                if context:
                    result = self._adjust_result(result, directory, context)

                return result

        return None

    def _adjust_result(
        self,
        result: AnalysisResult,
        directory: DirectoryInfo,
        context: AnalysisContext,
    ) -> AnalysisResult:
        """Adjust result based on context."""
        # If migration is intent and directory is large, suggest move
        if context.intent == "migrate" and context.target_drive:
            if (
                result.recommended_action == RecommendedAction.CAN_DELETE
                and directory.size_mb > 500
            ):
                path = Path(directory.path)
                result.recommended_action = RecommendedAction.CAN_MOVE
                result.target_path = f"{context.target_drive}\\migrated\\{path.name}"
                result.reason = f"{result.reason} (or migrate to {context.target_drive})"

        return result
