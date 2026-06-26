"""Directory analyzer - intelligent analysis and recommendations."""

from pathlib import Path

from ..models import (
    AnalysisContext,
    AnalysisResult,
    DirectoryInfo,
    DirectoryType,
    LinkType,
    RecommendedAction,
    RiskLevel,
)
from .rules import RuleEngine


class DirectoryAnalyzer:
    """
    Analyzes directories and provides intelligent recommendations.

    Uses a combination of:
    - Rule-based matching for known directory patterns
    - Heuristics for unknown directories
    - Context-aware adjustments
    """

    def __init__(self):
        """Initialize analyzer with rule engine."""
        self.rule_engine = RuleEngine()

    def analyze(
        self,
        directory: DirectoryInfo,
        context: AnalysisContext | None = None,
    ) -> AnalysisResult:
        """
        Analyze a single directory.

        Args:
            directory: DirectoryInfo to analyze
            context: Optional analysis context

        Returns:
            AnalysisResult with recommendations
        """
        # Try rule-based matching first
        result = self.rule_engine.match(directory, context)
        if result:
            return result

        # Fall back to heuristic analysis
        return self._heuristic_analyze(directory, context)

    def analyze_batch(
        self,
        directories: list[DirectoryInfo],
        context: AnalysisContext | None = None,
    ) -> list[AnalysisResult]:
        """
        Analyze multiple directories.

        Args:
            directories: List of DirectoryInfo to analyze
            context: Optional analysis context

        Returns:
            List of AnalysisResult
        """
        return [self.analyze(d, context) for d in directories]

    def _heuristic_analyze(
        self,
        directory: DirectoryInfo,
        context: AnalysisContext | None = None,
    ) -> AnalysisResult:
        """
        Analyze directory using heuristics when no rule matches.

        Considers:
        - Directory name patterns
        - File type distribution
        - Size
        - Link status
        """
        path = Path(directory.path)
        name = path.name.lower()
        parent = path.parent.name.lower() if path.parent else ""

        # Default values
        dir_type = DirectoryType.UNKNOWN
        risk = RiskLevel.MEDIUM
        action = RecommendedAction.REVIEW
        reason = "Unknown directory type - requires manual review"
        confidence = 0.3

        # Check if already a link (already migrated)
        if directory.link_type != LinkType.NORMAL:
            target_info = f" -> {directory.link_target}" if directory.link_target else ""
            return AnalysisResult(
                path=directory.path,
                directory_type=DirectoryType.MIGRATED,
                risk_level=RiskLevel.SAFE,
                recommended_action=RecommendedAction.KEEP,
                reason=f"[MIGRATED] {directory.link_type.value}{target_info}",
                confidence=0.95,
                target_path=directory.link_target,
            )

        # Heuristic: cache-like names
        cache_patterns = ["cache", "tmp", "temp", ".cache", "_cache"]
        if any(p in name for p in cache_patterns):
            dir_type = DirectoryType.CACHE
            risk = RiskLevel.LOW
            action = RecommendedAction.CAN_DELETE
            reason = "Appears to be a cache directory based on name"
            confidence = 0.6

        # Heuristic: log files
        elif "log" in name or name.endswith(".log"):
            dir_type = DirectoryType.LOG
            risk = RiskLevel.LOW
            action = RecommendedAction.CAN_DELETE
            reason = "Appears to be a log directory"
            confidence = 0.6

        # Heuristic: config directories
        elif name.startswith(".") or "config" in name:
            dir_type = DirectoryType.CONFIG
            risk = RiskLevel.HIGH
            action = RecommendedAction.KEEP
            reason = "Appears to be a configuration directory"
            confidence = 0.5

        # Heuristic: build outputs
        build_patterns = ["build", "dist", "out", "target", ".output"]
        if any(p in name for p in build_patterns):
            dir_type = DirectoryType.BUILD
            risk = RiskLevel.LOW
            action = RecommendedAction.CAN_DELETE
            reason = "Appears to be a build output directory"
            confidence = 0.65

        # Heuristic: project directories
        if "project" in name or "code" in name or "src" in parent:
            dir_type = DirectoryType.PROJECT
            risk = RiskLevel.HIGH
            action = RecommendedAction.KEEP
            reason = "Appears to be a project directory"
            confidence = 0.5

        # Adjust based on context
        if context:
            result = self._adjust_for_context(
                directory, dir_type, risk, action, reason, confidence, context
            )
            dir_type, risk, action, reason, confidence = result

        return AnalysisResult(
            path=directory.path,
            directory_type=dir_type,
            risk_level=risk,
            recommended_action=action,
            reason=reason,
            confidence=confidence,
        )

    def _adjust_for_context(
        self,
        directory: DirectoryInfo,
        dir_type: DirectoryType,
        risk: RiskLevel,
        action: RecommendedAction,
        reason: str,
        confidence: float,
        context: AnalysisContext,
    ) -> tuple[DirectoryType, RiskLevel, RecommendedAction, str, float]:
        """Adjust analysis based on user context."""
        path = Path(directory.path)
        name = path.name.lower()

        # Developer context
        if context.user_type == "developer" or context.project_type:
            # Keep development-related directories
            dev_patterns = {
                "python": [
                    ".venv",
                    "venv",
                    ".conda",
                    "__pycache__",
                    ".pytest_cache",
                    "site-packages",
                ],
                "node": ["node_modules", ".npm", "dist", "build"],
                "rust": ["target", "cargo"],
                "go": ["pkg", "bin"],
            }

            if context.project_type:
                patterns = dev_patterns.get(context.project_type, [])
                if any(p in name for p in patterns):
                    if dir_type == DirectoryType.CACHE or dir_type == DirectoryType.DEPENDENCY:
                        # Can be regenerated, safe to clean
                        return (
                            dir_type,
                            RiskLevel.LOW,
                            RecommendedAction.CAN_DELETE,
                            reason,
                            confidence + 0.1,
                        )
                    elif dir_type == DirectoryType.UNKNOWN:
                        return (
                            DirectoryType.DEPENDENCY,
                            RiskLevel.LOW,
                            RecommendedAction.CAN_DELETE,
                            f"Development dependency for {context.project_type}",
                            0.7,
                        )

        # Cleanup intent
        if context.intent == "cleanup":
            # Be more aggressive about cleaning
            if dir_type == DirectoryType.CACHE and risk == RiskLevel.LOW:
                return dir_type, risk, RecommendedAction.CAN_DELETE, reason, confidence + 0.1

        # Migration intent
        if context.intent == "migrate" and context.target_drive:
            # Suggest migration for large directories
            if directory.size_mb > 500 and action == RecommendedAction.KEEP:
                return (
                    dir_type,
                    RiskLevel.MEDIUM,
                    RecommendedAction.CAN_MOVE,
                    f"Large directory suitable for migration to {context.target_drive}",
                    0.6,
                )

        return dir_type, risk, action, reason, confidence
