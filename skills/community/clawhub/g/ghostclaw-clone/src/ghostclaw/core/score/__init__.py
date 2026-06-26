from typing import Dict, Any, List
from .engine import ScoringEngine as EnhancedEngine, MultiDimensionalScore

class ScoringEngine:
    """
    Core mathematical engine for calculating architectural vibe scores.
    Bridge to the enhanced multi-dimensional engine (v0.2.2a0).
    """

    @staticmethod
    def compute_vibe_score(metrics: Dict, issue_count: int, ghost_count: int) -> int:
        """
        Calculate the final vibe score (0-100).
        Legacy method for backward compatibility.
        """
        # Create a minimal context for the enhanced engine
        engine = EnhancedEngine()

        # Determine stack (fallback to unknown if not in metrics)
        stack = metrics.get("stack", "unknown")

        # Mock issues and ghosts as empty lists for this legacy call
        mock_issues = ["Issue" for _ in range(issue_count)]
        mock_ghosts = ["Ghost" for _ in range(ghost_count)]

        # Check for running loop
        import asyncio
        has_running_loop = False
        try:
            asyncio.get_running_loop()
            has_running_loop = True
        except RuntimeError:
            has_running_loop = False

        if not has_running_loop:
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(engine.compute_score(
                    metrics=metrics,
                    issues=mock_issues,
                    ghosts=mock_ghosts,
                    flags=[],
                    stack=stack
                ))
                return result.overall
            except Exception:
                pass
            finally:
                loop.close()

        # Fallback formula
        score = 100
        large_file_penalty = min(30, metrics.get('large_file_count', 0) * 5)
        score -= large_file_penalty
        avg = metrics.get('average_lines', 0)
        if avg > 200:
            score -= 10
        score -= min(20, issue_count * 3)
        score -= min(15, ghost_count * 5)
        return max(0, min(100, score))


__all__ = ["ScoringEngine", "MultiDimensionalScore"]
