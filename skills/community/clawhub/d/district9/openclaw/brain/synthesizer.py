"""Meme concept synthesizer — turns signals into token ideas via LLM."""

from dataclasses import dataclass

from ..config import StrategyConfig
from ..sensing.base import Signal
from ..utils.logger import log
from .llm import LLMClient
from .prompts import SYSTEM_SYNTHESIZER, USER_SYNTHESIZER


@dataclass
class MemeConcept:
    """A generated meme token concept."""
    name: str
    symbol: str
    narrative: str
    logo_prompt: str
    score: float

    def __repr__(self):
        return f"MemeConcept({self.name} [{self.symbol}] score={self.score:.0f})"


class MemeSynthesizer:
    """Generate meme token concepts from real-time signals using LLM."""

    def __init__(self, strategy: StrategyConfig):
        self.strategy = strategy
        self.llm = LLMClient(
            provider=strategy.llm.provider,
            model=strategy.llm.model,
            api_key=strategy.llm.api_key,
            base_url=strategy.llm.base_url,
        )

    def generate(self, signals: list[Signal], count: int = 3) -> list[MemeConcept]:
        """Generate meme concepts from signals."""
        signals_text = "\n".join(
            f"- [{s.source}] {s.keyword} (relevance: {s.score:.0f}/100)\n  {s.context}"
            for s in signals[:10]  # limit to top 10 signals
        )

        system = SYSTEM_SYNTHESIZER.format(user_strategy=self.strategy.prompt)
        user = USER_SYNTHESIZER.format(signals=signals_text, count=count)

        try:
            raw = self.llm.generate_json(system, user, temperature=0.9)
        except Exception as e:
            log.error(f"LLM generation failed: {e}")
            return []

        concepts = []
        items = raw if isinstance(raw, list) else [raw]
        for item in items:
            try:
                concepts.append(MemeConcept(
                    name=item["name"],
                    symbol=item["symbol"].replace("$", ""),
                    narrative=item["narrative"],
                    logo_prompt=item.get("logo_prompt", ""),
                    score=float(item.get("score", 50)),
                ))
            except (KeyError, TypeError) as e:
                log.warning(f"Skipping malformed concept: {e}")

        return concepts
