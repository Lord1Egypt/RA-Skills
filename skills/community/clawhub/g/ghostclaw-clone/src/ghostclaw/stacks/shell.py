"""Shell script stack analyzer with cognitive complexity."""

from typing import Dict, List
from .base import StackAnalyzer
from ghostclaw.lib.complexity import analyze_files_cognitive, HAS_COMPLEXIPY


class ShellAnalyzer(StackAnalyzer):
    """Analyzes Shell scripts for architectural issues."""

    def get_extensions(self) -> List[str]:
        return ['.sh', '.bash', '.zsh']

    def get_large_file_threshold(self) -> int:
        return 150

    def analyze(self, root: str, files: List[str], metrics: Dict) -> Dict:
        """Run Shell-specific architectural checks."""
        issues = []
        ghosts = []
        flags = []

        # Cognitive complexity analysis via complexipy (if available)
        cognitive_data = analyze_files_cognitive(files)

        # Build final coupling_metrics with cognitive data plus any existing metrics
        coupling_metrics = {}
        if cognitive_data:
            coupling_metrics.update(cognitive_data)

        # Note: We could also add simple per-line metrics from metrics dict if needed

        return {
            "stack": "shell",
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": flags,
            "coupling_metrics": coupling_metrics
        }
