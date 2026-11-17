"""Style pack loader: v3 Style Contract v2.0 → resolved values.

Loads complete v3 style contracts with all tokens: colors, typography, grid,
spacing, card_tokens, table_tokens, chart_tokens, diagram_tokens, etc.
Backward compatible with v4.0 simplified packs (auto-detected by schema_version).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

EMU_PER_PT = 12700
EMU_PER_IN = 914400

DEFAULT_PACK = Path(__file__).resolve().parents[1] / "styles/editorial-knowledge.json"


@dataclass
class ResolvedStyle:
    """Resolved style contract with all v3 tokens accessible."""
    pack_id: str
    schema_version: str
    display_name: str

    # Core tokens (v3)
    colors: dict
    typography: dict
    grid: dict
    spacing: dict
    shape_tokens: dict
    shadow_tokens: dict

    # Component tokens (v3)
    card_tokens: dict
    table_tokens: dict
    chart_tokens: dict
    diagram_tokens: dict
    image_tokens: dict
    icon_tokens: dict
    footer_tokens: dict

    # Density and effects
    density_limits: dict
    allowed_effects: list
    forbidden_drift: list

    # v4 knobs (if present)
    density: str = "regular"
    margin_scale: float = 1.0
    alignment: str = "left"

    # Raw pack for advanced access
    raw: dict = field(default_factory=dict)

    def color(self, token: str, fallback: str = "#000000") -> str:
        """Resolve color token to hex value."""
        return self.colors.get(token, fallback)

    def color_with_opacity(self, token: str, opacity: float, fallback: str = "#000000") -> str:
        """Resolve color with opacity (for MSO RGB format)."""
        hex_color = self.color(token, fallback)
        # Return hex + opacity (builder will convert to MSO format)
        return hex_color

    def font(self, kind: str = "primary") -> str:
        """Get first font from stack."""
        key = f"font_{kind}"
        stack = self.typography.get(key) or self.typography.get("font_primary") or ["Calibri"]
        return stack[0] if isinstance(stack, list) else str(stack)

    def font_stack(self, kind: str = "primary") -> list[str]:
        """Get full font fallback stack."""
        key = f"font_{kind}"
        stack = self.typography.get(key) or self.typography.get("font_primary") or ["Calibri"]
        return stack if isinstance(stack, list) else [str(stack)]

    def size_cpt(self, group: str, level: str) -> int:
        """Get font size in centipoints (1/100 pt)."""
        table = self.typography.get(f"{group}_sizes_pt") or {}
        value = table.get(level)
        if value is None:
            # Fallback
            value = {"title": 22, "body": 13, "metric": 22}.get(group.split("_")[0], 13)
        return int(round(float(value) * 100))

    def body_levels_cpt(self) -> list[int]:
        """Descending body sizes for deterministic step-down (D9)."""
        table = self.typography.get("body_sizes_pt") or {}
        levels = [table.get(k) for k in ("large", "normal", "small", "footnote") if table.get(k)]
        return [int(round(float(v) * 100)) for v in levels] or [1300]

    def gap_emu(self, ref: str = "md") -> int:
        """Get spacing gap in EMU from spacing scale."""
        scale = self.spacing.get("scale", {})
        inches = scale.get(ref, 0.16)
        return int(round(inches * EMU_PER_IN))

    def margin_emu(self, side: str = "left") -> int:
        """Get grid margin in EMU."""
        key = f"margin_{side}_in"
        inches = self.grid.get(key, 0.55)
        return int(round(inches * EMU_PER_IN * self.margin_scale))

    def weight(self, name: str, default: int = 400) -> int:
        """Get font weight."""
        return int((self.typography.get("weights") or {}).get(name, default))

    def card_style(self, variant: str = "default") -> dict:
        """Get card token set (fill, border, padding, etc.)."""
        return self.card_tokens.get(variant, self.card_tokens.get("default", {}))

    def table_style(self, variant: str = "default") -> dict:
        """Get table token set."""
        return self.table_tokens.get(variant, self.table_tokens.get("default", {}))

    def chart_style(self) -> dict:
        """Get chart tokens."""
        return self.chart_tokens

    def diagram_style(self) -> dict:
        """Get diagram tokens."""
        return self.diagram_tokens

    def resolve_color_ref(self, ref: str) -> str:
        """Resolve a color reference (token name or hex)."""
        if ref.startswith("#"):
            return ref
        return self.color(ref)


def load_style_pack(path: str | Path | None = None) -> ResolvedStyle:
    """Load style pack with auto-detection of v3 (v2.0) vs v4 (v4.0) format."""
    pack = json.loads(Path(path or DEFAULT_PACK).read_text(encoding="utf-8"))
    schema_ver = pack.get("schema_version", "2.0")

    if schema_ver == "2.0":
        # v3 complete style contract
        return ResolvedStyle(
            pack_id=pack["style_id"],
            schema_version=schema_ver,
            display_name=pack["display_name"],
            colors=pack["colors"],
            typography=pack["typography"],
            grid=pack["grid"],
            spacing=pack["spacing"],
            shape_tokens=pack["shape_tokens"],
            shadow_tokens=pack["shadow_tokens"],
            card_tokens=pack["card_tokens"],
            table_tokens=pack["table_tokens"],
            chart_tokens=pack["chart_tokens"],
            diagram_tokens=pack["diagram_tokens"],
            image_tokens=pack["image_tokens"],
            icon_tokens=pack["icon_tokens"],
            footer_tokens=pack["footer_tokens"],
            density_limits=pack["density_limits"],
            allowed_effects=pack["allowed_effects"],
            forbidden_drift=pack["forbidden_drift"],
            density="regular",
            margin_scale=1.0,
            alignment="left",
            raw=pack,
        )
    else:
        # v4.0 simplified format (backward compat)
        tokens = pack.get("tokens", {})
        knobs = pack.get("layout_knobs", {})
        # Fill missing v3 tokens with defaults
        return ResolvedStyle(
            pack_id=pack.get("pack", {}).get("pack_id", "unknown"),
            schema_version=schema_ver,
            display_name=pack.get("pack", {}).get("display_name", "Unknown"),
            colors=tokens.get("colors", {}),
            typography=tokens.get("typography", {}),
            grid={"columns": 12, "rows": 8, "margin_left_in": 0.55, "margin_right_in": 0.55,
                  "margin_top_in": 0.38, "margin_bottom_in": 0.35, "gutter_horizontal_in": 0.14,
                  "gutter_vertical_in": 0.12, "title_zone_height_in": 0.72, "footer_zone_height_in": 0.24,
                  "safe_zone_in": {"left": 0.08, "right": 0.08, "top": 0.06, "bottom": 0.06}},
            spacing={"unit": "in", "scale": {"xs": 0.06, "sm": 0.1, "md": 0.16, "lg": 0.24, "xl": 0.36},
                     "rules": {}},
            shape_tokens=tokens.get("shape", {}),
            shadow_tokens={},
            card_tokens={},
            table_tokens={},
            chart_tokens=tokens.get("chart", {}),
            diagram_tokens={},
            image_tokens={},
            icon_tokens={},
            footer_tokens={},
            density_limits={},
            allowed_effects=[],
            forbidden_drift=[],
            density=knobs.get("density", "regular"),
            margin_scale=float(knobs.get("margin_scale", 1.0)),
            alignment=knobs.get("alignment", "left"),
            raw=pack,
        )
