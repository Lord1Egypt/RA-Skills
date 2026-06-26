"""Base sensor and data models for the sensing layer."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Signal:
    """A signal detected from an information source."""
    source: str       # e.g. "crypto", "news", "google_trends"
    keyword: str      # main topic/keyword
    score: float      # relevance score 0-100
    context: str      # additional context description

    def __repr__(self):
        return f"Signal({self.source}: {self.keyword} [{self.score:.0f}])"


class BaseSensor(ABC):
    """Abstract base class for information sensors."""

    name: str = "base"

    @abstractmethod
    def scan(self) -> list[Signal]:
        """Scan the information source and return signals."""
        ...
