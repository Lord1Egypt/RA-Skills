#!/usr/bin/env python3
"""Build an html-cart lookbook deploy directory from a config + picks file.

Inputs (CLI):
  --config        path to lookbook config JSON (see schema below)
  --picks         path to picks JSON (one entry per piece; produced by the
                  agent fetching /mcp/buckmason/products/<id> + imagery)
  --look-images   directory containing look<N>.png try-on images
                  (skip when --no-tryon — falls back to editorial tier)
  --out           output directory; will contain index.html + look*.jpg +
                  thumb-*.jpg + og.jpg
  --no-tryon      build the editorial tier (no try-on images, just product
                  imagery laid out per look)

Config JSON shape:
  {
    "lookbook_id":    "2026-05-09-la-mellow",
    "lookbook_title": "Two Looks for a Mellow LA Weekend",
    "lookbook_date":  "2026-05-09",
    "subtitle":       "Saturday on Abbot Kinney, Sunday sunset on Venice...",
    "page_url":       "https://buckmason-lookbook.pages.dev/",
    "looks": [
      { "id": "look1", "eyebrow": "Look 01", "title": "Saturday on Abbot Kinney",
        "note": "Coffee, books, the kind of mid-morning..." },
      { "id": "look2", "eyebrow": "Look 02", "title": "Sunday Sunset...",
        "note": "..." }
    ]
  }

Picks JSON shape (one per piece):
  [
    { "look": "look1", "picked_size": "L", "id": 10543,
      "name": "Natural Draped Linen Deuce Coupe Camp Shirt",
      "color": "Natural", "price": "$168.00", "price_cents": 16800,
      "url": "https://www.buckmason.com/products/...",
      "sku": "BM13211.679NATL",
      "in_stock_online": { "label": "In stock", ... },
      "try_on": { "url": "..." } | null,
      "hero":   { "url": "..." } | null, ... }
  ]

The script is deterministic: same inputs → same outputs (modulo the gpt-image-2
PNGs, which are produced separately and supplied via --look-images).
"""
import argparse, html, json, pathlib, subprocess, sys
# Pillow is imported lazily inside the functions that need it — keeps
# `--help` discoverable without requiring the optional dep installed.
# (CI's scripts-help job + downstream agents that just want to read
#  usage shouldn't have to `pip install Pillow` first.)

# ── Inputs ───────────────────────────────────────────────────────────────────

ap = argparse.ArgumentParser(description="Build an html-cart lookbook deploy directory.")
ap.add_argument("--config",      required=True, type=pathlib.Path)
ap.add_argument("--picks",       required=True, type=pathlib.Path)
ap.add_argument("--look-images", type=pathlib.Path, help="Directory with look<N>.png try-on images. Required unless --no-tryon.")
ap.add_argument("--out",         required=True, type=pathlib.Path)
ap.add_argument("--no-tryon",    action="store_true", help="Editorial tier — use product imagery for look heroes.")
args = ap.parse_args()

CFG   = json.loads(args.config.read_text())
PICKS = json.loads(args.picks.read_text())
OUT   = args.out
OUT.mkdir(parents=True, exist_ok=True)

if not args.no_tryon and not args.look_images:
    print("error: --look-images required unless --no-tryon", file=sys.stderr)
    sys.exit(2)

LOOKBOOK_ID    = CFG["lookbook_id"]

# ── Per-lookbook isolation check (references/run-layout.md) ─────────────────
# If --look-images carries a .lookbook_id marker, refuse to consume it when
# it doesn't match this run's lookbook_id. Missing marker = warn-only (manual
# or curated images don't always have one).
if args.look_images:
    marker = args.look_images / ".lookbook_id"
    if marker.exists():
        prior = marker.read_text().strip()
        if prior != LOOKBOOK_ID:
            print(
                f"error: --look-images directory has .lookbook_id {prior!r}\n"
                f"       but the config is for {LOOKBOOK_ID!r}.\n"
                f"       Either generate fresh look images for this lookbook (Premium tier),\n"
                f"       skip them with --no-tryon (Editorial tier), or fix the path.",
                file=sys.stderr,
            )
            sys.exit(5)
    else:
        print(
            f"warn: --look-images at {args.look_images} has no .lookbook_id marker — "
            f"can't verify these are this run's images. See references/run-layout.md.",
            file=sys.stderr,
        )
LOOKBOOK_TITLE = CFG["lookbook_title"]
LOOKBOOK_DATE  = CFG["lookbook_date"]
SUBTITLE       = CFG.get("subtitle", "")
PAGE_URL       = CFG["page_url"].rstrip("/") + "/"
OG_IMAGE_URL   = PAGE_URL + "og.jpg"

# ── Asset prep ───────────────────────────────────────────────────────────────
# Lazy-import Pillow at first actual use so `--help` works without the dep.
from PIL import Image  # noqa: E402

def web_jpeg(src, dst, max_w=1200, quality=85):
    img = Image.open(src).convert("RGB")
    if img.width > max_w:
        h = round(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.LANCZOS)
    img.save(dst, "JPEG", quality=quality, optimize=True)

def thumb(src_url, dst, w=240):
    if dst.exists() and dst.stat().st_size > 0:
        return
    tmp = dst.with_suffix(".tmp")
    subprocess.run(["curl", "-sSL", "-o", str(tmp), src_url], check=True)
    img = Image.open(tmp).convert("RGB")
    h = round(w * 4 / 3)
    ratio = max(w / img.width, h / img.height)
    new = img.resize((round(img.width * ratio), round(img.height * ratio)), Image.LANCZOS)
    left = (new.width - w) // 2
    top  = (new.height - h) // 2
    new.crop((left, top, left + w, top + h)).save(dst, "JPEG", quality=85, optimize=True)
    tmp.unlink()

# Build the per-look hero image
look_hero = {}   # look_id -> filename relative to OUT
for look in CFG["looks"]:
    look_id = look["id"]
    if args.no_tryon:
        # Editorial tier: use the first piece's hero image as the cover for the look.
        # Pieces may carry imagery as either a structured try_on/hero object
        # (from /products/:id/imagery) or just an image_url string (from the
        # /products list endpoint, which is what discover-weekly-candidates
        # emits). Fall through both shapes.
        pieces = [p for p in PICKS if p["look"] == look_id]
        if not pieces:
            continue
        p0 = pieces[0]
        src_url = ((p0.get("try_on") or {}).get("url")
                   or (p0.get("hero") or {}).get("url")
                   or p0.get("image_url"))
        if not src_url:
            print(f"warn: no hero image for {look_id}", file=sys.stderr)
            continue
        dst = OUT / f"{look_id}.jpg"
        if not dst.exists():
            tmp = dst.with_suffix(".tmp")
            subprocess.run(["curl", "-sSL", "-o", str(tmp), src_url], check=True)
            web_jpeg(tmp, dst, max_w=1200)
            tmp.unlink()
        look_hero[look_id] = dst.name
    else:
        src = args.look_images / f"{look_id}.png"
        if not src.exists():
            print(f"error: missing try-on image: {src}", file=sys.stderr)
            sys.exit(2)
        dst = OUT / f"{look_id}.jpg"
        web_jpeg(src, dst, max_w=1200)
        look_hero[look_id] = dst.name

# Per-piece thumbnails
for p in PICKS:
    src_url = ((p.get("try_on") or {}).get("url")
               or (p.get("hero") or {}).get("url")
               or p.get("image_url"))
    if not src_url:
        continue
    p["thumb_path"] = f"thumb-{p['id']}.jpg"
    thumb(src_url, OUT / p["thumb_path"], w=240)

# og.jpg — preserve the hero's native aspect ratio (do NOT letterbox onto a
# 1200×630 landscape canvas). Portrait/square OG images render as the "tall"
# image-dominant card in iMessage/Apple Messages, filling the bubble width;
# a portrait subject pasted into a landscape canvas produces a centered photo
# with white side-bars, which is the broken-looking variant. Fit the longest
# side to 1200px (FB recommends ≥1200px on the wide axis).
OG_W, OG_H = 1200, 630   # fallback if there's no hero (legacy default)
first_look_id = CFG["looks"][0]["id"] if CFG.get("looks") else None
hero_name = look_hero.get(first_look_id) if first_look_id else None
cover_src = (OUT / hero_name) if hero_name else None
if cover_src and cover_src.is_file():
    cover = Image.open(cover_src).convert("RGB")
    ratio = 1200 / max(cover.width, cover.height)
    OG_W, OG_H = int(cover.width * ratio), int(cover.height * ratio)
    cover.resize((OG_W, OG_H), Image.LANCZOS).save(
        OUT / "og.jpg", "JPEG", quality=85, optimize=True
    )

# ── HTML render ──────────────────────────────────────────────────────────────

def fullsize_url(p):
    return ((p.get("hero") or {}).get("url")
            or (p.get("try_on") or {}).get("url")
            or p.get("image_url")
            or "")

def stock_line(p):
    online = p.get("in_stock_online") or {}
    label = online.get("label", "—") if isinstance(online, dict) else str(online)
    return f"Size {html.escape(p['picked_size'])} · {html.escape(label)}"

def fmt_money(cents):
    return f"${cents/100:.2f}".rstrip("0").rstrip(".")

def look_section(look):
    look_id = look["id"]
    pieces = [p for p in PICKS if p["look"] == look_id]
    if not pieces:
        return ""
    subtotal_cents = sum(p["price_cents"] for p in pieces)
    pieces_html = "\n".join(
        f'''        <label class="piece" for="cb-{look_id}-{i}">
          <input type="checkbox" id="cb-{look_id}-{i}"
                 data-name="{html.escape(p["name"])}"
                 data-size="{html.escape(p["picked_size"])}"
                 data-sku="{html.escape(p["sku"] or "")}"
                 data-qty="1"
                 data-price-cents="{p["price_cents"]}"
                 data-url="{html.escape(p["url"])}">
          <img src="{html.escape(p.get("thumb_path", ""))}" data-fullsize="{html.escape(fullsize_url(p))}" alt="{html.escape(p["name"])}">
          <div class="piece-info">
            <div class="name">{html.escape(p["name"])}</div>
            <div class="price">${p["price_cents"]/100:.2f}</div>
            <a href="{html.escape(p["url"])}" target="_blank" rel="noopener">View on buckmason.com</a>
            <div class="stock">{stock_line(p)}</div>
          </div>
        </label>'''
        for i, p in enumerate(pieces)
    )
    hero_src = look_hero.get(look_id, "")
    return f'''<section class="look" data-look="{look_id}">
      <div class="look-hero">
        <img src="{hero_src}" data-fullsize="{hero_src}" alt="Buck Mason lookbook — {html.escape(look['title'])}">
      </div>
      <div class="look-pieces">
        <div class="eyebrow">{html.escape(look['eyebrow'])}</div>
        <h2>{html.escape(look['title'])}</h2>
        <p class="note">{html.escape(look['note'])}</p>
{pieces_html}
        <div class="total">Look subtotal · {fmt_money(subtotal_cents)}</div>
        <button type="button" class="bm-btn-outline select-outfit" data-target-look="{look_id}" onclick="toggleLook('{look_id}', this)">Select this outfit</button>
      </div>
    </section>'''

ai_disclosure = (
    "AI-generated try-on previews — not photographs of real garments on the customer."
    if not args.no_tryon
    else "Editorial tier — product imagery from buckmason.com, no AI try-on."
)

PAGE = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(LOOKBOOK_TITLE)} · Buck Mason</title>
  <meta name="description" content="{html.escape(SUBTITLE)}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Buck Mason">
  <meta property="og:title" content="{html.escape(LOOKBOOK_TITLE)}">
  <meta property="og:description" content="{html.escape(SUBTITLE)}">
  <meta property="og:url" content="{PAGE_URL}">
  <meta property="og:image" content="{OG_IMAGE_URL}">
  <meta property="og:image:width" content="{OG_W}">
  <meta property="og:image:height" content="{OG_H}">
  <meta property="og:image:alt" content="Buck Mason lookbook — {html.escape(LOOKBOOK_TITLE)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(LOOKBOOK_TITLE)}">
  <meta name="twitter:description" content="{html.escape(SUBTITLE)}">
  <meta name="twitter:image" content="{OG_IMAGE_URL}">

  <style>
    :root {{
      --bm-cond: "Acumin Pro Condensed", "Helvetica Neue Condensed", "Helvetica Neue", Helvetica, Arial, sans-serif;
      --bm-body: "Acumin Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
      --bm-ink: #333; --bm-mute: #666; --bm-faint: #999; --bm-line: #e5e2dd; --bm-accent: #f3f1ef;
    }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: var(--bm-body); color: var(--bm-ink); background: #fff; margin: 0; font-size: 14px; line-height: 1.5; }}
    a {{ color: var(--bm-mute); }}
    .eyebrow {{ font-family: var(--bm-cond); font-size: 11px; letter-spacing: 0.02em; text-transform: uppercase; color: var(--bm-mute); }}
    h1 {{ font-family: var(--bm-cond); font-weight: 600; font-size: 22px; line-height: 1; letter-spacing: 0.02em; text-transform: uppercase; margin: 8px 0 12px; color: var(--bm-ink); }}
    h2 {{ font-family: var(--bm-cond); font-weight: 600; font-size: 20px; line-height: 1; letter-spacing: 0.02em; text-transform: uppercase; margin: 8px 0 12px; color: var(--bm-ink); }}
    p.note {{ color: var(--bm-mute); margin: 0 0 24px; }}
    .page {{ max-width: 1200px; margin: 0 auto; padding: 64px 32px 120px; }}
    .cover {{ text-align: left; padding-bottom: 16px; }}
    .cover .meta {{ color: var(--bm-faint); font-size: 12px; margin-top: 12px; }}
    .look {{ display: grid; grid-template-columns: 5fr 4fr; gap: 48px; padding: 64px 0; }}
    .look-hero img {{ width: 100%; aspect-ratio: 3/4; object-fit: cover; display: block; }}
    .look-pieces {{ display: flex; flex-direction: column; gap: 0; }}
    .piece {{ display: grid; grid-template-columns: 24px 88px 1fr; gap: 16px; align-items: start; padding: 18px 0; border-top: 1px solid var(--bm-line); cursor: pointer; }}
    .piece:first-of-type {{ border-top: 1px solid var(--bm-ink); }}
    .piece input[type="checkbox"] {{ width: 16px; height: 16px; margin-top: 4px; appearance: none; -webkit-appearance: none; border: 1px solid var(--bm-ink); cursor: pointer; position: relative; flex-shrink: 0; }}
    .piece input[type="checkbox"]:checked {{ background: var(--bm-ink); }}
    .piece input[type="checkbox"]:checked::after {{ content: ""; position: absolute; left: 4px; top: 0; width: 4px; height: 10px; border: solid #fff; border-width: 0 2px 2px 0; transform: rotate(45deg); }}
    .piece img {{ width: 88px; aspect-ratio: 3/4; object-fit: cover; display: block; background: #fafafa; }}
    .piece-info {{ display: flex; flex-direction: column; gap: 4px; }}
    .piece .name {{ font-family: var(--bm-cond); font-weight: 600; font-size: 13px; letter-spacing: 0.02em; text-transform: uppercase; }}
    .piece .price {{ font-size: 14px; }}
    .piece a {{ font-size: 11px; }}
    .piece .stock {{ font-size: 11px; color: var(--bm-mute); }}
    .total {{ font-family: var(--bm-cond); font-weight: 700; font-size: 13px; letter-spacing: 0.02em; text-transform: uppercase; padding-top: 18px; margin-top: 18px; border-top: 1px solid var(--bm-ink); }}
    .bm-btn-outline {{ display: inline-block; font-family: var(--bm-cond); font-weight: 600; font-size: 12px; letter-spacing: 0.02em; text-transform: uppercase; color: var(--bm-ink); background: transparent; border: 1px solid var(--bm-ink); padding: 12px 20px; min-height: 44px; cursor: pointer; transition: background 120ms, color 120ms; }}
    .bm-btn-outline:hover {{ background: var(--bm-ink); color: #fff; }}
    .bm-btn-outline.selected {{ background: var(--bm-ink); color: #fff; }}
    .bm-btn-outline.selected::before {{ content: "✓ "; }}
    #select-all-btn {{ margin-top: 16px; }}
    .select-outfit {{ margin-top: 20px; align-self: flex-start; }}
    .footer {{ text-align: center; font-family: var(--bm-cond); font-size: 11px; letter-spacing: 0.02em; text-transform: uppercase; color: var(--bm-faint); padding: 48px 0 0; }}
    @media (max-width: 1023px) and (min-width: 700px) {{
      .page {{ padding: 48px 32px 120px; }}
      .look {{ grid-template-columns: 1fr; gap: 24px; padding: 48px 0; }}
      .piece {{ grid-template-columns: 24px 96px 1fr; }}
      .piece img {{ width: 96px; }}
    }}
    @media (max-width: 699px) {{
      body {{ font-size: 13px; }}
      .page {{ padding: 32px 16px 120px; }}
      .look {{ grid-template-columns: 1fr; gap: 16px; padding: 32px 0; }}
      .piece {{ grid-template-columns: 22px 64px 1fr; gap: 12px; padding: 16px 0; }}
      .piece img {{ width: 64px; }}
      h1 {{ font-size: 20px; }}
      h2 {{ font-size: 18px; }}
      .footer {{ padding-top: 32px; }}
    }}
    #cart-bar {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--bm-ink); color: #fff; padding: 16px 32px; display: none; align-items: center; justify-content: space-between; gap: 16px; font-family: var(--bm-cond); font-size: 12px; letter-spacing: 0.02em; text-transform: uppercase; z-index: 5; }}
    #cart-bar.show {{ display: flex; }}
    #cart-bar button {{ background: #fff; color: var(--bm-ink); border: 0; padding: 14px 24px; font: inherit; letter-spacing: 0.02em; cursor: pointer; min-height: 44px; }}
    @media (max-width: 699px) {{ #cart-bar {{ padding: 12px 16px; font-size: 10px; }} #cart-bar button {{ padding: 12px 16px; font-size: 10px; }} }}
    #handoff {{ display: none; position: fixed; inset: 32px; background: #fff; z-index: 10; padding: 32px; overflow: auto; box-shadow: 0 0 60px rgba(0,0,0,.25); }}
    #handoff.show {{ display: block; }}
    #handoff h2 {{ margin-top: 0; }}
    #handoff p {{ color: var(--bm-mute); }}
    #handoff pre {{ background: var(--bm-accent); border: 0; padding: 16px; font-size: 12px; line-height: 1.5; white-space: pre-wrap; word-break: break-all; max-height: 50dvh; overflow: auto; }}
    #handoff .actions {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    #handoff button {{ font-family: var(--bm-cond); letter-spacing: 0.02em; text-transform: uppercase; font-size: 11px; cursor: pointer; min-height: 44px; padding: 12px 24px; }}
    #handoff .primary {{ background: var(--bm-ink); color: #fff; border: 0; }}
    #handoff .secondary {{ background: transparent; color: var(--bm-ink); border: 1px solid var(--bm-ink); }}
    @media (max-width: 699px) {{ #handoff {{ inset: 12px; padding: 20px; }} }}
    .look-hero img, .piece img {{ cursor: zoom-in; }}
    #lightbox {{ position: fixed; inset: 0; background: rgba(0,0,0,0.94); display: none; align-items: center; justify-content: center; z-index: 20; padding: 32px; cursor: zoom-out; }}
    #lightbox.show {{ display: flex; }}
    #lightbox img {{ max-width: min(100%, 1600px); max-height: 100%; object-fit: contain; cursor: default; display: block; }}
    #lightbox .close {{ position: absolute; top: 12px; right: 12px; background: transparent; color: #fff; border: 0; font: 24px/1 var(--bm-cond); cursor: pointer; padding: 12px 16px; min-height: 44px; min-width: 44px; }}
    @media (max-width: 699px) {{ #lightbox {{ padding: 12px; }} }}
  </style>
</head>
<body>
  <div class="page">
    <header class="cover">
      <div class="eyebrow">Buck Mason · Stylist · {html.escape(LOOKBOOK_ID)}</div>
      <h1>{html.escape(LOOKBOOK_TITLE)}</h1>
      <p class="note">{html.escape(SUBTITLE)}</p>
      <button type="button" id="select-all-btn" class="bm-btn-outline" onclick="toggleAll(this)">Select all looks</button>
      <div class="meta">{html.escape(ai_disclosure)}</div>
    </header>
    {"".join(look_section(l) for l in CFG["looks"])}
    <div class="footer">Buck Mason · Pima.io · Stylist Skill</div>
  </div>

  <div id="cart-bar">
    <span><span id="cart-count">0</span> selected · <span id="cart-total">$0</span></span>
    <button onclick="openHandoff()">Send to my stylist</button>
  </div>

  <div id="handoff" role="dialog" aria-modal="true" aria-labelledby="handoff-title">
    <h2 id="handoff-title">Tell your stylist</h2>
    <p>Speak this aloud to a voice agent, or paste it into a chat. Your agent will confirm shipping or pickup, coupon, and credit before charging.</p>
    <pre id="handoff-text"></pre>
    <div class="actions">
      <button id="copy-btn" class="primary" onclick="copyHandoff(this)">Copy to clipboard</button>
      <button class="secondary" onclick="closeHandoff()">Close</button>
    </div>
  </div>

  <div id="lightbox" onclick="closeLightbox(event)">
    <button class="close" type="button" aria-label="Close image" onclick="closeLightbox(event, true)">×</button>
    <img id="lightbox-img" alt="">
  </div>

  <script>
    const LOOKBOOK_ID    = {json.dumps(LOOKBOOK_ID)};
    const LOOKBOOK_TITLE = {json.dumps(LOOKBOOK_TITLE)};
    const LOOKBOOK_DATE  = {json.dumps(LOOKBOOK_DATE)};
    function selected() {{
      return [...document.querySelectorAll('.piece input[type="checkbox"]:checked')].map(el => ({{
        name: el.dataset.name, size: el.dataset.size,
        qty:  parseInt(el.dataset.qty, 10),
        cents:parseInt(el.dataset.priceCents, 10),
      }}));
    }}
    function fmtMoney(c) {{ return '$' + (c / 100).toFixed(c % 100 === 0 ? 0 : 2); }}
    function refresh() {{
      const items = selected();
      const cents = items.reduce((a, i) => a + i.cents * i.qty, 0);
      document.getElementById('cart-count').textContent = items.length;
      document.getElementById('cart-total').textContent = '$' + (cents / 100).toFixed(2);
      document.getElementById('cart-bar').classList.toggle('show', items.length > 0);
    }}
    function buildHandoffText() {{
      const items = selected();
      if (items.length === 0) return '';
      const subtotal = items.reduce((a, i) => a + i.cents * i.qty, 0);
      const lines = items.map(i => {{
        const qtyPart = i.qty > 1 ? ` (×${{i.qty}})` : '';
        return `• ${{i.name}} — size ${{i.size}} — ${{fmtMoney(i.cents)}}${{qtyPart}}`;
      }});
      return [
        `Buck Mason — ${{LOOKBOOK_TITLE}} (${{LOOKBOOK_DATE}})`,
        '',
        `I'd like to order:`,
        ...lines,
        '',
        `Subtotal at pick: ${{fmtMoney(subtotal)}}`,
        `Please confirm shipping or pickup, any coupon or credit, and run checkout.`,
      ].join('\\n');
    }}
    function openHandoff() {{
      document.getElementById('handoff-text').textContent = buildHandoffText();
      document.getElementById('handoff').classList.add('show');
    }}
    function closeHandoff() {{ document.getElementById('handoff').classList.remove('show'); }}
    let copyResetTimer = null;
    async function copyHandoff(btn) {{
      try {{
        await navigator.clipboard.writeText(document.getElementById('handoff-text').textContent);
      }} catch (e) {{
        const r = document.createRange(); r.selectNode(document.getElementById('handoff-text'));
        getSelection().removeAllRanges(); getSelection().addRange(r);
        document.execCommand('copy'); getSelection().removeAllRanges();
      }}
      btn.dataset.original = btn.dataset.original || btn.textContent;
      btn.textContent = '✓ Copied'; btn.disabled = true;
      clearTimeout(copyResetTimer);
      copyResetTimer = setTimeout(() => {{ btn.textContent = btn.dataset.original; btn.disabled = false; }}, 1800);
    }}
    document.addEventListener('change', e => {{
      if (e.target.matches('.piece input[type="checkbox"]')) {{ refresh(); refreshSelectButtons(); }}
    }});

    function lookCheckboxes(lookId) {{ return [...document.querySelectorAll(`.look[data-look="${{lookId}}"] .piece input[type="checkbox"]`)]; }}
    function allCheckboxes()        {{ return [...document.querySelectorAll('.piece input[type="checkbox"]')]; }}
    function toggleLook(lookId, btn) {{
      const boxes = lookCheckboxes(lookId);
      const allChecked = boxes.length > 0 && boxes.every(b => b.checked);
      boxes.forEach(b => {{ b.checked = !allChecked; }});
      refresh(); refreshSelectButtons();
    }}
    function toggleAll(btn) {{
      const boxes = allCheckboxes();
      const allChecked = boxes.length > 0 && boxes.every(b => b.checked);
      boxes.forEach(b => {{ b.checked = !allChecked; }});
      refresh(); refreshSelectButtons();
    }}
    function refreshSelectButtons() {{
      document.querySelectorAll('.select-outfit').forEach(btn => {{
        const boxes = lookCheckboxes(btn.dataset.targetLook);
        const allChecked = boxes.length > 0 && boxes.every(b => b.checked);
        btn.classList.toggle('selected', allChecked);
        btn.textContent = allChecked ? 'Outfit selected' : 'Select this outfit';
      }});
      const allBtn = document.getElementById('select-all-btn');
      if (allBtn) {{
        const all = allCheckboxes();
        const everySelected = all.length > 0 && all.every(b => b.checked);
        allBtn.classList.toggle('selected', everySelected);
        allBtn.textContent = everySelected ? 'Deselect all' : 'Select all looks';
      }}
    }}

    function openLightbox(src, alt) {{
      const lb = document.getElementById('lightbox');
      const img = document.getElementById('lightbox-img');
      img.src = src; img.alt = alt || '';
      lb.classList.add('show');
      document.body.style.overflow = 'hidden';
    }}
    function closeLightbox(ev, force) {{
      if (!force && ev && ev.target && ev.target.id === 'lightbox-img') return;
      document.getElementById('lightbox').classList.remove('show');
      document.body.style.overflow = '';
    }}
    document.addEventListener('click', e => {{
      const img = e.target.closest('.look-hero img, .piece img');
      if (img) {{
        e.preventDefault(); e.stopPropagation();
        openLightbox(img.dataset.fullsize || img.src, img.alt);
      }}
    }}, true);
    document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeLightbox(null, true); }});
  </script>
</body>
</html>
'''

(OUT / "index.html").write_text(PAGE)

# Stamp the run marker so deploy/validate steps can verify provenance.
(OUT / ".lookbook_id").write_text(LOOKBOOK_ID + "\n")

# Sanity-print
files = sorted(f for f in OUT.glob("*") if not f.name.startswith("."))
for f in files:
    print(f"  {f.name:48}  {f.stat().st_size:>10,} bytes")
print(f"\nwrote {len(files)} files to {OUT} (lookbook_id={LOOKBOOK_ID})")
