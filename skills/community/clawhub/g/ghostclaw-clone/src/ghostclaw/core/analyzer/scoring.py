from typing import Dict, Any, Union, Optional
from ghostclaw.core.score.engine import ScoringEngine as EnhancedEngine, MultiDimensionalScore

class VibeScorer:
    """Orchestrates vibe score calculation, potentially using custom scoring adapters."""

    @staticmethod
    async def compute_score(context: Dict[str, Any], registry=None) -> MultiDimensionalScore:
        """
        Compute the final multi-dimensional vibe score.
        
        Attempts to use a custom ScoringAdapter from the registry first,
        otherwise falls back to the enhanced ScoringEngine.

        Args:
            context: Analysis context with metrics, issues, etc.
            registry: Optional PluginRegistry instance. If None, uses the global registry.
        """
        if registry is None:
            from ghostclaw.core.adapters.registry import registry as global_registry
            registry = global_registry
        
        # 1. Try custom compute from registry (Scoring adapters)
        custom_vibe = await registry.compute_custom_vibe(context=context)
        if custom_vibe is not None:
            # If a custom adapter provides a score, we wrap it in a minimal MultiDimensionalScore
            val = int(custom_vibe)
            return MultiDimensionalScore(
                complexity=val,
                coupling=val,
                cohesion=val,
                naming=val,
                layering=val,
                overall=val,
                confidence=1.0
            )
        
        # 2. Use the enhanced internal engine
        engine = EnhancedEngine()
        return await engine.compute_score(
            metrics=context.get("metrics", {}),
            issues=context.get("issues", []),
            ghosts=context.get("ghosts", []),
            flags=context.get("flags", []),
            stack=context.get("stack", "unknown"),
            coupling_metrics=context.get("coupling_metrics")
        )
