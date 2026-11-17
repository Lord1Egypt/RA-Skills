#!/usr/bin/env python3
"""Independent vision QA for a rendered mockup — a yes/no verdict as JSON.

The agent running the web-image routine must never pull image bytes into its
own context (a few images balloon a session). So the eyes-on review is done
HERE, out of band: this script sends the downscaled mockup (plus a reference
strip of the prepared artwork) straight to a vision model over HTTP and prints
only a small JSON verdict. The agent reads the verdict, never the picture.

The reviewer is told the placement contract explicitly, with LEFT/RIGHT spelled
out in both frames (the wearer's side AND the image side), and must answer in
IMAGE coordinates for any fix so its suggested deltas map 1:1 onto
``compose_mockup.py``'s ``--offset-x-pct`` (positive = image right),
``--offset-y-pct`` (positive = down) and ``--width-delta-pct``.

Config (env):
    MOCKUP_VISION_API_KEY   — or OPENROUTER_API_KEY (required)
    MOCKUP_VISION_MODEL     — default ``anthropic/claude-sonnet-5``
    MOCKUP_VISION_BASE_URL  — OpenAI-compatible chat endpoint base,
                              default ``https://openrouter.ai/api/v1``

CLI (debugging):
    python3 scripts/vision_review.py --mockup out.png --spec spec.json [--art a.png ...]
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_MODEL = "anthropic/claude-sonnet-5"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
_REVIEW_MAX_PX = 1024

_CHECKS = [
    "blank_is_real_garment",   # a real product photo, not a placeholder/icon
    "background_removed",      # no box/plate/halo from the art's original background
    "correct_side",            # each print on the side the spec says
    "on_garment",              # inside the garment, not clipped, not on collar/sleeve seams
    "clear_of_sleeve",         # chest prints on the chest panel, measured from the garment's own centre line
    "size_reasonable",         # size matches the placement class
    "art_intact",              # art not cropped, distorted, mirrored, or unreadable
]

SYSTEM_PROMPT = """You are a strict QA inspector for apparel product mockups that \
will be published as store thumbnails. You are shown (1) a MOCKUP: a flat front \
photo of a blank garment with one or more decorations composited on it, and \
optionally (2) ART REFERENCE: the prepared artwork for each decoration on a gray \
checker card.

ORIENTATION — read carefully, this is the most common failure:
- Placement names use the WEARER'S left/right. The photo shows the garment from \
the FRONT, as if the wearer faces you. So the wearer's LEFT chest/sleeve appears \
on the IMAGE'S RIGHT half, and the wearer's RIGHT appears on the IMAGE'S LEFT half.
- Every decoration in the spec states its required IMAGE side explicitly. Judge \
against the image side. Give every fix in IMAGE coordinates.

Check each item and answer only with JSON:
{
  "verdict": "yes" | "no",
  "checks": {"blank_is_real_garment": bool, "background_removed": bool,
             "correct_side": bool, "on_garment": bool, "clear_of_sleeve": bool,
             "size_reasonable": bool, "art_intact": bool},
  "issues": [
    {"decoration_id": int | null,
     "code": "wrong_side" | "background_visible" | "too_high" | "too_low" |
             "too_far_left" | "too_far_right" | "too_big" | "too_small" |
             "clipped" | "on_sleeve" | "art_damaged" | "bad_blank" | "other",
     "detail": "one short sentence",
     "fix": {"offset_x_pct": number, "offset_y_pct": number,
             "width_delta_pct": number}}
  ],
  "summary": "one short sentence"
}

BACKGROUND — the second most common failure: the print must be only the \
design's own marks on the garment. A solid or textured coloured rectangle, box, \
panel, swatch or rounded plate behind the logo (often a fabric colour from an \
embroidery preview, or white/black from a thumbnail) is a LEFTOVER BACKGROUND: \
set background_removed=false, report background_visible, answer "no". This \
holds even when the ART REFERENCE shows the same box — the reference is the \
prepared art and can carry the same leftover. Look for a hard-edged block of \
colour around the logo that is not the garment's own colour.

CENTRE LINE — judge every position against the GARMENT'S OWN centre line: the \
zipper, placket, or the middle of the neckline. Not the middle of the photo, and \
not the middle of the garment's outline. Vendor photos are often shot on a form \
turned slightly to one side: the centre line is then off-centre, one chest panel \
looks narrower, and one sleeve looks bigger. A chest print must sit ON the chest \
panel, between the centre line and the armhole seam, clearly inside that panel. \
If any part of it touches or crosses the armhole seam, sits on the sleeve or the \
shoulder, or is closer to the armhole seam than to the centre line, set \
clear_of_sleeve=false, report on_sleeve with the offset_x_pct that moves it back \
toward the centre line, and answer "no". A turned photo is still a usable blank — \
do NOT call it bad_blank.

BLANK — bad_blank is only for a photo that cannot be a product image: an "image \
not available" / placeholder graphic, an icon or drawing, a person wearing the \
garment, or a different product.

Rules: "yes" only if every check passes and a shopper would accept the image. \
Fix deltas: offset_x_pct is percentage points of garment width, POSITIVE MOVES \
RIGHT in the image; offset_y_pct is percentage points of garment height, \
POSITIVE MOVES DOWN; width_delta_pct is percent change in print width. Use \
0 for axes that are fine; use small corrections (2-10) unless clearly far off. \
For a print on the wrong side, give the offset_x_pct that moves it to the mirror \
position. background_visible and bad_blank cannot be fixed by moving — give no \
fix for them. Output JSON only, no prose."""


def _img_to_data_url(img, max_px: int = _REVIEW_MAX_PX) -> str:
    from PIL import Image

    im = img.copy()
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        bg.paste(im, mask=im.getchannel("A"))
        im = bg
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.convert("RGB").save(buf, format="JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def art_reference_strip(art_images, height: int = 256):
    """Prepared art on a gray checker card, side by side — shows the reviewer
    whether a background plate survived the knockout."""
    from PIL import Image, ImageDraw

    tiles = []
    for art in art_images:
        a = art.convert("RGBA")
        a.thumbnail((height, height))
        card = Image.new("RGBA", (height, height), (150, 150, 150, 255))
        d = ImageDraw.Draw(card)
        s = 16
        for y in range(0, height, s):
            for x in range(0, height, s):
                if (x // s + y // s) % 2:
                    d.rectangle([x, y, x + s - 1, y + s - 1], fill=(185, 185, 185, 255))
        card.alpha_composite(a, ((height - a.width) // 2, (height - a.height) // 2))
        tiles.append(card)
    if not tiles:
        return None
    strip = Image.new("RGBA", (height * len(tiles) + 8 * (len(tiles) - 1), height),
                      (255, 255, 255, 255))
    for i, t in enumerate(tiles):
        strip.paste(t, (i * (height + 8), 0))
    return strip


# What a correct print looks like, per placement — concrete enough that the
# reviewer can say "no" to a chest logo drifting toward the centre or the pocket
# (store 17: a youth-hoodie left chest ended up low and central and was passed),
# without over-steering: "halfway to the side seam, not near the drawstrings"
# made it push a correct hoodie logo out to the armhole (24942 grey, +6 x).
_PLACEMENT_LOOK = {
    "left_chest": ("small (a pocket-sized logo, roughly 1/7 of the garment width) on the "
                   "IMAGE-RIGHT half of the upper chest: clearly off the centre line but "
                   "well inside the side seam — about a third of the way from the centre "
                   "line toward the side seam; top edge a little below where the "
                   "neckline meets the shoulder. On a hoodie, sitting beside or near the "
                   "drawstrings is NORMAL and is not a reason to move it outward; it must "
                   "never approach the armhole/sleeve seam, and must not drop toward the "
                   "pocket or belly"),
    "right_chest": ("small (a pocket-sized logo, roughly 1/7 of the garment width) on the "
                    "IMAGE-LEFT half of the upper chest: clearly off the centre line but "
                    "well inside the side seam — about a third of the way from the centre "
                    "line toward the side seam; top edge a little below where the "
                    "neckline meets the shoulder. On a hoodie, sitting beside or near the "
                    "drawstrings is NORMAL and is not a reason to move it outward; it must "
                    "never approach the armhole/sleeve seam, and must not drop toward the "
                    "pocket or belly"),
    "center_chest": "small, horizontally centred, upper chest just below the neckline",
    "left_leg": ("on the FRONT of the wearer's left leg = the leg on the IMAGE RIGHT "
                 "(shorts/pants): roughly centred on that leg's width, on the lower "
                 "thigh a little above the hem; never on the waistband or crossing "
                 "into the other leg"),
    "right_leg": ("on the FRONT of the wearer's right leg = the leg on the IMAGE LEFT "
                  "(shorts/pants): roughly centred on that leg's width, on the lower "
                  "thigh a little above the hem; never on the waistband or crossing "
                  "into the other leg"),
    "full_front": ("large, horizontally centred, top edge a few inches below the neckline; "
                   "on a hoodie it must end above the front pocket"),
    "left_sleeve": "small, on the sleeve at the IMAGE RIGHT, upper arm",
    "right_sleeve": "small, on the sleeve at the IMAGE LEFT, upper arm",
    "front": "centred on the front panel",
}

_HOODIE_NOTE = ("This is a hoodie: the hood occupies the top of the photo, so the "
                "chest starts lower than on a tee — judge the chest relative to the "
                "neckline and the pocket, not the top of the image.")


def spec_text(spec: dict) -> str:
    lines = [f"Garment: {spec.get('product_name') or 'unknown'}; "
             f"colour: {spec.get('color') or 'unknown'}.",
             "Decorations that MUST appear on this front image:"]
    for layer in spec.get("layers", []):
        side = layer.get("image_side")
        where = {"right": "RIGHT half of the IMAGE",
                 "left": "LEFT half of the IMAGE",
                 "center": "horizontally CENTERED"}.get(side, "unspecified")
        wearer = layer.get("wearer_side")
        wearer_txt = f" (the wearer's {wearer})" if wearer else ""
        lines.append(
            f"- decoration_id {layer['decoration_id']} \"{layer.get('name')}\": "
            f"placement {layer['placement']}{wearer_txt} → must be on the {where}. "
            f"Correct look: {_PLACEMENT_LOOK.get(layer['placement'], 'per placement')}.")
    if "hood" in (spec.get("product_name") or "").lower():
        lines.append(_HOODIE_NOTE)
    lines.append("Answer \"no\" if a print is noticeably off its correct look, even if "
                 "it is on the right side — a store thumbnail should look professionally placed.")
    if spec.get("omitted"):
        lines.append("Back-of-garment decorations are intentionally NOT shown.")
    return "\n".join(lines)


def _parse_json(text: str) -> dict | None:
    text = (text or "").strip()
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except ValueError:
        return None


def _normalize(result: dict) -> dict:
    verdict = str(result.get("verdict", "")).strip().lower()
    checks = result.get("checks") or {}
    checks = {k: bool(checks.get(k, False)) for k in _CHECKS}
    issues = []
    for it in result.get("issues") or []:
        if not isinstance(it, dict):
            continue
        fix = it.get("fix") or {}
        clean_fix = {}
        for k in ("offset_x_pct", "offset_y_pct", "width_delta_pct"):
            try:
                v = float(fix.get(k, 0) or 0)
            except (TypeError, ValueError):
                v = 0.0
            if v:
                clean_fix[k] = max(-40.0, min(40.0, v))
        issues.append({
            "decoration_id": it.get("decoration_id"),
            "code": str(it.get("code") or "other"),
            "detail": str(it.get("detail") or "")[:240],
            "fix": clean_fix,
        })
    # A "yes" with a failed check is not a yes.
    ok = verdict == "yes" and all(checks.values())
    return {"verdict": "yes" if ok else "no", "checks": checks, "issues": issues,
            "summary": str(result.get("summary") or "")[:300]}


def review(mockup_path: Path, spec: dict, art_images=None, *,
           api_key: str | None = None, model: str | None = None,
           base_url: str | None = None, timeout: float = 90.0) -> dict:
    """Return ``{"verdict": "yes"|"no"|"error", ..., "usage": {..., "cost_usd"}}``.
    Never raises on a model/HTTP problem — an unreviewable mockup is an
    ``error`` verdict, which the caller must treat as NOT approved."""
    import requests
    from PIL import Image

    api_key = api_key or os.environ.get("MOCKUP_VISION_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    model = model or os.environ.get("MOCKUP_VISION_MODEL") or DEFAULT_MODEL
    base_url = (base_url or os.environ.get("MOCKUP_VISION_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    if not api_key:
        return {"verdict": "error", "error": "no vision API key (set MOCKUP_VISION_API_KEY "
                "or OPENROUTER_API_KEY)", "model": model}

    content = [
        {"type": "text", "text": spec_text(spec)},
        {"type": "text", "text": "MOCKUP:"},
        {"type": "image_url", "image_url": {"url": _img_to_data_url(Image.open(mockup_path))}},
    ]
    strip = art_reference_strip(art_images or [])
    if strip is not None:
        content += [
            {"type": "text", "text": "ART REFERENCE (prepared art on a checker card, "
                                     "left to right in spec order). Any solid box or "
                                     "plate visible here is a leftover background, "
                                     "not part of the design:"},
            {"type": "image_url", "image_url": {"url": _img_to_data_url(strip, 768)}},
        ]
    body = {
        "model": model,
        "temperature": 0,
        "max_tokens": 800,
        # OpenRouter usage accounting: the response carries the call's exact
        # cost (usage.cost, USD) so runs can report what the review spent.
        "usage": {"include": True},
        "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                     {"role": "user", "content": content}],
    }
    try:
        resp = requests.post(f"{base_url}/chat/completions", json=body, timeout=timeout,
                             headers={"Authorization": f"Bearer {api_key}"})
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        return {"verdict": "error", "error": f"{type(exc).__name__}: {exc}", "model": model}
    usage = _usage(data)
    if resp.status_code != 200:
        return {"verdict": "error", "model": model, "usage": usage,
                "error": f"HTTP {resp.status_code}: {str(data)[:300]}"}
    try:
        text = data["choices"][0]["message"]["content"] or ""
        if isinstance(text, list):
            text = "".join(p.get("text", "") for p in text if isinstance(p, dict))
    except (KeyError, IndexError, TypeError):
        return {"verdict": "error", "model": model, "usage": usage,
                "error": "malformed response"}
    parsed = _parse_json(text)
    if parsed is None:
        return {"verdict": "error", "model": model, "usage": usage,
                "error": "reviewer did not return JSON", "raw": str(text)[:300]}
    out = _normalize(parsed)
    out["model"] = model
    out["usage"] = usage
    return out


def _usage(data) -> dict:
    """Tokens + cost of one call. ``cost_usd`` is None when the endpoint does
    not report cost (a non-OpenRouter base URL) — unknown, not free."""
    u = (data or {}).get("usage") if isinstance(data, dict) else None
    u = u or {}
    cost = u.get("cost")
    try:
        cost = round(float(cost), 6) if cost is not None else None
    except (TypeError, ValueError):
        cost = None
    return {"prompt_tokens": u.get("prompt_tokens"),
            "completion_tokens": u.get("completion_tokens"),
            "cost_usd": cost,
            "generation_id": (data or {}).get("id") if isinstance(data, dict) else None}


def main() -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _bootstrap  # noqa: E402

    _bootstrap.ensure(_bootstrap.IMAGING + ["requests>=2.31,<3"],
                      _bootstrap.IMAGING_MODS + ["requests"])
    from PIL import Image

    ap = argparse.ArgumentParser(description="Vision yes/no review of a mockup")
    ap.add_argument("--mockup", required=True)
    ap.add_argument("--spec", required=True, help="JSON file: {product_name, color, layers:[...]}")
    ap.add_argument("--art", action="append", default=[], help="prepared art PNG(s)")
    ap.add_argument("--model", default=None)
    args = ap.parse_args()
    spec = json.loads(Path(args.spec).read_text())
    arts = [Image.open(p) for p in args.art]
    print(json.dumps(review(Path(args.mockup), spec, arts, model=args.model)))


if __name__ == "__main__":
    main()
