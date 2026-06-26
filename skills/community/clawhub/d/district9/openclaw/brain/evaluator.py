"""Meme concept evaluator — scores and selects the best concept."""

from ..config import StrategyConfig
from ..utils.logger import log
from .llm import LLMClient
from .prompts import SYSTEM_EVALUATOR, USER_EVALUATOR
from .synthesizer import MemeConcept


class MemeEvaluator:
    """Evaluate and select the best meme concept using LLM."""

    def __init__(self, strategy: StrategyConfig):
        self.strategy = strategy
        self.llm = LLMClient(
            provider=strategy.llm.provider,
            model=strategy.llm.model,
            api_key=strategy.llm.api_key,
            base_url=strategy.llm.base_url,
        )

    def select_best(self, concepts: list[MemeConcept], min_score: float = 50) -> MemeConcept | None:
        """Evaluate concepts and return the best one above min_score."""
        if not concepts:
            return None

        scored = []
        for concept in concepts:
            score = self._evaluate(concept)
            if score is not None:
                concept.score = score
            scored.append(concept)

        # Sort by score descending
        scored.sort(key=lambda c: c.score, reverse=True)

        best = scored[0]
        if best.score < min_score:
            log.info(f"Best concept scored {best.score:.0f} (below threshold {min_score})")
            return None

        return best

    def _evaluate(self, concept: MemeConcept) -> float | None:
        """Evaluate a single concept using LLM. Returns score 0-100."""
        user = USER_EVALUATOR.format(
            name=concept.name,
            symbol=concept.symbol,
            narrative=concept.narrative,
        )

        try:
            result = self.llm.generate_json(SYSTEM_EVALUATOR, user, temperature=0.3)
            return float(result.get("final_score", concept.score))
        except Exception as e:
            log.warning(f"Evaluation failed for {concept.name}: {e}")
            return None
