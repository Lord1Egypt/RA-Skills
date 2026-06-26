"""
Stack detection and analysis logic for Ghostclaw analyzer.
"""

import asyncio
from typing import List, Dict, Any, Optional
from ghostclaw.core.detector import detect_stack
from ghostclaw.stacks import get_analyzer


class StackAnalyzer:
    """Handles stack detection and orchestrating stack-specific analysis."""

    @staticmethod
    async def detect(root: str) -> str:
        """Detect the tech stack of the repository."""
        return await asyncio.to_thread(detect_stack, root)

    @staticmethod
    async def analyze_stack(stack: str, root: str, files: List[str], base_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Perform legacy stack-specific analysis."""
        analyzer = get_analyzer(stack)
        if not analyzer:
            return {
                "issues": ["Standard stack detection failed."],
                "architectural_ghosts": [],
                "red_flags": [],
                "coupling_metrics": {},
                "graph": None
            }

        stack_result = await asyncio.to_thread(analyzer.analyze, root, files, base_metrics)
        
        # Extract graph if available
        if hasattr(analyzer, 'graph'):
            stack_result['import_edges'] = analyzer.graph.edges
        else:
            stack_result['import_edges'] = []
            
        return stack_result

    @staticmethod
    def get_analyzer_instance(stack: str):
        """Get the stack-specific analyzer instance."""
        return get_analyzer(stack)
