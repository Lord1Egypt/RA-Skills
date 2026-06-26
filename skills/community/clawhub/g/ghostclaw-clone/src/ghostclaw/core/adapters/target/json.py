"""Target adapter for JSON output, perfect for CI/CD pipelines."""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from ghostclaw.core.adapters.base import TargetAdapter, AdapterMetadata
from ghostclaw.core.adapters.hooks import hookimpl


class JsonTargetAdapter(TargetAdapter):
    """Routes agent events and final reports to a JSON file."""

    def __init__(self, output_path: Optional[Path] = None):
        # Default to reports directory with timestamp
        if output_path is None:
            import datetime

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = (
                Path.cwd() / ".ghostclaw" / "reports" / f"report_{timestamp}.json"
            )
        self.output_path = output_path

    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="json_target",
            version="0.1.0",
            description="Standardized JSON output for CI/CD and API consumption.",
            dependencies=[],
        )

    async def is_available(self) -> bool:
        return True

    @hookimpl
    async def ghost_emit(self, event_type: str, data: Any) -> None:
        """Handle agent events. We only care about POST_SYNTHESIS for the full report."""
        if event_type == "POST_SYNTHESIS":
            await self.emit(event_type, data)

    async def emit(self, event_type: str, data: Any) -> None:
        """Implementation of TargetAdapter interface."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        # We save the data (which should be the report dict) to a file
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @hookimpl
    def ghost_get_metadata(self) -> Dict[str, Any]:
        """Expose metadata to the plugin manager."""
        meta = self.get_metadata()
        return {
            "name": meta.name,
            "version": meta.version,
            "description": meta.description,
            "available": True,
        }
