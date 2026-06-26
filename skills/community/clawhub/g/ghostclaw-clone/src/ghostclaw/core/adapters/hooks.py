"""Hook specifications for Ghostclaw plugins using pluggy."""

import pluggy
from typing import List, Dict, Any, Optional

hookspec = pluggy.HookspecMarker("ghostclaw")
hookimpl = pluggy.HookimplMarker("ghostclaw")

class GhostclawPluginSpecs:
    """Specification of hooks that Ghostclaw plugins can implement."""

    @hookspec
    async def ghost_analyze(self, root: str, files: List[str]) -> Dict[str, Any]:
        """
        Run analysis on the codebase.
        
        Returns a dict with 'issues', 'architectural_ghosts', and 'red_flags'.
        """

    @hookspec
    async def ghost_emit(self, event_type: str, data: Any) -> None:
        """Handle an agent lifecycle event."""

    @hookspec
    async def ghost_save_report(self, report: Any) -> Optional[str]:
        """Save an architecture report."""

    @hookspec
    def ghost_get_metadata(self) -> Dict[str, Any]:
        """Return plugin metadata."""

    @hookspec
    async def ghost_compute_vibe(self, context: Any) -> float:
        """Compute the architectural vibe score."""

    @hookspec
    async def ghost_initialize(self, context: Dict[str, Any]) -> None:
        """Initialize plugin with runtime context (config, qmd_store, registry, etc.)."""
