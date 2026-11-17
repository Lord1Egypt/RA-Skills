"""Authoring-time style pack QA (D8): structural schema check plus the
perceptual checks a JSON Schema cannot express. Runs when a pack is
created or edited — a bad palette is rejected before it ever renders,
not discovered per-deck.

Errors block the pack; warnings advise. All findings machine-readable.

Perceptual rules:
  CONTRAST_* : WCAG-style contrast floors for the token pairs the engine
               actually composes (body text on background and surfaces,
               secondary text, titles, KPI values on cards).
  NO_CJK_FALLBACK : font_primary has no known CJK-capable family — CJK
               decks would render via uncontrolled OS substitution.
  DATA_SERIES_FAINT : a chart series nearly invisible on the background.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .qa_plan import contrast_ratio

_ROOT = Path(__file__).resolve().parents[1]

# (foreground token, background token, floor, severity)
CONTRAST_RULES = [
    ("text_primary", "background", 4.5, "error"),
    ("text_primary", "surface_1", 4.5, "error"),
    ("text_primary", "surface_2", 4.0, "error"),
    ("text_secondary", "background", 3.0, "error"),
    ("text_secondary", "surface_1", 2.6, "warning"),
    ("primary", "background", 3.0, "error"),
    ("accent", "background", 2.2, "warning"),
    ("negative", "background", 2.6, "warning"),
    ("positive", "background", 2.6, "warning"),
]

CJK_FAMILY_HINTS = ("pingfang", "noto sans cjk", "noto serif cjk", "source han",
                    "microsoft yahei", "songti", "simsun", "simhei", "hiragino",
                    "wenquanyi", "sarasa", "dengxian")


def _finding(code: str, severity: str, message: str, **extra) -> dict:
    return {"code": code, "severity": severity, "message": message, **extra}


def validate_style_pack(pack: dict) -> dict:
    findings: list[dict] = []

    # Detect schema version and pick appropriate schema
    schema_version = pack.get("schema_version", "2.0")

    scripts_dir = str(_ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import validate_contracts  # noqa: PLC0415

    if schema_version == "2.0":
        # v3 style contract (complete)
        schema_path = _ROOT / "schemas/v4/style-contract-v3.schema.json"
    else:
        # v4.0 style contract (simplified)
        schema_path = _ROOT / "schemas/v4/style-contract-v4.schema.json"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    for error in validate_contracts.validate_schema_subset(
            pack, schema, Path("style-pack"), True):
        findings.append(_finding("SCHEMA_" + error["code"], "error",
                                 f"{error['pointer']}: {error['repair_suggestion']}"))
    if any(f["severity"] == "error" for f in findings):
        return {"status": "fail", "findings": findings}

    # Access colors from appropriate location
    if schema_version == "2.0":
        colors = pack.get("colors", {})
        typo = pack.get("typography", {})
    else:
        colors = pack.get("tokens", {}).get("colors", {})
        typo = pack.get("tokens", {}).get("typography", {})
    for fg, bg, floor, severity in CONTRAST_RULES:
        if fg in colors and bg in colors:
            ratio = contrast_ratio(colors[fg], colors[bg])
            if ratio < floor:
                findings.append(_finding(
                    f"CONTRAST_{fg.upper()}_ON_{bg.upper()}", severity,
                    f"{colors[fg]} on {colors[bg]} is {ratio:.2f}, floor {floor}",
                    ratio=round(ratio, 2), floor=floor))

    # KPI contrast check (different paths for v2.0 vs v4.0)
    if schema_version == "2.0":
        # v3: check card_tokens.metric
        kpi_token = pack.get("card_tokens", {}).get("metric", {}).get("number_color", "primary")
        card_token = pack.get("card_tokens", {}).get("metric", {}).get("fill", "background")
    else:
        # v4: check skins
        kpi_token = (pack.get("skins", {}).get("kpi") or {}).get("value_color", "primary")
        card_token = (pack.get("skins", {}).get("card") or {}).get("fill", "surface_1")

    # Resolve token to actual color
    kpi_color = colors.get(kpi_token, kpi_token) if not kpi_token.startswith("#") else kpi_token
    card_color = colors.get(card_token, card_token) if not card_token.startswith("#") else card_token
    if kpi_color.startswith("#") and card_color.startswith("#"):
        ratio = contrast_ratio(kpi_color, card_color)
        if ratio < 3.0:
            findings.append(_finding("CONTRAST_KPI_ON_CARD", "error",
                                     f"kpi value {ratio:.2f} on card fill, floor 3.0",
                                     ratio=round(ratio, 2), floor=3.0))

    stack = " ".join(typo.get("font_primary", [])).lower()
    if not any(hint in stack for hint in CJK_FAMILY_HINTS):
        findings.append(_finding(
            "NO_CJK_FALLBACK", "warning",
            "font_primary declares no known CJK-capable family; CJK text will "
            "render via uncontrolled OS substitution"))

    for idx, series in enumerate(colors.get("data_series", [])):
        ratio = contrast_ratio(series, colors["background"])
        if ratio < 1.6:
            findings.append(_finding("DATA_SERIES_FAINT", "warning",
                                     f"data_series[{idx}] {series} is {ratio:.2f} "
                                     f"against background", index=idx))

    status = "fail" if any(f["severity"] == "error" for f in findings) else \
        ("warn" if findings else "pass")
    return {"status": status, "findings": findings}
