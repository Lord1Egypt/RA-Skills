"""Polyglot scoring adapter using the Lizard library."""

import lizard
import lizard_ext.lizardnd
import lizard_ext.lizardns
import logging
from typing import Any, List, Dict
from ghostclaw.core.adapters.base import ScoringAdapter, AdapterMetadata
from ghostclaw.core.adapters.hooks import hookimpl

logger = logging.getLogger(__name__)

class LizardScoringAdapter(ScoringAdapter):
    """
    Computes a vibe score based on code metrics like Cyclomatic Complexity
    and Cognitive Complexity using the Lizard library.
    """

    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="lizard",
            version="0.1.0",
            description="Polyglot metric scoring (CCN, Cognitive Complexity, ND)",
            author="Ghostclaw Team",
            dependencies=["lizard"]
        )

    async def is_available(self) -> bool:
        try:
            import lizard
            return True
        except ImportError:
            return False

    @hookimpl
    def ghost_get_metadata(self) -> Dict[str, Any]:
        """Expose metadata to the plugin manager."""
        meta = self.get_metadata()
        return {
            "name": meta.name,
            "version": meta.version,
            "description": meta.description,
            "available": True
        }

    @hookimpl
    async def ghost_analyze(self, root: str, files: List[str]) -> Dict[str, Any]:
        """Gather metrics and hotspots."""
        data = await self._analyze_internal(files)
        if not data or data["total_functions"] == 0:
            return {}

        issues = []
        if data["max_ccn"] > 20:
            issues.append(f"Lizard: Complex logic hotspot detected (Max CCN: {data['max_ccn']})")
        if data["max_nd"] > 6:
            issues.append(f"Lizard: Deeply nested code hotspot detected (Max ND: {data['max_nd']})")

        return {
            "issues": issues,
            "coupling_metrics": {
                "avg_ccn": round(data["avg_ccn"], 2),
                "avg_nd": round(data["avg_nd"], 2),
                "max_ccn": data["max_ccn"],
                "max_nd": data["max_nd"],
                "total_functions": data["total_functions"]
            }
        }

    @hookimpl
    async def ghost_compute_vibe(self, context: Any) -> float:
        """Hook implementation for vibe computation."""
        # Try to use existing metrics from context if provided by ghost_analyze
        metrics = context.get("coupling_metrics", {})
        if "avg_ccn" in metrics and "avg_nd" in metrics:
            return self._calculate_vibe_from_metrics(metrics)
            
        return await self.compute_vibe(context)

    async def compute_vibe(self, context: Any) -> float:
        """Fallback vibe computation if metrics not yet gathered."""
        files = context.get('files', [])
        data = await self._analyze_internal(files)
        return self._calculate_vibe_from_metrics(data)

    def _calculate_vibe_from_metrics(self, data: Dict) -> float:
        """Internal scoring formula: 30% CCN, 50% ND, 20% LoC."""
        if not data or data.get("total_functions", 0) == 0:
            return 100.0

        avg_ccn = data.get("avg_ccn", 0.0)
        avg_nd = data.get("avg_nd", 0.0)
        avg_nloc = data.get("avg_nloc", 0.0)
        max_ccn = data.get("max_ccn", 0)
        max_nd = data.get("max_nd", 0)

        # 30% CCN (threshold 15)
        ccn_penalty = min(30.0, (avg_ccn / 15.0) * 30.0) if avg_ccn > 5 else 0
        # 50% ND (threshold 5)
        nd_penalty = min(50.0, (avg_nd / 5.0) * 50.0) if avg_nd > 2 else 0
        # 20% LoC (threshold 100)
        loc_penalty = min(20.0, (avg_nloc / 100.0) * 20.0) if avg_nloc > 40 else 0
        
        score = 100.0 - (ccn_penalty + nd_penalty + loc_penalty)
        
        if max_ccn > 25 or max_nd > 8:
            score -= 10.0

        return max(0.0, min(100.0, score))

    async def _analyze_internal(self, files: List[str]) -> Dict[str, Any]:
        """Core Lizard analysis runner."""
        if not files:
            return {}

        total_ccn = 0
        total_nd = 0
        total_ns = 0
        total_nloc = 0
        total_functions = 0
        max_ccn = 0
        max_nd = 0
        
        extensions = lizard.get_extensions([
            lizard_ext.lizardnd.LizardExtension(),
            lizard_ext.lizardns.LizardExtension()
        ])
        analyzer = lizard.FileAnalyzer(extensions)
        
        for file_path in files:
            try:
                analysis = analyzer(file_path)
                for func in analysis.function_list:
                    total_ccn += func.cyclomatic_complexity
                    func_nd = getattr(func, 'max_nesting_depth', 0)
                    func_ns = getattr(func, 'max_nested_structures', 0)
                    
                    total_nd += func_nd
                    total_ns += func_ns
                    total_nloc += func.nloc
                    total_functions += 1
                    
                    if func.cyclomatic_complexity > max_ccn:
                        max_ccn = func.cyclomatic_complexity
                    if func_nd > max_nd:
                        max_nd = func_nd
            except Exception:
                continue

        if total_functions == 0:
            return {"total_functions": 0}

        return {
            "avg_ccn": total_ccn / total_functions,
            "avg_nd": (total_nd + total_ns) / (2 * total_functions),
            "avg_nloc": total_nloc / total_functions,
            "max_ccn": max_ccn,
            "max_nd": max_nd,
            "total_functions": total_functions
        }
