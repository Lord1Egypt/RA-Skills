"""Metric adapter for pyscn structural analysis."""

import json
from typing import Dict, List, Any, Optional
from ghostclaw.core.adapters.metric.base import AsyncProcessMetricAdapter
from ghostclaw.core.adapters.base import AdapterMetadata
from ghostclaw.core.adapters.hooks import hookimpl

class PySCNAdapter(AsyncProcessMetricAdapter):
    """Wraps pyscn tool into the Ghostclaw adapter interface."""

    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="pyscn",
            version="0.1.0",
            description="Structural clone and dead code detection engine.",
            dependencies=["pyscn"]
        )

    async def is_available(self) -> bool:
        """Check if pyscn binary is in the PATH."""
        result = await self.run_tool(["pyscn", "--version"])
        return result.get("returncode") == 0

    @hookimpl
    async def ghost_analyze(self, root: str, files: List[str]) -> Dict[str, Any]:
        """Perform analysis using pyscn (hook implementation)."""
        return await self.analyze(root, files)

    async def analyze(self, root: str, files: List[str]) -> Dict[str, Any]:
        """Perform analysis using pyscn (ABC implementation)."""
        if not await self.is_available():
            return {}

        # Run pyscn analyze
        result = await self.run_tool(["pyscn", "analyze", root, "--json"])
        if result.get("returncode") != 0:
            stderr = result.get("stderr", "").lower()
            # Known "no files" patterns — treat as empty, not an error
            if any(phrase in stderr for phrase in ["no python files", "no files found", "no matching files"]):
                return {}
            return {"issues": [f"PySCN error: {result.get('stderr')}"]}

        data = self.parse_json(result.get("stdout", "{}"))
        if not data:
            return {}

        # Transform native output to GhostEngine dialect
        issues = []
        ghosts = []

        clones = data.get("clones", [])
        if clones:
            ghosts.append(f"Found {len(clones)} structural clones via PySCN.")

        dead_code = data.get("dead_code", [])
        if dead_code:
            issues.append(f"Detected {len(dead_code)} dead code entries via PySCN.")

        return {
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": []
        }

    @hookimpl
    def ghost_get_metadata(self) -> Dict[str, Any]:
        """Expose metadata to the plugin manager."""
        meta = self.get_metadata()
        return {
            "name": meta.name,
            "version": meta.version,
            "description": meta.description,
            "available": True # Should be checked dynamically in 'plugins list'
        }
