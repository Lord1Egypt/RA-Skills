#!/usr/bin/env python3
"""Compose a decoration onto a blank product photo.

The sizing model is ratio-based against the *detected garment bounding
box*, not absolute pixels or inches. That way the same placement rule
produces a visually identical mockup for a youth tee and an adult tee
even when the source images are at different resolutions / crops /
zoom levels.

Pipeline:
    1. Detect the garment bbox in the blank (rembg → alpha → tight bbox,
       falling back to the full image if rembg finds nothing).
    2. Look up ``placement_rules.json[category][placement]`` (or
       ``_defaults[placement]``) → ``{width_ratio, x_center_ratio,
       y_top_ratio, rotation_deg}``.
    3. Apply user-supplied deltas on top (``--width-delta-pct``,
       ``--offset-x-pct``, ``--offset-y-pct``, ``--rotate-deg``).
    4. Optionally strip the decoration background (rembg) when
       ``--auto-remove-bg`` is passed and the input has no alpha.
    5. Scale the decoration (aspect-locked), rotate with expand=True, and
       alpha-composite onto the blank.
    6. Write the PNG and emit a JSON receipt to stdout so the caller can
       diff between iterations.

No generative model is ever invoked.

Paths: the placement-rules catalog and output directory default to the
skill data dir (``$MOCKUP_DATA_DIR`` or ``~/.drivethru/mockup``), falling
back to the catalog bundled with the skill. Override with ``--rules`` /
``--output``.

Usage:
    python3 scripts/compose_mockup.py \
        --blank /tmp/hoodie.jpg \
        --decoration /tmp/logo.png \
        --category hoodie --placement full_front \
        [--auto-remove-bg] \
        [--width-delta-pct 0] [--offset-x-pct 0] [--offset-y-pct 0] \
        [--rotate-deg 0] \
        [--output /path/to/out.png]
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _paths  # noqa: E402


_DEFAULTS_KEY = "_defaults"


def _load_rules(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(
            f"ERROR: rules file not found at {path}. Point --rules at a valid "
            "placement_rules.json or create one with edit_placement_rule.py."
        )
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: rules file at {path} is not valid JSON: {e}")


def _resolve_rule(rules: dict, category: str | None, placement: str) -> tuple[dict, str]:
    """Return ``(rule, resolved_category)``. Falls back to ``_defaults``."""
    for candidate in (category, _DEFAULTS_KEY):
        if not candidate:
            continue
        bucket = rules.get(candidate)
        if isinstance(bucket, dict) and placement in bucket:
            return bucket[placement], candidate
    raise SystemExit(
        f"ERROR: no rule for placement='{placement}' under category="
        f"'{category}' or '{_DEFAULTS_KEY}'. Add one with edit_placement_rule.py."
    )


def _detect_bbox(blank_path: Path) -> dict:
    # Import inside the function so a missing rembg only breaks --auto paths.
    from detect_garment_bbox import detect_bbox  # type: ignore

    return detect_bbox(blank_path)


def _prepare_decoration(decoration_path: Path, auto_remove_bg: bool):
    from PIL import Image

    img = Image.open(decoration_path).convert("RGBA")
    if not auto_remove_bg:
        return img, False

    alpha = img.getchannel("A")
    if alpha.getextrema()[0] < 255:
        # Already has transparency — leave it alone.
        return img, False

    from rembg import new_session, remove

    session = new_session("u2net")
    with decoration_path.open("rb") as f:
        data = f.read()
    cut = remove(data, session=session)
    import io
    return Image.open(io.BytesIO(cut)).convert("RGBA"), True


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def compose(
    *,
    blank_path: Path,
    decoration_path: Path,
    category: str | None,
    placement: str,
    rules_path: Path,
    output_path: Path,
    auto_remove_bg: bool,
    width_delta_pct: float,
    offset_x_pct: float,
    offset_y_pct: float,
    rotate_deg_override: float | None,
) -> dict:
    from PIL import Image

    rules = _load_rules(rules_path)
    rule, resolved_category = _resolve_rule(rules, category, placement)

    bbox = _detect_bbox(blank_path)
    bb_w = max(1, bbox["width"])
    bb_h = max(1, bbox["height"])

    # Effective ratios after deltas.
    width_ratio = _clamp(rule["width_ratio"] * (1 + width_delta_pct / 100.0), 0.01, 1.5)
    x_center_ratio = _clamp(rule["x_center_ratio"] + offset_x_pct / 100.0, 0.0, 1.0)
    y_top_ratio = _clamp(rule["y_top_ratio"] + offset_y_pct / 100.0, 0.0, 1.0)
    rotation_deg = (
        rotate_deg_override
        if rotate_deg_override is not None
        else float(rule.get("rotation_deg", 0))
    )

    decoration, bg_removed = _prepare_decoration(decoration_path, auto_remove_bg)
    src_w, src_h = decoration.size
    if src_w == 0 or src_h == 0:
        raise SystemExit("ERROR: decoration image has zero-sized dimension")

    target_w = max(1, int(round(bb_w * width_ratio)))
    target_h = max(1, int(round(target_w * (src_h / src_w))))
    scaled = decoration.resize((target_w, target_h), Image.BICUBIC)

    # Rotate around center; expand so corners aren't clipped.
    rotated = scaled.rotate(-rotation_deg, resample=Image.BICUBIC, expand=True)
    rot_w, rot_h = rotated.size

    # Position: x_center_ratio / y_top_ratio are relative to the bbox, so
    # translate back to absolute pixel coordinates on the blank canvas.
    anchor_x = bbox["left"] + int(round(bb_w * x_center_ratio))
    anchor_y = bbox["top"] + int(round(bb_h * y_top_ratio))
    paste_x = anchor_x - rot_w // 2
    paste_y = anchor_y

    blank = Image.open(blank_path).convert("RGBA")
    canvas = blank.copy()
    canvas.alpha_composite(rotated, dest=(paste_x, paste_y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG")

    return {
        "output": str(output_path),
        "blank": str(blank_path),
        "decoration": str(decoration_path),
        "category_requested": category,
        "category_resolved": resolved_category,
        "placement": placement,
        "garment_bbox": bbox,
        "rule": rule,
        "applied": {
            "width_ratio": width_ratio,
            "x_center_ratio": x_center_ratio,
            "y_top_ratio": y_top_ratio,
            "rotation_deg": rotation_deg,
            "width_delta_pct": width_delta_pct,
            "offset_x_pct": offset_x_pct,
            "offset_y_pct": offset_y_pct,
        },
        "decoration_size_px": [rot_w, rot_h],
        "paste_top_left_px": [paste_x, paste_y],
        "background_removed": bg_removed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose a decoration onto a blank product photo")
    parser.add_argument("--blank", required=True, help="Path to the blank product image")
    parser.add_argument("--decoration", required=True, help="Path to the decoration image")
    parser.add_argument("--category", default=None, help="Garment category (hoodie, tee, hat, mug, ...)")
    parser.add_argument("--placement", default="full_front", help="Placement name (full_front, left_chest, ...)")
    parser.add_argument(
        "--rules",
        default=None,
        help="Path to placement_rules.json (default: editable copy in the data dir, "
        "else the catalog bundled with the skill)",
    )
    parser.add_argument("--output", default=None, help="Output PNG path (default: <data dir>/out/<uuid>.png)")
    parser.add_argument(
        "--auto-remove-bg",
        action="store_true",
        help="Run rembg on the decoration first if it has no alpha",
    )
    parser.add_argument(
        "--width-delta-pct",
        type=float,
        default=0.0,
        help="Adjust rule width_ratio by this percent (+10 = 10%% wider, -10 = 10%% narrower)",
    )
    parser.add_argument(
        "--offset-x-pct",
        type=float,
        default=0.0,
        help="Shift x_center_ratio by this percentage-point delta (positive = right)",
    )
    parser.add_argument(
        "--offset-y-pct",
        type=float,
        default=0.0,
        help="Shift y_top_ratio by this percentage-point delta (positive = down)",
    )
    parser.add_argument(
        "--rotate-deg",
        type=float,
        default=None,
        help="Override the rule's rotation (positive = clockwise)",
    )
    args = parser.parse_args()

    blank_path = Path(args.blank)
    decoration_path = Path(args.decoration)
    for p, label in ((blank_path, "blank"), (decoration_path, "decoration")):
        if not p.exists():
            print(f"ERROR: {label} not found: {p}", file=sys.stderr)
            sys.exit(1)

    rules_path = Path(args.rules) if args.rules else _paths.effective_rules_path()

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = _paths.output_dir() / f"{uuid.uuid4().hex}.png"

    try:
        receipt = compose(
            blank_path=blank_path,
            decoration_path=decoration_path,
            category=args.category,
            placement=args.placement,
            rules_path=rules_path,
            output_path=output_path,
            auto_remove_bg=args.auto_remove_bg,
            width_delta_pct=args.width_delta_pct,
            offset_x_pct=args.offset_x_pct,
            offset_y_pct=args.offset_y_pct,
            rotate_deg_override=args.rotate_deg,
        )
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERROR: compose failed: {e}", file=sys.stderr)
        sys.exit(2)

    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
