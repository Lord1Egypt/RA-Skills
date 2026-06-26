"""TypeScript stack analyzer with Node-based coupling patterns and cognitive complexity."""

from typing import Dict, List
from ghostclaw.core.node_coupling import NodeImportAnalyzer
from .base import StackAnalyzer
from ghostclaw.lib.complexity import analyze_files_cognitive


class TypeScriptAnalyzer(StackAnalyzer):
    """Analyzes TypeScript projects for architectural issues."""

    def get_extensions(self) -> List[str]:
        # Favor TS but include JS for mixed projects
        return ['.ts', '.tsx', '.js', '.jsx']

    def get_large_file_threshold(self) -> int:
        # TS tends to be more modular; lower threshold
        return 350

    def analyze(self, root: str, files: List[str], metrics: Dict) -> Dict:
        """Run TypeScript-specific architectural checks including import coupling."""
        issues = []
        ghosts = []
        flags = []

        # Leverage standard Node/TS import analyzer
        try:
            analyzer = NodeImportAnalyzer(root)
            coupling_report = analyzer.analyze()

            issues.extend(coupling_report.get('issues', []))
            ghosts.extend(coupling_report.get('architectural_ghosts', []))
            flags.extend(coupling_report.get('red_flags', []))
            coupling_metrics = coupling_report.get('coupling_metrics', {})
        except Exception as e:
            coupling_metrics = {}
            issues.append(f"TS Import analysis failed: {str(e)}")

        # Add cognitive complexity metrics via complexipy (if available)
        cognitive_data = analyze_files_cognitive(files)
        if cognitive_data:
            coupling_metrics.update(cognitive_data)

        return {
            "stack": "typescript",
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": flags,
            "coupling_metrics": coupling_metrics
        }
