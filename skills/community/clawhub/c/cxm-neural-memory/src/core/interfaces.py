# src/cxm/core/interfaces.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseIntentAnalyzer(ABC):
    @abstractmethod
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """Analyze user prompt and return intent and context needs."""
        pass

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, context_needs: List[str], k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve candidates based on query and needs."""
        pass

class BaseReranker(ABC):
    @abstractmethod
    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_k: int = 5, token_budget: int = 4000) -> List[Dict[str, Any]]:
        """Rerank candidates to fit within budget and maximize relevance."""
        pass

class BaseContextProvider(ABC):
    @abstractmethod
    def gather(self) -> Dict[str, Any]:
        """Gather specific system or project context."""
        pass

class BaseContextEvaluator(ABC):
    @abstractmethod
    def evaluate(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate if a specific context hit is relevant to the query.
        Returns a dict with 'relevant' (bool) and 'reason' (str).
        """
        pass
