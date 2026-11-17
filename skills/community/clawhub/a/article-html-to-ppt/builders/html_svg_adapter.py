from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import BuildInspection, BuildPlan, BuildResult, BuilderCapability, SupportLevel


class HtmlSvgAdapter:
    name = "html_svg"

    def probe(self) -> BuilderCapability:
        return BuilderCapability(
            name=self.name,
            available=True,
            version="stdlib-svg",
            command="python",
            features={
                "native_text": False,
                "native_table": False,
                "native_chart": False,
                "native_connector": False,
                "svg_embed": True,
                "speaker_notes": False,
                "theme": False,
                "slide_master": False,
                "readback": False,
            },
            warnings=["HTML/SVG adapter is visual-only and must not satisfy native-required objects."],
        )

    def supports(self, component_type: str, delivery_route: str) -> SupportLevel:
        if delivery_route in {"svg_component", "generated_image", "background_image", "hybrid_overlay"}:
            return "visual_only"
        return "unsupported"

    def plan(self, ppt_ir: dict[str, Any], style_contract: dict[str, Any], delivery_plan: dict[str, Any]) -> BuildPlan:
        return BuildPlan(builder=self.name, slides=delivery_plan.get("slides", []) or [])

    def build(self, build_plan: BuildPlan, output_dir: Path) -> BuildResult:
        return BuildResult(builder=self.name, status="failed", errors=["BUILDER_RUNTIME_NOT_IMPLEMENTED"])

    def inspect_output(self, pptx_path: Path) -> BuildInspection:
        return BuildInspection(builder=self.name, status="not_run")
