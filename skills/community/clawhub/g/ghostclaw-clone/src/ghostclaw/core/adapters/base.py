"""Base adapter interfaces for Ghostclaw's plugin system."""

import abc
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

class AdapterMetadata(BaseModel):
    """Metadata for an adapter."""
    name: str
    version: str
    description: str
    author: Optional[str] = None
    dependencies: List[str] = []  # External binaries required
    min_ghostclaw_version: Optional[str] = None
    max_ghostclaw_version: Optional[str] = None
    supports_per_file_cache: bool = False  # Whether adapter outputs can be split per file safely

class BaseAdapter(abc.ABC):
    """Abstract base class for all Ghostclaw adapters."""

    @abc.abstractmethod
    def get_metadata(self) -> AdapterMetadata:
        """Return metadata about the adapter."""
        pass

    @abc.abstractmethod
    async def is_available(self) -> bool:
        """Check if the adapter's external dependencies are available."""
        pass

class MetricAdapter(BaseAdapter):
    """Adapter for external analysis tools (pyscn, sonar, eslint)."""

    @abc.abstractmethod
    async def analyze(self, root: str, files: List[str]) -> Dict[str, Any]:
        """
        Run analysis on the given files and return discovered issues/ghosts.
        
        Returns:
            Dict containing 'issues', 'architectural_ghosts', and 'red_flags'.
        """
        pass

class TargetAdapter(BaseAdapter):
    """Adapter for output routing (CLI, Markdown file, JSON-API)."""

    @abc.abstractmethod
    async def emit(self, event_type: str, data: Any) -> None:
        """Handle an agent lifecycle event."""
        pass

class StorageAdapter(BaseAdapter):
    """Adapter for vibe history persistence (JSON/SQLite)."""

    @abc.abstractmethod
    async def save_report(self, report_phi: Any) -> str:
        """Save a report and return its unique identifier."""
        pass

    @abc.abstractmethod
    async def get_history(self, limit: int = 10) -> List[Any]:
        """Retrieve recent reports."""
        pass

class ScoringAdapter(BaseAdapter):
    """Adapter for custom vibe score calculation algorithms (e.g., CodeBERTScore)."""

    @abc.abstractmethod
    async def compute_vibe(self, context: Any) -> float:
        """
        Calculate a vibe score based on the provided analysis context.

        Returns:
            A float representing the vibe score (0-100).
        """
        pass
