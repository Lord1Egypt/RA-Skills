from __future__ import annotations

from pathlib import Path
from shutil import which
from typing import Any

from .base import BuildInspection, BuildPlan, BuildResult, BuilderCapability, SupportLevel


class OfficeCliAdapter:
    name = "officecli"

    def probe(self) -> BuilderCapability:
        command = which("officecli")
        return BuilderCapability(
            name=self.name,
            available=False,
            version=None,
            command=command,
            features={
                "native_text": "unknown",
                "native_table": "unknown",
                "native_chart": "unknown",
                "native_connector": "unknown",
                "svg_embed": "unknown",
                "speaker_notes": "unknown",
                "theme": "unknown",
                "slide_master": "unknown",
                "readback": "unknown",
            },
            warnings=["OfficeCLI is not marked available until a project-specific smoke test is configured."],
        )

    def supports(self, component_type: str, delivery_route: str) -> SupportLevel:
        return "unknown"

    def plan(self, ppt_ir: dict[str, Any], style_contract: dict[str, Any], delivery_plan: dict[str, Any]) -> BuildPlan:
        return BuildPlan(builder=self.name, unsupported_objects=[], warnings=["OfficeCLI adapter is a contract stub."])

    def build(self, build_plan: BuildPlan, output_dir: Path) -> BuildResult:
        return BuildResult(builder=self.name, status="failed", errors=["BUILDER_RUNTIME_NOT_IMPLEMENTED"])

    def inspect_output(self, pptx_path: Path) -> BuildInspection:
        return BuildInspection(builder=self.name, status="not_run")
