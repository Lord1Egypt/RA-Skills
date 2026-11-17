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
    4. Prepare the decoration's alpha (see _prepare_decoration): art already cut
       out is trusted; art on a SOLID opaque plate (a logo on a black / white /
       coloured field — the common DTF-preview shape) has that plate color-keyed
       to transparent BY DEFAULT so it never composites as a coloured box; a
       photographic subject on a non-uniform opaque background is segmented
       (rembg) only when ``--auto-remove-bg`` is passed.
    5. Normalise the artwork's framing: trim the decoration to its alpha content
       box (so placement refers to the visible art, not the source file's
       incidental padding), then add back a *calculated* horizontal safe-margin
       (rule ``side_pad_ratio`` / ``--side-pad-pct``) so a full-front print sits a
       touch in from the garment edges instead of running out to them.
    6. Scale the decoration (aspect-locked), rotate with expand=True, and
       alpha-composite onto the blank.
    7. Write the PNG and emit a JSON receipt to stdout so the caller can
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
        [--rotate-deg 0] [--side-pad-pct 6] \
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
import _bootstrap  # noqa: E402

# bbox detection segments with rembg, so ensure the full imaging+segmentation set
# up front — otherwise the lazy import in detect_garment_bbox would re-exec mid-run.
_bootstrap.ensure(_bootstrap.REMBG, _bootstrap.REMBG_MODS)


_DEFAULTS_KEY = "_defaults"


def _load_rules(path: Path) -> dict:
    try:
        rules = json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(
            f"ERROR: rules file not found at {path}. Point --rules at a valid "
            "placement_rules.json or create one with edit_placement_rule.py."
        )
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: rules file at {path} is not valid JSON: {e}")
    # An editable copy in the data dir was seeded from an older bundled catalog
    # and never learns placements added since (right_chest for hoodies,
    # left/right_sleeve, …). Fill those in from the bundle; any placement the
    # copy does define still wins, so human edits are never overridden.
    if path.resolve() != _paths.BUNDLED_RULES.resolve() and _paths.BUNDLED_RULES.exists():
        for cat, bucket in json.loads(_paths.BUNDLED_RULES.read_text()).items():
            if isinstance(bucket, dict):
                mine = rules.setdefault(cat, {})
                for placement, rule in bucket.items():
                    mine.setdefault(placement, rule)
    return rules


# LEFT/RIGHT IN A PLACEMENT NAME ARE THE WEARER'S. Blanks are flat FRONT photos,
# so the wearer's left chest / left sleeve sits on the IMAGE's RIGHT half
# (x_center_ratio > 0.5) and the wearer's right on the image's left half. The
# catalog once shipped this mirrored, and an editable copy seeded from it may
# still live in the data dir — so the invariant is enforced here on every
# compose rather than trusted.
_WEARER_SIDE_IMAGE_HALF = {"left": "right", "right": "left"}


def _orientation_guard(rule: dict, placement: str) -> tuple[dict, str | None]:
    """Return ``(rule, warning)``; mirrors a rule that puts a wearer-side
    placement on the wrong half of a front photo."""
    side = placement.split("_", 1)[0]
    want = _WEARER_SIDE_IMAGE_HALF.get(side)
    if not want or "back" in placement:
        return rule, None
    x = float(rule["x_center_ratio"])
    wrong = (want == "right" and x < 0.5) or (want == "left" and x > 0.5)
    if not wrong:
        return rule, None
    fixed = dict(rule, x_center_ratio=round(1.0 - x, 4))
    return fixed, (
        f"rule for '{placement}' had x_center_ratio={x} (the {side.upper()} side "
        f"of the IMAGE) — mirrored to {fixed['x_center_ratio']}: the wearer's "
        f"{side} is the image's {want} on a front photo. Fix the catalog with "
        f"edit_placement_rule.py.")


def _resolve_rule(rules: dict, category: str | None, placement: str) -> tuple[dict, str]:
    """Return ``(rule, resolved_category)``. Falls back to ``_defaults``."""
    if placement == "sleeve":
        raise SystemExit(
            "ERROR: 'sleeve' is ambiguous — use left_sleeve or right_sleeve "
            "(the WEARER's side; the wearer's left sleeve is on the image's right).")
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


# A decoration that arrives as flat art on a SOLID opaque plate (a logo on a
# black / white / coloured field — the common DTF-preview shape) must have that
# plate keyed out before compositing, or the mockup shows the art inside a
# coloured box. These gate the automatic color-key so it fires only on a genuine
# uniform plate, never on real art.
_PLATE_UNIFORM_TOL = 24.0   # max RGB spread across the 4 corners to call it "solid"
_PLATE_MIN_REMOVED = 0.05   # the keyed result must clear at least this much, else it was not a plate

# After the plate is keyed out (or on already-cut art), the real logo usually
# sits inside a wide field of now-transparent pixels — a near-square DTF preview
# with a centred logo is the classic case. Placement anchors the decoration's
# TOP edge at y_top_ratio, so those transparent top margins shove the artwork
# down the garment: a full-front CHEST logo ends up on the belly. Trimming the
# decoration to its alpha content box makes every placement ratio refer to the
# visible art instead of the padded plate.
_TRIM_ALPHA_THRESHOLD = 26  # 0-255; treat fainter alpha as noise when finding content


def _color_to_alpha(rgb, key):
    """GIMP color-to-alpha (mirrors knockout_color.py).

    ``rgb`` is HxWx3 float32 (0..255), ``key`` len-3. Returns
    ``(out_rgb uint8, alpha01 float)`` — the key color becomes transparent and
    the true foreground colour is un-multiplied back out so edges stay crisp.
    """
    import numpy as np

    p = rgb.astype(np.float32)
    k = np.asarray(key, dtype=np.float32)
    dist_hi = np.where(p > k, (p - k) / np.maximum(255.0 - k, 1e-6), 0.0)
    dist_lo = np.where(p < k, (k - p) / np.maximum(k, 1e-6), 0.0)
    per_ch = np.clip(np.maximum(dist_hi, dist_lo), 0.0, 1.0)
    alpha = per_ch.max(axis=2)
    safe = np.maximum(alpha[..., None], 1e-6)
    fg = np.clip(k + (p - k) / safe, 0.0, 255.0)
    out_rgb = np.where(alpha[..., None] > 0.0, fg, 0.0).astype(np.uint8)
    return out_rgb, alpha


def _corner_key_spread(rgb):
    """Median colour of the four corners, and how far apart they are.

    A small spread means the corners agree → the art sits on one solid plate.
    """
    import numpy as np

    h, w, _ = rgb.shape
    c = max(1, min(8, h, w))
    meds = [
        np.median(rgb[y0:y0 + c, x0:x0 + c].reshape(-1, 3), axis=0)
        for (y0, x0) in ((0, 0), (0, w - c), (h - c, 0), (h - c, w - c))
    ]
    key = np.median(np.stack(meds), axis=0)
    spread = float(max(np.sqrt(((m - key) ** 2).sum()) for m in meds))
    return key, spread


def _prepare_decoration(decoration_path: Path, auto_remove_bg: bool):
    """Return ``(rgba_image, prep_info)`` with the decoration ready to composite.

    Decorations arrive in three shapes, each handled differently:

    * **Already cut out** (a real alpha channel) — trusted and composited as-is.
    * **Flat art on a solid opaque plate** (a logo on a black/white/coloured
      field — the common DTF-preview case) — that plate is color-keyed to
      transparent **by default**, because compositing a solid plate onto a
      garment is never what you want. This is what stops the "logo in a black
      box" mockup, and it needs no flag and no visual review to trigger.
    * **A photographic subject on a non-uniform opaque background** — segmented
      with rembg only when ``--auto-remove-bg`` is explicitly requested; we do
      not guess a cut on a complex opaque image.
    """
    from PIL import Image
    import numpy as np

    img = Image.open(decoration_path).convert("RGBA")
    arr = np.asarray(img)
    if int(arr[:, :, 3].min()) < 250:
        # Real transparency already present — it is cut out; leave it.
        return img, {"method": "already_transparent", "background_removed": False}

    rgb = arr[:, :, :3].astype(np.float32)
    key, spread = _corner_key_spread(rgb)
    if spread <= _PLATE_UNIFORM_TOL:
        # Opaque art on a uniform plate → key that plate out.
        out_rgb, alpha01 = _color_to_alpha(rgb, key)
        removed = float((alpha01 < 0.02).mean())
        if removed >= _PLATE_MIN_REMOVED:
            cut = np.dstack([
                out_rgb,
                np.clip(alpha01 * 255.0, 0, 255).round().astype(np.uint8),
            ])
            return Image.fromarray(cut, "RGBA"), {
                "method": "color_key",
                "key_color": "#{:02X}{:02X}{:02X}".format(*(int(round(v)) for v in key)),
                "removed_fraction": round(removed, 4),
                "background_removed": True,
            }

    if auto_remove_bg:
        # Explicitly requested photographic segmentation.
        from rembg import new_session, remove
        import io

        session = new_session("u2net")
        cut = remove(decoration_path.read_bytes(), session=session)
        return Image.open(io.BytesIO(cut)).convert("RGBA"), {
            "method": "rembg", "background_removed": True,
        }

    # Opaque, no uniform plate, no explicit rembg request → composite as-is.
    return img, {"method": "left_opaque", "background_removed": False}


def _trim_to_content(img, prep_info):
    """Crop transparent margins so placement refers to the artwork.

    Once the plate is keyed (or on already-cut art) the visible logo commonly
    occupies only the centre of the image. Because compose anchors the
    decoration's TOP edge at ``y_top_ratio``, any transparent top margin offsets
    the art downward — this is the "logo on the belly" bug. Cropping to the alpha
    content box removes that offset so a full-front chest logo lands on the chest.

    A small alpha threshold ignores near-transparent noise (JPEG ringing, keying
    residue) when locating content; it falls back to any non-zero alpha, and to
    the untrimmed image when there is nothing to trim (e.g. a fully opaque
    decoration). Trim metadata is recorded on ``prep_info`` for the receipt.
    """
    alpha = img.getchannel("A")
    mask = alpha.point(lambda a: 255 if a >= _TRIM_ALPHA_THRESHOLD else 0)
    bbox = mask.getbbox() or alpha.getbbox()
    prep_info["trimmed"] = False
    if not bbox:
        return img
    w, h = img.size
    if bbox == (0, 0, w, h):
        return img
    cropped = img.crop(bbox)
    prep_info["trimmed"] = True
    prep_info["content_bbox"] = list(bbox)
    prep_info["size_before_trim_px"] = [w, h]
    prep_info["size_after_trim_px"] = list(cropped.size)
    return cropped


def _pad_to_safe_area(img, side_pad_ratio, prep_info):
    """Add a calculated transparent side margin to the (already trimmed) art.

    ``side_pad_ratio`` is the fraction of the FINAL print box left empty on EACH
    side. After compose scales the padded box to ``width_ratio`` of the garment,
    the visible art spans ``(1 - 2*side_pad_ratio)`` of that box, so it sits a
    touch in from the garment edges instead of running out to them. Because the
    art is trimmed to its content first, this margin is deterministic — it no
    longer depends on whatever incidental padding the source file shipped with.

    Padding is horizontal only, so the vertical (chest) anchor is unchanged; the
    aspect-locked scale in ``compose`` then shrinks the art slightly and evenly to
    make room. Trim/pad metadata is recorded on ``prep_info`` for the receipt.
    """
    prep_info["side_padded"] = False
    if not side_pad_ratio or side_pad_ratio <= 0:
        return img
    from PIL import Image

    ratio = min(max(float(side_pad_ratio), 0.0), 0.45)
    w, h = img.size
    padded_w = int(round(w / max(1e-6, 1.0 - 2.0 * ratio)))
    pad_x = max(0, (padded_w - w) // 2)
    if pad_x == 0:
        return img
    out = Image.new("RGBA", (w + 2 * pad_x, h), (0, 0, 0, 0))
    out.paste(img, (pad_x, 0))
    prep_info["side_padded"] = True
    prep_info["side_pad_ratio"] = round(ratio, 4)
    prep_info["side_pad_px"] = pad_x
    return out


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
    side_pad_pct_override: float | None,
    bbox: dict | None = None,
    base_path: Path | None = None,
    decoration_image=None,
) -> dict:
    from PIL import Image

    rules = _load_rules(rules_path)
    rule, resolved_category = _resolve_rule(rules, category, placement)
    rule, orientation_warning = _orientation_guard(rule, placement)

    # ``bbox`` / ``base_path`` let a caller layer several decorations onto one
    # blank: detect the garment once on the clean blank, then paste each layer
    # onto the previous layer's output.
    bbox = bbox or _detect_bbox(blank_path)
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

    if decoration_image is not None:
        # Already prepared by the caller (e.g. web_mockup_job's art prep).
        decoration, prep = decoration_image.convert("RGBA"), {"method": "prepared_by_caller"}
    else:
        decoration, prep = _prepare_decoration(decoration_path, auto_remove_bg)
    decoration = _trim_to_content(decoration, prep)
    # Calculated side safe-margin: rule's side_pad_ratio, overridable per run.
    side_pad_ratio = (
        side_pad_pct_override / 100.0
        if side_pad_pct_override is not None
        else float(rule.get("side_pad_ratio", 0.0))
    )
    decoration = _pad_to_safe_area(decoration, side_pad_ratio, prep)
    src_w, src_h = decoration.size
    if src_w == 0 or src_h == 0:
        raise SystemExit("ERROR: decoration image has zero-sized dimension")

    target_w = max(1, int(round(bb_w * width_ratio)))
    target_h = max(1, int(round(target_w * (src_h / src_w))))

    # Optional height cap: some locations have a fixed print box (e.g. a
    # hoodie full-front must clear the pocket, ~9"). If the aspect-locked
    # height exceeds max_height_ratio * bbox height, scale both dims down so
    # the print fits the box — aspect ratio preserved, smaller dimension wins.
    max_height_ratio = rule.get("max_height_ratio")
    height_capped = False
    if max_height_ratio is not None:
        max_h = max(1, int(round(bb_h * float(max_height_ratio))))
        if target_h > max_h:
            target_h = max_h
            target_w = max(1, int(round(target_h * (src_w / src_h))))
            height_capped = True

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

    blank = Image.open(base_path or blank_path).convert("RGBA")
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
            "side_pad_ratio": side_pad_ratio,
            "max_height_ratio": max_height_ratio,
            "height_capped": height_capped,
            "effective_width_ratio": target_w / bb_w,
        },
        "orientation_warning": orientation_warning,
        "decoration_size_px": [rot_w, rot_h],
        "paste_top_left_px": [paste_x, paste_y],
        "background_removed": prep.get("background_removed", False),
        "decoration_prep": prep,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose a decoration onto a blank product photo")
    parser.add_argument("--blank", required=True, help="Path to the blank product image")
    parser.add_argument("--decoration", required=True, help="Path to the decoration image")
    parser.add_argument("--category", default=None, help="Garment category (hoodie, tee, hat, mug, ...)")
    parser.add_argument("--placement", default="full_front", help="Placement name (full_front, left_chest, right_sleeve, ...). "
                        "Left/right are the WEARER's: left_chest lands on the IMAGE's right.")
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
        help="Segment a PHOTOGRAPHIC decoration off a non-uniform opaque "
        "background with rembg. A solid art plate (logo on a black/white/"
        "coloured field) is color-keyed automatically without this flag.",
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
    parser.add_argument(
        "--side-pad-pct",
        type=float,
        default=None,
        help="Override the placement's side_pad_ratio: the percent of the print box "
        "left empty on EACH side. Adds a calculated horizontal safe-margin AFTER the "
        "art is trimmed to its content, so the print sits a touch in from the garment "
        "edges (e.g. 6 = 6%% margin per side). Only affects placements that use it.",
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
            side_pad_pct_override=args.side_pad_pct,
        )
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERROR: compose failed: {e}", file=sys.stderr)
        sys.exit(2)

    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
