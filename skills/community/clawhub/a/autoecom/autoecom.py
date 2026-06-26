#!/usr/bin/env python3
"""autoecom CLI — utility commands for the daily ecommerce carousel pipeline.

Architecture: this script is the GLUE. The brand kit (logo, colors, font, voice),
the bestseller pick, the slide plan, the post caption — all of that creative /
identity work is done by the agent (Claude / openclaw) using its multimodal
abilities and direct WebFetch / Read / Write access. This script only handles
the mechanical bits the agent can't do directly:

    download <url> <out>          download a file (logo, product image)
    palette <image>               extract dominant hex colors from an image
    product <url>                 parse a product page's JSON-LD into a dict
    generate <plan.json>          nano-banana → raw stylized images per slide
    compose <plan.json>           Pillow overlay → final 1080x1350 slides
    publish <plan.json>           Upload-Post photo carousel → IG + TikTok
    mark-processed <url>
    list-processed

Run `autoecom.py --help` for CLI flags. The agent calls these one at a time
so it can stop between steps for human approval.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

OUTPUT_FOLDER = Path(os.getenv("OUTPUT_FOLDER", ROOT / "output")).expanduser()
STATE_FOLDER = ROOT / "state"
STATE_FILE = STATE_FOLDER / "processed.json"

GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
GEMINI_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
UPLOAD_POST_BASE = "https://api.upload-post.com/api"

LEARNINGS_FOLDER = ROOT / "learnings"
RUNS_FOLDER = LEARNINGS_FOLDER / "runs"
HOT_HOOKS_FILE = LEARNINGS_FOLDER / "HOT_HOOKS.md"
HOT_IMAGERY_FILE = LEARNINGS_FOLDER / "HOT_IMAGERY.md"
POST_HISTORY = LEARNINGS_FOLDER / "post-history.jsonl"
CANDIDATE_HISTORY = LEARNINGS_FOLDER / "candidate-history.jsonl"
METRICS_FILE = LEARNINGS_FOLDER / "metrics.jsonl"

CANVAS_W, CANVAS_H = 1080, 1350  # 4:5 — IG carousel native, TikTok photo OK
DEFAULT_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


# ========== generic helpers ==========

def log(msg: str) -> None:
    print(f"[autoecom] {msg}", file=sys.stderr)


def http_get(url: str, *, timeout: int = 30) -> requests.Response:
    res = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
    res.raise_for_status()
    return res


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:60] or "product"


def product_slug_from_url(url: str) -> str:
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        return slugify(parsed.netloc)
    return slugify(parts[-1])


def today_dir() -> Path:
    return OUTPUT_FOLDER / datetime.now().strftime("%Y-%m-%d")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def candidate_id_from_plan(plan: dict) -> str:
    import hashlib
    payload = json.dumps({
        "url": plan.get("url"),
        "slides": [
            (s.get("role"), s.get("text_overlay"), s.get("image_prompt"))
            for s in plan.get("slides") or []
        ],
    }, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def hook_from_plan(plan: dict) -> str:
    for s in plan.get("slides") or []:
        if s.get("role") == "hook":
            return s.get("text_overlay") or ""
    slides = plan.get("slides") or []
    return (slides[0].get("text_overlay") if slides else "") or ""


def image_prompts_from_plan(plan: dict) -> list[str]:
    return [(s.get("image_prompt") or "") for s in plan.get("slides") or []]


def plan_summary(plan: dict) -> dict:
    product = plan.get("product") or {}
    return {
        "candidate_id": candidate_id_from_plan(plan),
        "product_url": plan.get("url") or product.get("url"),
        "product_name": product.get("name"),
        "category": product.get("category"),
        "hook_text": hook_from_plan(plan),
        "image_prompts": image_prompts_from_plan(plan),
        "slide_count": len(plan.get("slides") or []),
    }


# ========== download ==========

def cmd_download(args: argparse.Namespace) -> None:
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    log(f"GET {args.url}")
    res = http_get(args.url, timeout=60)
    out.write_bytes(res.content)
    print(json.dumps({
        "url": args.url,
        "path": str(out),
        "bytes": len(res.content),
        "content_type": res.headers.get("content-type"),
    }, indent=2))


# ========== palette ==========

def extract_dominant_colors(img: Image.Image, *, n: int = 5) -> list[str]:
    """Return up to n hex colors, skipping near-white / near-black / transparent."""
    rgba = img.convert("RGBA").resize((128, 128))
    pixels: list[tuple[int, int, int]] = []
    for r, g, b, a in list(rgba.getdata()):
        if a < 128:
            continue
        if r > 240 and g > 240 and b > 240:
            continue
        if r < 15 and g < 15 and b < 15:
            continue
        # Quantize to 5-bit per channel so similar shades cluster.
        pixels.append((r >> 3 << 3, g >> 3 << 3, b >> 3 << 3))
    if not pixels:
        return ["#222222"]
    counts = Counter(pixels).most_common(n)
    return [f"#{r:02x}{g:02x}{b:02x}" for (r, g, b), _ in counts]


def cmd_palette(args: argparse.Namespace) -> None:
    path = Path(args.image).resolve()
    if not path.exists():
        raise SystemExit(f"image not found: {path}")
    with Image.open(path) as im:
        colors = extract_dominant_colors(im, n=args.n)
    print(json.dumps({"image": str(path), "colors": colors}, indent=2))


# ========== product page extractor (JSON-LD) ==========

def _iter_jsonld_objects(data):
    if isinstance(data, dict):
        yield data
        for v in data.values():
            yield from _iter_jsonld_objects(v)
    elif isinstance(data, list):
        for item in data:
            yield from _iter_jsonld_objects(item)


def find_product_jsonld(soup: BeautifulSoup) -> dict | None:
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "{}")
        except json.JSONDecodeError:
            continue
        for candidate in _iter_jsonld_objects(data):
            t = candidate.get("@type")
            if t == "Product" or (isinstance(t, list) and "Product" in t):
                return candidate
    return None


def parse_product(url: str) -> dict:
    log(f"fetching product {url}")
    res = http_get(url, timeout=20)
    soup = BeautifulSoup(res.text, "lxml")
    product = find_product_jsonld(soup) or {}

    raw_images = product.get("image") or []
    if isinstance(raw_images, str):
        raw_images = [raw_images]
    elif isinstance(raw_images, dict):
        raw_images = [raw_images.get("url") or raw_images.get("@id")]
    images = [urljoin(url, i) for i in raw_images if i]

    if not images:
        for img in soup.select(".woocommerce-product-gallery__image img, .product-images img, figure img"):
            src = img.get("data-large_image") or img.get("data-src") or img.get("src")
            if src:
                images.append(urljoin(url, src))
        seen: set[str] = set()
        images = [i for i in images if not (i in seen or seen.add(i))]

    offers = product.get("offers") or {}
    if isinstance(offers, list) and offers:
        offers = offers[0]
    price = offers.get("price") if isinstance(offers, dict) else None
    currency = offers.get("priceCurrency") if isinstance(offers, dict) else None

    name = product.get("name") or (soup.title.string.strip() if soup.title else "Product")
    description = product.get("description") or ""
    if not description:
        og_desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
        if og_desc:
            description = og_desc.get("content", "")

    aggregate = product.get("aggregateRating") or {}
    rating = aggregate.get("ratingValue") if isinstance(aggregate, dict) else None
    review_count = aggregate.get("reviewCount") if isinstance(aggregate, dict) else None

    brand = product.get("brand")
    if isinstance(brand, dict):
        brand = brand.get("name")

    return {
        "url": url,
        "name": str(name).strip(),
        "description": str(description).strip(),
        "price": str(price) if price is not None else None,
        "currency": currency,
        "images": images[:8],
        "rating": rating,
        "review_count": review_count,
        "brand": brand,
        "sku": product.get("sku"),
    }


def cmd_product(args: argparse.Namespace) -> None:
    print(json.dumps(parse_product(args.url), indent=2, ensure_ascii=False))


# ========== nano-banana image generation ==========

def download_image(url: str) -> Image.Image:
    res = http_get(url, timeout=30)
    return Image.open(io.BytesIO(res.content)).convert("RGB")


def imagery_prior() -> str:
    """Read HOT_IMAGERY.md and return as a prompt prefix, or '' if absent."""
    if not HOT_IMAGERY_FILE.exists():
        return ""
    body = HOT_IMAGERY_FILE.read_text(encoding="utf-8").strip()
    if not body:
        return ""
    return (
        "PRIOR LEARNINGS — visual patterns that have outperformed for this brand. "
        "Apply when interpreting the slide brief; do not contradict explicit slide instructions.\n\n"
        f"{body}\n\n---\n\n"
    )


def cmd_generate(args: argparse.Namespace) -> None:
    from google import genai
    from google.genai import types

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY missing in .env")

    plan_path = Path(args.plan).resolve()
    plan = read_json(plan_path)
    out_dir = plan_path.parent
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    product = plan.get("product") or {}
    images = product.get("images") or []
    if not images:
        raise SystemExit("plan has no product.images — agent must include them in plan.json")

    # Reference image: agent can override per-slide via slide["ref_image_index"].
    default_ref_url = images[0]
    log(f"default reference image: {default_ref_url}")

    ref_cache: dict[int, Image.Image] = {}

    def get_ref(idx: int) -> Image.Image:
        if idx not in ref_cache:
            url = images[idx]
            log(f"downloading ref image [{idx}] {url}")
            ref_cache[idx] = download_image(url)
        return ref_cache[idx]

    # Always cache the default ref to disk so the user can inspect it.
    default_ref_img = get_ref(0)
    default_ref_img.save(raw_dir / "_ref.jpg", "JPEG", quality=92)

    client = genai.Client(api_key=api_key)
    slides = plan.get("slides", [])
    if not slides:
        raise SystemExit("plan has no slides")

    prior_prefix = imagery_prior()
    if prior_prefix:
        log(f"using HOT_IMAGERY.md prior ({len(prior_prefix)} chars prepended to each slide)")

    for i, slide in enumerate(slides, start=1):
        slot = raw_dir / f"slide_{i:02d}.png"
        if slot.exists() and not args.force:
            log(f"  slide {i:02d} already exists, skip (use --force to regenerate)")
            continue
        slide_prompt = slide.get("image_prompt") or "Stylized product shot."
        prompt = prior_prefix + slide_prompt
        ref_idx = slide.get("ref_image_index", 0)
        if not (0 <= ref_idx < len(images)):
            ref_idx = 0
        ref = get_ref(ref_idx)
        log(f"  generating slide {i:02d} ({slide.get('role','?')}) using ref [{ref_idx}] …")
        try:
            res = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=[ref, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"nano-banana call failed on slide {i}: {e}")

        saved = False
        for cand in res.candidates or []:
            for part in (cand.content.parts or []):
                inline = getattr(part, "inline_data", None)
                if inline and inline.data:
                    img = Image.open(io.BytesIO(inline.data)).convert("RGB")
                    img.save(slot, "PNG")
                    log(f"    → {slot} ({img.size[0]}x{img.size[1]})")
                    saved = True
                    break
            if saved:
                break
        if not saved:
            raise SystemExit(f"nano-banana returned no image for slide {i}")

    print(str(raw_dir))


# ========== Pillow composer ==========

def find_font(*, size: int) -> ImageFont.FreeTypeFont:
    override = os.getenv("BRAND_FONT_PATH")
    candidates: list[str] = []
    if override:
        candidates.append(override)
    candidates.extend(DEFAULT_FONT_CANDIDATES)
    for path in candidates:
        if path and Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def fit_text(draw: ImageDraw.ImageDraw, text: str, *,
             max_width: int, max_size: int, min_size: int) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    """Decrease font size until each wrapped line fits in max_width."""
    words = text.split()
    if not words:
        return find_font(size=max_size), [""]

    lines: list[str] = []
    for size in range(max_size, min_size - 1, -4):
        font = find_font(size=size)
        lines = []
        cur = words[0]
        for w in words[1:]:
            tentative = f"{cur} {w}"
            bbox = draw.textbbox((0, 0), tentative, font=font)
            if bbox[2] - bbox[0] <= max_width:
                cur = tentative
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        if all(draw.textbbox((0, 0), ln, font=font)[2] <= max_width for ln in lines):
            return font, lines
    return find_font(size=min_size), lines


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(ch * 2 for ch in hex_color)
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def fit_to_canvas(img: Image.Image, w: int, h: int) -> Image.Image:
    """Resize to fully cover w x h while keeping aspect, then center-crop."""
    src_ratio = img.width / img.height
    dst_ratio = w / h
    if src_ratio > dst_ratio:
        new_h = h
        new_w = int(round(h * src_ratio))
    else:
        new_w = w
        new_h = int(round(w / src_ratio))
    img2 = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return img2.crop((left, top, left + w, top + h))


def overlay_logo(canvas: Image.Image, logo_path: str | None) -> None:
    if not logo_path or not Path(logo_path).exists():
        return
    try:
        with Image.open(logo_path) as raw:
            logo = raw.convert("RGBA")
            target_w = int(CANVAS_W * 0.18)
            ratio = target_w / logo.width
            target_h = max(1, int(logo.height * ratio))
            logo = logo.resize((target_w, target_h), Image.LANCZOS)
            margin = int(CANVAS_W * 0.04)
            canvas.paste(logo, (margin, CANVAS_H - target_h - margin), logo)
    except Exception as e:  # noqa: BLE001
        log(f"logo overlay skipped: {e}")


def compose_slide(raw_path: Path, text: str, brand: dict, out_path: Path, *, role: str) -> None:
    primary = brand.get("primary_color") or "#000000"
    accent = brand.get("accent_color") or "#ffffff"

    with Image.open(raw_path).convert("RGB") as raw:
        canvas = fit_to_canvas(raw, CANVAS_W, CANVAS_H)

    # Bottom gradient so text stays legible on busy images.
    gradient = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gradient)
    grad_h = int(CANVAS_H * 0.45)
    for y in range(grad_h):
        alpha = int(180 * (y / grad_h))
        gd.line([(0, CANVAS_H - grad_h + y), (CANVAS_W, CANVAS_H - grad_h + y)], fill=(0, 0, 0, alpha))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), gradient)

    if text:
        draw = ImageDraw.Draw(canvas)
        max_w = int(CANVAS_W * 0.86)
        max_size = 140 if role == "hook" else 96
        min_size = 48
        rendered_text = text.upper() if role in {"hook", "cta"} else text
        font, lines = fit_text(
            draw, rendered_text,
            max_width=max_w, max_size=max_size, min_size=min_size,
        )
        ascent, descent = font.getmetrics()
        line_h = ascent + descent + int(font.size * 0.15)
        block_h = line_h * len(lines)
        y = CANVAS_H - block_h - int(CANVAS_H * 0.10)
        margin_x = int(CANVAS_W * 0.07)
        for ln in lines:
            draw.text(
                (margin_x, y), ln, font=font,
                fill=accent if role in {"hook", "cta"} else "white",
                stroke_width=max(2, font.size // 24),
                stroke_fill=primary,
            )
            y += line_h

    overlay_logo(canvas, brand.get("logo_path"))
    canvas.convert("RGB").save(out_path, "PNG")


def cmd_compose(args: argparse.Namespace) -> None:
    plan_path = Path(args.plan).resolve()
    plan = read_json(plan_path)
    out_dir = plan_path.parent
    raw_dir = out_dir / "raw"
    if not raw_dir.exists():
        raise SystemExit("no raw/ folder — run `generate` first")

    brand = plan.get("brand") or {}
    finals: list[Path] = []
    for i, slide in enumerate(plan.get("slides", []), start=1):
        raw = raw_dir / f"slide_{i:02d}.png"
        if not raw.exists():
            raise SystemExit(f"missing raw image for slide {i}: {raw}")
        out = out_dir / f"slide_{i:02d}.png"
        compose_slide(
            raw, slide.get("text_overlay", ""), brand, out, role=slide.get("role", ""),
        )
        log(f"  composed slide {i:02d} → {out}")
        finals.append(out)

    print(json.dumps([str(p) for p in finals], indent=2))


# ========== Upload-Post carousel ==========

def cmd_publish(args: argparse.Namespace) -> None:
    api_key = os.getenv("UPLOAD_POST_API_KEY")
    profile = os.getenv("UPLOAD_POST_PROFILE")
    if not api_key or not profile:
        raise SystemExit("UPLOAD_POST_API_KEY or UPLOAD_POST_PROFILE missing in .env")

    plan_path = Path(args.plan).resolve()
    plan = read_json(plan_path)
    out_dir = plan_path.parent

    slides = sorted(out_dir.glob("slide_*.png"))
    if not slides:
        raise SystemExit("no composed slides — run `compose` first")
    if len(slides) < 2:
        raise SystemExit(f"need at least 2 slides for a carousel, got {len(slides)}")
    if len(slides) > 10:
        log(f"capping carousel at 10 slides (had {len(slides)})")
        slides = slides[:10]

    caption = plan.get("caption", "")
    hashtags = plan.get("hashtags") or []
    description = caption + ("\n\n" + " ".join(hashtags) if hashtags else "")
    title = (plan.get("product") or {}).get("name") or "New product"

    platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]

    data: list[tuple[str, str]] = [
        ("user", profile),
        ("title", title[:140]),
        ("caption", description),
    ]
    for p in platforms:
        data.append(("platform[]", p))
    if "tiktok" in platforms:
        post_mode = "MEDIA_UPLOAD" if args.tiktok_mode == "draft" else "DIRECT_POST"
        data.append(("post_mode", post_mode))

    if args.dry_run:
        print(json.dumps({
            "DRY_RUN": True,
            "endpoint": f"{UPLOAD_POST_BASE}/upload_photos",
            "slides": [str(p) for p in slides],
            "fields": data,
        }, indent=2, ensure_ascii=False))
        return

    files = []
    handles = []
    try:
        for s in slides:
            fh = s.open("rb")
            handles.append(fh)
            files.append(("photos[]", (s.name, fh, "image/png")))

        log(f"uploading {len(slides)} slides to {platforms} …")
        res = requests.post(
            f"{UPLOAD_POST_BASE}/upload_photos",
            headers={"Authorization": f"Apikey {api_key}"},
            data=data,
            files=files,
            timeout=600,
        )
    finally:
        for fh in handles:
            fh.close()

    if res.status_code >= 400:
        sys.stderr.write(res.text + "\n")
        raise SystemExit(f"upload-post HTTP {res.status_code}")

    body = res.json()
    log("publish OK")

    published_at = datetime.now().isoformat(timespec="seconds")
    history = out_dir / "publish.json"
    history.write_text(json.dumps({
        "published_at": published_at,
        "url": plan.get("url"),
        "platforms": platforms,
        "response": body,
    }, indent=2, ensure_ascii=False))

    request_id = body.get("request_id") if isinstance(body, dict) else None
    summary = plan_summary(plan)
    append_jsonl(POST_HISTORY, {
        **summary,
        "request_id": request_id,
        "published_at": published_at,
        "platforms": platforms,
        "out_dir": str(out_dir),
    })
    log(f"appended to {POST_HISTORY.relative_to(ROOT)} (candidate_id={summary['candidate_id']})")

    print(json.dumps(body, indent=2, ensure_ascii=False))


# ========== state subcommands ==========

def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"cycle_started_at": None, "store": None, "products": []}
    state = json.loads(STATE_FILE.read_text())
    state.setdefault("cycle_started_at", None)
    state.setdefault("store", None)
    state.setdefault("products", [])
    return state


def save_state(state: dict) -> None:
    STATE_FOLDER.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def cmd_mark_processed(args: argparse.Namespace) -> None:
    state = load_state()
    now = datetime.now().isoformat(timespec="seconds")
    if state.get("cycle_started_at") is None:
        state["cycle_started_at"] = now
    if args.store:
        state["store"] = args.store

    existing = next((p for p in state["products"] if p["url"] == args.url), None)
    if existing:
        existing["last_processed_at"] = now
        existing["cycles_count"] = existing.get("cycles_count", 0) + 1
        existing["slides_published"] = args.slides
    else:
        state["products"].append({
            "url": args.url,
            "first_processed_at": now,
            "last_processed_at": now,
            "cycles_count": 1,
            "slides_published": args.slides,
        })
    save_state(state)
    log(f"marked {args.url} as processed (cycle started {state['cycle_started_at']})")


def cmd_list_processed(_: argparse.Namespace) -> None:
    print(json.dumps(load_state(), indent=2, ensure_ascii=False))


def cmd_new_cycle(_: argparse.Namespace) -> None:
    state = load_state()
    state["cycle_started_at"] = datetime.now().isoformat(timespec="seconds")
    save_state(state)
    log(f"new cycle started at {state['cycle_started_at']}")
    print(json.dumps({"cycle_started_at": state["cycle_started_at"]}, indent=2))


# ========== learnings: priors + log-candidate ==========

def cmd_priors(_: argparse.Namespace) -> None:
    """Dump current HOT_HOOKS.md and HOT_IMAGERY.md so the agent can inject them
    into the planning step. Empty strings if no prior exists yet."""
    payload = {
        "hooks": HOT_HOOKS_FILE.read_text(encoding="utf-8") if HOT_HOOKS_FILE.exists() else "",
        "imagery": HOT_IMAGERY_FILE.read_text(encoding="utf-8") if HOT_IMAGERY_FILE.exists() else "",
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_log_candidate(args: argparse.Namespace) -> None:
    """Append the agent's INITIAL plan proposal to candidate-history.jsonl, before
    any user editing. Reflect later compares this against post-history (what
    actually shipped) to extract the user's qualitative filter."""
    plan = read_json(Path(args.plan).resolve())
    summary = plan_summary(plan)
    append_jsonl(CANDIDATE_HISTORY, {
        **summary,
        "logged_at": datetime.now().isoformat(timespec="seconds"),
    })
    log(f"candidate {summary['candidate_id']} → {CANDIDATE_HISTORY.relative_to(ROOT)}")
    print(json.dumps({"candidate_id": summary["candidate_id"]}, indent=2))


# ========== learnings: learn (weekly metrics-driven) ==========

LEARN_HOOKS_PROMPT = """You are a senior ecommerce social-media strategist. You're refreshing a creator's HOT.md of HOOK COPY patterns based on real engagement data from their Instagram + TikTok carousels.

Below you will see:
1. The CURRENT HOT_HOOKS.md (or empty if none yet) — patterns we currently believe in.
2. WINNERS — carousels in the top percentile by composite score (z(views) * w_views + z(engagement_rate) * w_eng).
3. LOSERS — carousels in the bottom percentile.

For each carousel: the slide-1 hook_text on screen, slide_count, product_name, category, per-platform metrics, plus the rest of the slide hooks/text overlays for context.

YOUR JOB
Produce an updated HOT_HOOKS.md focused EXCLUSIVELY on slide-1 hook copy patterns. Examples of useful patterns: hook length, presence of numbers, question vs. statement form, emotional register, specificity, CTAs.

CONSTRAINTS
- Maximum 60 lines of markdown.
- Each bullet is single, actionable, falsifiable. No platitudes.
- Cite sample sizes: "(seen in 4/5 winners, 0/5 losers)".
- Merge with existing HOT_HOOKS.md: keep what's still corroborated, drop what's contradicted, add new patterns.
- Write in the dominant language of the hooks themselves.
- If evidence is weak (<3 winners or <3 losers), output the existing HOT_HOOKS.md plus a single appended bullet noting "evidence still thin, N carousels analyzed".

OUTPUT
Return ONLY the updated HOT_HOOKS.md content as plain markdown. No preamble, no JSON wrapper."""


LEARN_IMAGERY_PROMPT = """You are a senior visual director. You're refreshing a creator's HOT.md of IMAGE-PROMPT patterns based on real engagement data from their Instagram + TikTok carousels generated with Gemini 2.5 Flash Image (nano-banana).

Below you will see:
1. The CURRENT HOT_IMAGERY.md (or empty if none yet).
2. WINNERS — top-percentile carousels.
3. LOSERS — bottom-percentile carousels.

For each carousel: the per-slide image_prompts (the exact text sent to nano-banana), product_name, category, slide_count, per-platform metrics.

YOUR JOB
Produce an updated HOT_IMAGERY.md focused EXCLUSIVELY on image-prompt patterns. Examples of useful patterns: lighting style ("soft golden-hour", "studio softbox"), composition ("centered hero", "rule-of-thirds"), background ("minimalist gradient", "lifestyle context"), framing ("macro close-up", "wide flat-lay"), color treatment, subject pose, prop usage.

CONSTRAINTS
- Maximum 60 lines of markdown.
- Each bullet is single, actionable, falsifiable. No platitudes.
- Cite sample sizes: "(seen in 4/5 winners, 0/5 losers)".
- Merge with existing HOT_IMAGERY.md: keep what's still corroborated, drop what's contradicted.
- This file is auto-prepended to every nano-banana call, so write it AS DIRECT GUIDANCE TO AN IMAGE MODEL — use directive language ("prefer", "avoid").
- If evidence is weak (<3 winners or <3 losers), output the existing HOT_IMAGERY.md plus a single bullet noting "evidence still thin, N carousels analyzed".
- If the winners and losers have no image_prompts at all (empty lists everywhere), output the existing HOT_IMAGERY.md unchanged plus a single bullet noting "no image_prompt data available — keeping existing priors".

OUTPUT
Return ONLY the updated HOT_IMAGERY.md content as plain markdown. No preamble, no JSON wrapper."""


def _post_metrics(platforms: dict) -> dict:
    """Sum views/engagement across all platforms in a post-analytics response."""
    total_views = 0
    total_engagement = 0
    per_platform: dict = {}
    for platform, data in (platforms or {}).items():
        m = (data or {}).get("post_metrics") or {}
        views = int(m.get("views") or m.get("impressions") or m.get("reach") or 0)
        likes = int(m.get("likes") or 0)
        comments = int(m.get("comments") or 0)
        shares = int(m.get("shares") or 0)
        saves = int(m.get("saves") or 0)
        eng = likes + comments + shares + saves
        total_views += views
        total_engagement += eng
        per_platform[platform] = {
            "views": views, "likes": likes, "comments": comments,
            "shares": shares, "saves": saves, "engagement": eng,
        }
    eng_rate = total_engagement / total_views if total_views else 0.0
    return {
        "total_views": total_views,
        "total_engagement": total_engagement,
        "engagement_rate": eng_rate,
        "per_platform": per_platform,
    }


def _zscore(values: list[float]) -> list[float]:
    if not values:
        return []
    n = len(values)
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / n
    sd = var ** 0.5
    if sd == 0:
        return [0.0] * n
    return [(v - mean) / sd for v in values]


def cmd_learn(args: argparse.Namespace) -> None:
    from google import genai
    from google.genai import types

    api_key_up = os.getenv("UPLOAD_POST_API_KEY")
    api_key_g = os.getenv("GEMINI_API_KEY")
    if not api_key_up:
        raise SystemExit("UPLOAD_POST_API_KEY missing in .env")
    if not api_key_g:
        raise SystemExit("GEMINI_API_KEY missing in .env")

    history = read_jsonl(POST_HISTORY)
    if not history:
        raise SystemExit("post-history.jsonl is empty — publish some carousels first")

    now = datetime.now()
    soak_seconds = args.soak_days * 86400
    max_age_seconds = args.max_age_days * 86400

    eligible = []
    for h in history:
        try:
            pub = datetime.fromisoformat(h["published_at"])
        except (KeyError, ValueError):
            continue
        age = (now - pub).total_seconds()
        if soak_seconds <= age <= max_age_seconds:
            eligible.append(h)

    log(f"[learn] {len(eligible)} carousels in soak window ({args.soak_days}-{args.max_age_days}d)")
    if not eligible:
        raise SystemExit("no carousels in soak window — wait or shorten --soak-days")

    enriched = []
    for h in eligible:
        rid = h.get("request_id")
        if not rid:
            continue
        url = f"{UPLOAD_POST_BASE}/uploadposts/post-analytics/{rid}"
        try:
            r = requests.get(url, headers={"Authorization": f"Apikey {api_key_up}"}, timeout=30)
        except requests.RequestException as e:
            log(f"  {rid}: HTTP error {e}")
            continue
        if r.status_code >= 400:
            log(f"  {rid}: HTTP {r.status_code}: {r.text[:200]}")
            continue
        body = r.json()
        append_jsonl(METRICS_FILE, {
            "fetched_at": now.isoformat(timespec="seconds"),
            "request_id": rid,
            "candidate_id": h.get("candidate_id"),
            "raw": body,
        })
        m = _post_metrics(body.get("platforms") or {})
        enriched.append({**h, "metrics": m})

    if len(enriched) < args.min_cohort:
        msg = (f"only {len(enriched)} carousels have analytics — need >={args.min_cohort} "
               f"to refresh priors, retry later")
        log(f"[learn] {msg}")
        run_path = RUNS_FOLDER / f"learn-{now.strftime('%Y-%m-%d')}.md"
        run_path.parent.mkdir(parents=True, exist_ok=True)
        run_path.write_text(f"# Learn run — {now.date()}\n\n{msg}\n", encoding="utf-8")
        return

    views = [c["metrics"]["total_views"] for c in enriched]
    engs = [c["metrics"]["engagement_rate"] for c in enriched]
    z_views = _zscore(views)
    z_engs = _zscore(engs)
    for i, c in enumerate(enriched):
        c["composite"] = args.weight_views * z_views[i] + args.weight_engagement * z_engs[i]

    enriched.sort(key=lambda c: c["composite"], reverse=True)
    n = len(enriched)
    top_n = max(args.min_per_bucket, int(n * args.top_pct))
    bot_n = max(args.min_per_bucket, int(n * args.bottom_pct))
    # Guard against overlap when n is small.
    if top_n + bot_n > n:
        top_n = bot_n = max(1, n // 2)
    winners = enriched[:top_n]
    losers = enriched[-bot_n:]

    def render(c: dict) -> str:
        m = c["metrics"]
        return json.dumps({
            "product_name": c.get("product_name"),
            "category": c.get("category"),
            "hook_text": c.get("hook_text"),
            "image_prompts": c.get("image_prompts"),
            "slide_count": c.get("slide_count"),
            "metrics": {
                "total_views": m["total_views"],
                "total_engagement": m["total_engagement"],
                "engagement_rate": round(m["engagement_rate"], 4),
                "per_platform": m["per_platform"],
            },
            "composite_score": round(c["composite"], 3),
        }, ensure_ascii=False)

    winners_text = "\n".join(render(c) for c in winners)
    losers_text = "\n".join(render(c) for c in losers)

    client = genai.Client(api_key=api_key_g)

    def refresh(meta_prompt: str, current: str, target: Path, label: str) -> str:
        full = (
            meta_prompt
            + f"\n\n## CURRENT {target.name}\n"
            + (current or "(empty — first learn run)")
            + f"\n\n## WINNERS (top {len(winners)} of {n})\n" + winners_text
            + f"\n\n## LOSERS (bottom {len(losers)} of {n})\n" + losers_text
        )
        log(f"  calling {GEMINI_TEXT_MODEL} for {label}…")
        resp = client.models.generate_content(
            model=GEMINI_TEXT_MODEL,
            contents=[full],
            config=types.GenerateContentConfig(response_mime_type="text/plain"),
        )
        new_body = (resp.text or "").strip()
        if not new_body:
            log(f"  {label}: model returned empty output, keeping current")
            return current
        if target.exists():
            backup = LEARNINGS_FOLDER / f"{target.stem}.{now.strftime('%Y%m%d-%H%M%S')}.md.bak"
            backup.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
        LEARNINGS_FOLDER.mkdir(parents=True, exist_ok=True)
        target.write_text(new_body + "\n", encoding="utf-8")
        log(f"  {target.name} updated ({len(new_body)} chars)")
        return new_body

    current_hooks = HOT_HOOKS_FILE.read_text(encoding="utf-8") if HOT_HOOKS_FILE.exists() else ""
    current_imagery = HOT_IMAGERY_FILE.read_text(encoding="utf-8") if HOT_IMAGERY_FILE.exists() else ""
    new_hooks = refresh(LEARN_HOOKS_PROMPT, current_hooks, HOT_HOOKS_FILE, "HOT_HOOKS.md")
    new_imagery = refresh(LEARN_IMAGERY_PROMPT, current_imagery, HOT_IMAGERY_FILE, "HOT_IMAGERY.md")

    run_path = RUNS_FOLDER / f"learn-{now.strftime('%Y-%m-%d')}.md"
    run_path.parent.mkdir(parents=True, exist_ok=True)
    audit = [
        f"# Learn run — {now.isoformat(timespec='seconds')}",
        "",
        f"- soak: {args.soak_days}d / max age: {args.max_age_days}d",
        f"- weights: views={args.weight_views} engagement={args.weight_engagement}",
        f"- cohort: {n} carousels with analytics",
        f"- winners ({len(winners)}):",
    ]
    for w in winners:
        audit.append(
            f"  - score={w['composite']:.2f}  views={w['metrics']['total_views']}  "
            f"eng_rate={w['metrics']['engagement_rate']:.4f}  hook=\"{w.get('hook_text')}\""
        )
    audit.append(f"- losers ({len(losers)}):")
    for l in losers:
        audit.append(
            f"  - score={l['composite']:.2f}  views={l['metrics']['total_views']}  "
            f"eng_rate={l['metrics']['engagement_rate']:.4f}  hook=\"{l.get('hook_text')}\""
        )
    audit += ["", "## New HOT_HOOKS.md", "", new_hooks, "", "## New HOT_IMAGERY.md", "", new_imagery]
    run_path.write_text("\n".join(audit), encoding="utf-8")
    log(f"[learn] audit → {run_path}")


# ========== learnings: reflect (qualitative pass) ==========

REFLECT_PROMPT = """You are observing how a creator manually edits AI-proposed ecommerce carousel plans BEFORE engagement data exists.

You will see:
1. CANDIDATES — every initial plan the agent proposed (logged via log-candidate, before any user editing).
2. PUBLISHED — every carousel that actually shipped.

A candidate is "approved unchanged" if its candidate_id appears in PUBLISHED. A candidate is "rejected/edited" if its candidate_id is NOT in PUBLISHED for the same product (the agent or user revised it before publishing).

YOUR JOB
Identify qualitative patterns that explain the user's filter. Two separate buckets:
- HOOK observations (slide-1 text)
- IMAGERY observations (image_prompts)

Examples: "approves hooks containing a specific number", "rejects question-form hooks", "approves image_prompts mentioning soft natural light", "rejects busy lifestyle backgrounds".

CONSTRAINTS
- 3-6 hook observations + 3-6 imagery observations.
- Each: rule + evidence count ("approved 4/5 hooks <8 words, edited 3/3 with >12 words").
- Do not extrapolate to engagement.
- Write in the dominant language of the candidate hooks.

OUTPUT
Return STRICT JSON:
{"hook_observations": [{"rule": "...", "evidence": "..."}, ...],
 "imagery_observations": [{"rule": "...", "evidence": "..."}, ...]}"""


def cmd_reflect(args: argparse.Namespace) -> None:
    from google import genai
    from google.genai import types

    api_key_g = os.getenv("GEMINI_API_KEY")
    if not api_key_g:
        raise SystemExit("GEMINI_API_KEY missing in .env")

    candidates = read_jsonl(CANDIDATE_HISTORY)
    posts = read_jsonl(POST_HISTORY)
    if not candidates:
        raise SystemExit("candidate-history.jsonl is empty — call log-candidate after planning at least once")
    if not posts:
        raise SystemExit("post-history.jsonl is empty — publish some carousels first")

    cutoff = datetime.now().timestamp() - args.window_days * 86400

    def in_window(rec: dict, key: str) -> bool:
        try:
            return datetime.fromisoformat(rec[key]).timestamp() >= cutoff
        except (KeyError, ValueError):
            return False

    recent_candidates = [c for c in candidates if in_window(c, "logged_at")]
    recent_posts = [p for p in posts if in_window(p, "published_at")]
    published_ids = {p.get("candidate_id") for p in recent_posts}

    approved = [c for c in recent_candidates if c.get("candidate_id") in published_ids]
    rejected = [c for c in recent_candidates if c.get("candidate_id") not in published_ids]

    log(f"[reflect] window {args.window_days}d: {len(approved)} approved-unchanged, "
        f"{len(rejected)} edited/rejected, {len(recent_posts)} total posts")

    if not recent_candidates:
        raise SystemExit(f"no candidates in last {args.window_days} days")
    if not (approved and rejected) and not recent_posts:
        raise SystemExit("need either approved+rejected candidates OR posts in window")

    def short(c: dict) -> dict:
        return {
            "product_name": c.get("product_name"),
            "category": c.get("category"),
            "hook_text": c.get("hook_text"),
            "image_prompts": c.get("image_prompts"),
            "slide_count": c.get("slide_count"),
        }

    full_prompt = (
        REFLECT_PROMPT
        + "\n\n## CANDIDATES (initial agent proposals)\n"
        + json.dumps([short(c) for c in recent_candidates], ensure_ascii=False, indent=2)
        + "\n\n## PUBLISHED (final carousels that shipped)\n"
        + json.dumps([short(p) for p in recent_posts], ensure_ascii=False, indent=2)
    )

    client = genai.Client(api_key=api_key_g)
    log(f"  calling {GEMINI_TEXT_MODEL}…")
    resp = client.models.generate_content(
        model=GEMINI_TEXT_MODEL,
        contents=[full_prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    try:
        data = json.loads(resp.text)
    except (json.JSONDecodeError, TypeError):
        raise SystemExit(f"Gemini returned non-JSON: {(resp.text or '')[:300]}")

    now = datetime.now()
    run_path = RUNS_FOLDER / f"reflect-{now.strftime('%Y-%m-%d-%H%M')}.md"
    run_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Reflect run — {now.isoformat(timespec='seconds')}",
        "",
        f"- window: last {args.window_days} days",
        f"- approved-unchanged: {len(approved)} / edited-or-rejected: {len(rejected)}",
        f"- posts in window: {len(recent_posts)}",
        "",
        "## Hook observations (NOT auto-promoted to HOT_HOOKS.md — read and curate)",
        "",
    ]
    for o in data.get("hook_observations") or []:
        lines.append(f"- **{o.get('rule')}** — {o.get('evidence')}")
    lines += ["", "## Imagery observations (NOT auto-promoted to HOT_IMAGERY.md — read and curate)", ""]
    for o in data.get("imagery_observations") or []:
        lines.append(f"- **{o.get('rule')}** — {o.get('evidence')}")
    run_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"[reflect] {len(data.get('hook_observations') or [])} hook + "
        f"{len(data.get('imagery_observations') or [])} imagery observations → {run_path}")
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ========== CLI ==========

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="autoecom")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("download", help="download a URL to a local path")
    s.add_argument("url")
    s.add_argument("out", help="output file path")
    s.set_defaults(func=cmd_download)

    s = sub.add_parser("palette", help="extract dominant hex colors from an image")
    s.add_argument("image", help="path to image file")
    s.add_argument("--n", type=int, default=5)
    s.set_defaults(func=cmd_palette)

    s = sub.add_parser("product", help="parse a product page's JSON-LD into a dict")
    s.add_argument("url")
    s.set_defaults(func=cmd_product)

    s = sub.add_parser("generate", help="nano-banana → raw stylized images per slide")
    s.add_argument("plan", help="path to plan.json")
    s.add_argument("--force", action="store_true", help="regenerate slides even if already cached")
    s.set_defaults(func=cmd_generate)

    s = sub.add_parser("compose", help="Pillow overlay → final 1080x1350 carousel slides")
    s.add_argument("plan", help="path to plan.json")
    s.set_defaults(func=cmd_compose)

    s = sub.add_parser("publish", help="Upload-Post carousel to IG + TikTok")
    s.add_argument("plan", help="path to plan.json")
    s.add_argument("--platforms", default="instagram,tiktok",
                   help="comma-separated: instagram, tiktok")
    s.add_argument("--tiktok-mode", default="draft", choices=["draft", "direct"],
                   help="TikTok upload mode (default: draft, never auto-publishes)")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(func=cmd_publish)

    s = sub.add_parser("mark-processed", help="record that a product URL was just published")
    s.add_argument("url")
    s.add_argument("--slides", type=int, default=0)
    s.add_argument("--store", help="record/update the store URL on the state file")
    s.set_defaults(func=cmd_mark_processed)

    s = sub.add_parser("list-processed", help="dump processed.json to stdout")
    s.set_defaults(func=cmd_list_processed)

    s = sub.add_parser("new-cycle", help="manually start a new cycle (admin)")
    s.set_defaults(func=cmd_new_cycle)

    s = sub.add_parser("priors", help="dump current HOT_HOOKS.md + HOT_IMAGERY.md as JSON")
    s.set_defaults(func=cmd_priors)

    s = sub.add_parser("log-candidate",
                       help="append the agent's INITIAL plan proposal to candidate-history.jsonl")
    s.add_argument("plan", help="path to plan.json")
    s.set_defaults(func=cmd_log_candidate)

    s = sub.add_parser("learn",
                       help="weekly: pull Upload-Post analytics, refresh HOT_HOOKS.md + HOT_IMAGERY.md")
    s.add_argument("--soak-days", type=int, default=7,
                   help="ignore carousels younger than this (analytics not mature)")
    s.add_argument("--max-age-days", type=int, default=90,
                   help="ignore carousels older than this (stale)")
    s.add_argument("--top-pct", type=float, default=0.20)
    s.add_argument("--bottom-pct", type=float, default=0.20)
    s.add_argument("--weight-views", type=float, default=0.6)
    s.add_argument("--weight-engagement", type=float, default=0.4)
    s.add_argument("--min-cohort", type=int, default=7,
                   help="minimum total carousels with analytics to run synthesis")
    s.add_argument("--min-per-bucket", type=int, default=3,
                   help="minimum winners and minimum losers per bucket")
    s.set_defaults(func=cmd_learn)

    s = sub.add_parser("reflect",
                       help="qualitative pass: compare candidates vs published, emit observations")
    s.add_argument("--window-days", type=int, default=30)
    s.set_defaults(func=cmd_reflect)

    return p


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
