"""Mock storage adapter for testing Ghostclaw without disk I/O."""

from typing import List, Any, Dict, Optional
from ghostclaw.core.adapters.base import StorageAdapter, AdapterMetadata
from ghostclaw.core.adapters.hooks import hookimpl

class MockStorageAdapter(StorageAdapter):
    """In-memory storage for vibe reports. No persistence."""

    def __init__(self):
        self.reports: List[Dict[str, Any]] = []
        self._initialized = True

    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="mock-storage",
            version="0.1.0",
            description="In-memory storage for unit testing."
        )

    async def is_available(self) -> bool:
        return True

    @hookimpl
    async def ghost_save_report(self, report: Any) -> Optional[str]:
        """Hook implementation for saving report."""
        return await self.save_report(report)

    async def save_report(self, report: Any) -> str:
        """Store report in memory."""
        if hasattr(report, "model_dump"):
            data = report.model_dump()
        else:
            data = report
        
        report_id = str(len(self.reports) + 1)
        data["id"] = report_id
        self.reports.append(data)
        return report_id

    async def get_history(self, limit: int = 10) -> List[Any]:
        """Retrieve recent reports from memory."""
        return self.reports[-limit:][::-1]

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
