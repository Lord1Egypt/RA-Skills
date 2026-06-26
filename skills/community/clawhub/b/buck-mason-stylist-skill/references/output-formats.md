# Lookbook output formats

Four supported outputs from the lookbook workflow (`SKILL.md` workflow 3, step 4):

| Format | Build time | Best for |
|---|---|---|
| `images` (PNG only) | ~0s after generation | Quick iteration, "just show me" |
| `ppt` (`.pptx`) | ~2s | Sharing for review (stylist, SO, yourself) |
| `html` (`.html`) | ~1s | Public preview link, email body, browser sharing |
| `html-cart` (`.html`, interactive) | ~1s | Customer picks items from the lookbook → structured handoff back to the stylist agent → MPP checkout (no Shopify redirect) |

For an unqualified customer request that says "lookbook," default to the hosted path: Premium gpt-image-2 virtual try-on imagery inside `html` or `html-cart`, then Cloudflare Pages deploy with the voting mechanism enabled. `images` and `ppt` are explicit-format outputs; `html` becomes read-only only when the customer asks for no cart affordance, and voting is suppressed only with an explicit read-only / `--no-voting` request.

Every format MUST include, per piece:
1. Product name
2. Price (USD with `$`)
3. Clickable `buckmason.com/products/<slug>` link
4. In-your-size stock per location, bucketed: `In stock` / `Low (N)` / `Out of stock`
5. Per-look total at the bottom of each look

Identity disclosure ("AI-generated try-on preview, not a real photo of you in the garment") goes on the cover or the footer of the deck/page.

---

## 1. `images` — raw PNGs

Just the files written by the OpenAI image-edit calls. No assembly. Output to `lookbook/<date>-<event>-look-N.png`. List the file paths back to the customer with the per-piece info as plain markdown:

```
Look 01 — Mediterranean Evening
   lookbook/2026-04-26-sonoma-look-1.png

   • Brown / Natural Gun Club Graduate Jacket — $698 — In stock
     https://www.buckmason.com/products/brown-natural-gun-club-graduate-jacket
   • Faded Indigo Como Cashmere Polo — $168 — In stock
     https://www.buckmason.com/products/faded-indigo-como-cashmere-polo
   • Chocolate Irish Linen Hollywood Pleated Trouser — $298 — Low (1)
     https://www.buckmason.com/products/chocolate-irish-linen-hollywood-pleated-trouser

   Look 01 total: $1,164
```

---

## 2. `ppt` — `.pptx` slide deck

Build with `python-pptx`. 16:9 widescreen (`13.333" × 7.5"`). One slide per look + one cover slide.

**Read `references/brand-style.md` before building.** It contains the python-pptx mapping for every brand rule (font names, RGB values, headline sizes, image ratios). The two highest-leverage rules: **headlines stay small (20pt, not 36pt+)** and **product imagery is 3:4 portrait** (`Inches(4.5), Inches(6.0)`) even on a 16:9 slide.

### Required Python deps
```
python-pptx
Pillow
```

### Slide layout
- **Cover slide**: white background, brand eyebrow (Acumin Pro Condensed 11pt uppercase #666), title (Acumin Pro Condensed 20pt 600 #333), one-line subtitle, list of featured anchor pieces with names + prices + clickable links, "Stores near 90291" block.
- **Per-look slide**: `LOOK 01` eyebrow, title (Acumin Pro Condensed, 20pt, uppercase, #333), one-sentence occasion note, generated look image on the left at 3:4 portrait (4.5"×6.0"), per-piece rows on the right (1.4"×1.87" thumbnails + name + price + clickable link + stock line), per-look total at the bottom. **No dividers between sections** — whitespace + the eyebrow label do the job.

### Clickable hyperlinks — non-negotiable
Every URL on the deck MUST be a real hyperlink. In `python-pptx`:

```python
run = paragraph.add_run()
run.text = "buckmason.com/products/..."
run.hyperlink.address = "https://www.buckmason.com/products/..."
```

PowerPoint and Keynote do NOT auto-detect plain URL text — without `run.hyperlink.address` the link is dead.

### Stock-line format
```
Size L — Online: In stock  ·  Abbot Kinney: Low (5)  ·  Century City: Out  ·  Bloomies CC: Low (3)
```

The bucket thresholds and labels come from the same logic as `/mcp/buckmason/stock/:sku`:
- `0` → `Out of stock` (or just `Out` for compact display)
- `1–9` → `Low (N)`
- `10+` → `In stock` (no exact count surfaced)

### Reference implementation
A working `python-pptx` builder is shipped in the test-output / dev fixtures of this repo's history — search for `build-outfit*-deck.py`. Reuse its `cover_slide()` and `look_slide()` functions; only the data inputs change between lookbooks.

---

## 3. `html` — single self-contained `.html`

Build with a string template — no framework needed. Single file, ~30 KB before image embedding, ~3–8 MB with images embedded as base64.

### Why self-contained
- Works offline (no broken images when the customer airdrops it to themselves)
- Single attachment in email
- Trivial to host (any static host accepts it)
- Survives moving between devices without breaking image paths

### Layout
Vertical scroll: cover section → one section per look. Same content as the PPT but in a single document. Mobile-responsive: the per-piece grid collapses to a single column under 700px.

### Skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Three Looks for Sonoma · Buck Mason</title>
  <meta name="description" content="An editorial styling for a May wedding weekend, by Buck Mason.">

  <!-- Social preview (Open Graph + Twitter Card).
       Required so iMessage/Slack/Discord/Twitter render a hero image when the
       URL is pasted. og:image and og:url MUST be absolute URLs — see
       references/hosting-options.md § "Social-preview meta tags" for how the
       absolute URLs get resolved per transport. -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Buck Mason">
  <meta property="og:title" content="Three Looks for Sonoma">
  <meta property="og:description" content="An editorial styling for a May wedding weekend, by Buck Mason.">
  <meta property="og:url" content="{{ABSOLUTE_PAGE_URL}}">
  <meta property="og:image" content="{{ABSOLUTE_OG_IMAGE_URL}}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Buck Mason lookbook hero — Look 01">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Three Looks for Sonoma">
  <meta name="twitter:description" content="An editorial styling for a May wedding weekend, by Buck Mason.">
  <meta name="twitter:image" content="{{ABSOLUTE_OG_IMAGE_URL}}">

  <style>
    /* Embed all CSS inline — no external stylesheets, no font CDN.
       Stacks chosen to mimic Acumin Pro / Acumin Pro Condensed offline.
       See references/brand-style.md for the source-of-truth values. */
    :root {
      --bm-cond: "Acumin Pro Condensed", "Helvetica Neue Condensed", "Helvetica Neue", Helvetica, Arial, sans-serif;
      --bm-body: "Acumin Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    body { font-family: var(--bm-body); color: #333; background: #fff; margin: 0; font-size: 13px; line-height: 1.4; }
    .page { max-width: 1100px; margin: 0 auto; padding: 64px 32px; }
    .eyebrow { font-family: var(--bm-cond); font-size: 11px; letter-spacing: 0.02em; text-transform: uppercase; color: #666; }
    .cover h1 { font-family: var(--bm-cond); font-weight: 600; font-size: 20px; line-height: 1; letter-spacing: 0.02em; text-transform: uppercase; margin: 8px 0 24px; color: #333; }
    .look { display: grid; grid-template-columns: 3fr 4fr; gap: 32px; padding: 64px 0; }
    @media (max-width: 700px) { .look { grid-template-columns: 1fr; } }
    .look img.hero { width: 100%; aspect-ratio: 3/4; object-fit: cover; display: block; }
    .piece { display: flex; gap: 16px; padding: 16px 0; }
    .piece img { width: 80px; height: 107px; object-fit: cover; background: #fafafa; }   /* 3:4 thumbnail */
    .piece .name { font-family: var(--bm-cond); font-weight: 600; font-size: 13px; letter-spacing: 0.02em; text-transform: uppercase; }
    .piece a { color: #666; font-size: 11px; word-break: break-all; text-decoration: underline; }
    .stock { font-size: 11px; color: #666; margin-top: 4px; }
    .total { font-family: var(--bm-cond); font-weight: 700; font-size: 13px; letter-spacing: 0.02em; text-transform: uppercase; padding-top: 16px; margin-top: 16px; }
    .footer { text-align: center; font-family: var(--bm-cond); font-size: 11px; letter-spacing: 0.02em; text-transform: uppercase; color: #999; padding: 32px; }
  </style>
</head>
<body>
  <section class="page cover">
    <div class="eyebrow">Buck Mason · Spring 2026</div>
    <h1>Three Looks for Sonoma</h1>
    <p style="color:#666;">An editorial styling for a May wedding weekend.</p>
  </section>

  <section class="page look">
    <div><img class="hero" src="data:image/png;base64,…" alt="Look 01"></div>
    <div>
      <div style="font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#888;">Look 01</div>
      <h2 style="font-family:var(--bm-cond);font-weight:600;font-size:20px;letter-spacing:.02em;text-transform:uppercase;">Mediterranean Evening</h2>

      <div class="piece">
        <img src="data:image/jpeg;base64,…">
        <div>
          <div class="name">Brown / Natural Gun Club Graduate Jacket</div>
          <div>$698</div>
          <a href="https://www.buckmason.com/products/brown-natural-gun-club-graduate-jacket">buckmason.com/products/brown-natural-gun-club-graduate-jacket</a>
          <div class="stock">Size L — Online: In stock · Abbot Kinney: Low (5) · Century City: Out · Bloomies CC: Out</div>
        </div>
      </div>
      <!-- More pieces -->

      <div class="total">Look 01 total · $1,164</div>
    </div>
  </section>
  <!-- More looks -->

  <div class="footer">AI-generated try-on preview · Buck Mason / Pima.io</div>
</body>
</html>
```

### Image embedding (base64)

```bash
# bash one-liner per image
b64=$(base64 -i lookbook/2026-04-26-look-1.png)
# then string-substitute into the template: src="data:image/png;base64,$b64"
```

Or in Python:
```python
import base64, mimetypes, pathlib
def embed(path):
    mime, _ = mimetypes.guess_type(str(path))
    b64 = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
    return f"data:{mime};base64,{b64}"
```

### File-size sanity check
- 3 looks × (1 hero @ 2 MB + 3 thumbnails @ 200 KB) = ~7.8 MB raw → ~10.4 MB base64-encoded.
- If size matters (email attachment, mobile), pre-resize the hero PNGs to 1024px wide JPEG with `magick hero.png -resize 1024x -quality 85 hero.jpg` before embedding — drops to ~3 MB total.

### Responsive — mobile / tablet / desktop (non-negotiable)

**The lookbook must look right on iPhone, iPad, and laptop.** Buck Mason's customers open links from iMessage on their phone first, the desktop check-in is later. Anything that overflows, mis-stacks, or hides the per-piece info on a 390px-wide viewport is a defect — even if the desktop layout is gorgeous. This applies equally to the static `html`, the interactive `html-cart`, and any React-flavored variant if you take that branch.

Three breakpoint tiers, named after the device tier they target:

| Tier | Width | Layout | Notes |
|---|---|---|---|
| Mobile | `< 700px` | Single column. Hero image full-width above the per-piece list. Page padding 16–24px. Cart bar full-width sticky bottom. Handoff modal nearly full-screen (small inset). | Default for ~60% of opens — design here first, then expand. |
| Tablet | `700px – 1023px` | Single column with wider page padding (32px), but with a sub-grid: per-piece thumbnails at 96–112px instead of 80px. Cart bar full-width. | iPad portrait; iPad landscape; many in-between Android tablets. |
| Desktop | `≥ 1024px` | Two-column hero/pieces split (the `1fr 1fr` or `3fr 4fr` grid). Page padding 32–64px. Cart bar centered or with side margins. | Laptops, monitors. Don't go wider than ~1100px max-width — the brand vibe is editorial, not magazine-spread. |

The skeleton above includes the mobile breakpoint (`@media (max-width: 700px)`); for `html-cart` (and any new variant), add the tablet rule too:

```css
@media (max-width: 1023px) and (min-width: 700px) {
  .look { grid-template-columns: 1fr; gap: 24px; }   /* still single-column but tighter */
  .page { padding: 48px 32px; }
  .piece img { width: 96px; height: 128px; }         /* slightly larger thumbs than mobile */
  #cart-bar { padding: 14px 24px; font-size: 11px; } /* keep cart bar usable */
  #handoff { inset: 24px; padding: 24px; }
}

@media (max-width: 699px) {
  .page { padding: 32px 16px; }
  .piece { padding-left: 28px; }                      /* room for the checkbox */
  .piece img { width: 64px; height: 85px; }           /* compact thumbs */
  #cart-bar { padding: 12px 16px; font-size: 10px; }
  #cart-bar button { padding: 10px 16px; font-size: 10px; }
  #handoff { inset: 12px; padding: 20px; }
  #handoff pre { font-size: 11px; }
}
```

Touch-target rules that override the desktop styling on mobile:

- **Checkboxes and buttons must be at least 44×44px tap targets** on mobile (Apple's HIG; matches Material). The desktop 16×16px checkbox should expand its hit area via padding on the wrapping label, not by enlarging the visual square. The visual stays minimal; the hit area gets generous.
- **"Send to my stylist" button** on mobile is full-width with ~14px vertical padding minimum, not a centered medium button.
- **External links** (`buckmason.com/products/...` per piece) need `word-break: break-all` to wrap long slugs without overflowing the viewport.
- **Hero image** uses `width: 100%` + `aspect-ratio: 3/4` + `object-fit: cover` so it scales without breaking the brand 3:4 portrait crop.

Test (or have the customer test) at three real viewports before sharing:

```bash
# After deploy, screenshot at three widths to spot-check.
# Replace <url> with the deploy URL.
for w in 390 768 1280; do
  npx playwright screenshot --viewport-size="$w,800" "<url>" "screenshot-${w}.png"
done
```

(Playwright is one option; any headless browser works.) The agent doesn't need to do this every time, but at least once when the skeleton or any layout-touching CSS changes.

**What NOT to do on mobile:**
- ❌ Hide the per-piece info ("show on hover" patterns) — touch has no hover.
- ❌ Force the desktop two-column layout via horizontal scroll. Stack instead.
- ❌ Use `vh` units alone for cart-bar / modal heights — Safari's dynamic toolbar makes `100vh` unreliable. Use `dvh` (`100dvh`) or fixed pixel values.
- ❌ Disable user pinch-zoom (`maximum-scale=1.0` on the viewport meta) — accessibility regression and no real benefit.
- ❌ Render the OG image inline at full size on mobile — it's a social-preview asset, not body content.

---

## 4. `html-cart` — interactive checkbox lookbook + stylist handoff

Same builder as `html`, plus a checkbox per piece, a sticky selection summary, and a **"Send to my stylist"** button that emits a structured JSON block the customer pastes back to the agent. The agent then drives **MPP checkout** (workflow #4 path B in `SKILL.md`), gathering ship-vs-pickup, coupon, and credit conversationally and calling `POST /mcp/buckmason/checkout`. Buck Mason / Shopify never enter the customer's UI.

**Why this format exists.** Plain `html` is a viewer; `html-cart` is an intent-capture surface. Use it whenever the lookbook is going to drive a purchase **and MPP is reachable** — `@stripe/link-cli` is installed in the agent's runtime AND the customer has a Stripe Link account with a payment method linked (persisted as `profile.md → link_payment_method: confirmed`). Without those, the cart bar would emit a handoff the agent can't actually settle, which is worse than no cart bar at all — fall back to hosted `html` (read-only commerce, voting still enabled) or `ppt` only when the customer explicitly asked for slides. `OPENAI_API_KEY` is orthogonal — it gates the try-on images inside any of these formats, not MPP.

Use plain `html` when the customer explicitly wants a non-commerce shareable artifact (email body, public preview), or when MPP isn't reachable on this surface.

### What's added on top of `html`

- **Per-piece checkbox** at the top-left of every `.piece` row. Default: unchecked.
- **Sticky selection footer** (`position: fixed; bottom: 0`) showing running selected count, running subtotal (sum of `price_cents_at_pick`), and a "Send to my stylist" button. Hidden until at least one box is checked.
- **A modal reveal** on click that shows the plain-prose handoff (below) with a one-button "Copy to clipboard" affordance that flips to "✓ Copied" briefly on success.
- **"Select this outfit" toggle per look** — a brand-outline button at the bottom of each look's piece list (after the subtotal) that selects every checkbox in that look in one tap. Toggles bidirectionally: when all pieces in the look are already selected, the same button deselects them and the label flips to "Outfit selected" (with a `✓` prefix and the brand black-fill style) so the state is always visually obvious.
- **"Select all looks" global toggle** — a single brand-outline button on the cover that flips every piece on the page on or off. Same toggle pattern as the per-look button. Useful when the customer says "yeah, ship me everything" without scanning each row.
- **Full-screen image lightbox.** Tapping any look hero or piece thumbnail opens it full-screen on a near-black overlay (`rgba(0,0,0,0.94)`) with a small × close affordance, click-outside-to-close, and ESC key support. The lightbox is critical on mobile — the inline thumbnails are too small to assess fabric weight or color nuance, and the look hero deserves to be examined at full resolution before the customer commits to the cart. Prevent the lightbox click from also toggling the underlying piece checkbox via `e.stopPropagation()`.
- **No network calls.** The HTML is still fully self-contained; `<script>` is vanilla DOM only — no fetch, no analytics, no font CDN. Persistence (cross-session wishlist) is the agent's job, not the page's — the agent owns `~/.buck-mason-stylist/wishlist.jsonl`.

### The handoff is plain English — speakable, pasteable, agent-parseable

When the customer clicks "Send to my stylist," the page reveals a short prose paragraph naming the lookbook + the selected pieces in natural language. The customer either pastes that text back into their stylist agent, or — for voice flows — just speaks the same thing aloud ("from the LA Mellow Weekend lookbook, I want the camp shirt in L and the chinos in 31"). The agent resolves the names against the catalog on its end.

The format the modal renders:

```
Buck Mason — LA Mellow Weekend Lookbook (2026-05-09)

I'd like to order:
• Natural Draped Linen Deuce Coupe Camp Shirt — size L — $168
• Khaki Tropic Twill Carry-On Ford Standard Pant — size 31 — $168

Subtotal at pick: $336
Please confirm shipping or pickup, any coupon or credit, and run checkout.
```

That's it. No JSON, no envelope, no kind/version. Three reasons:

- **Voice is first-class.** The same paragraph reads naturally aloud — "from the LA Mellow Weekend lookbook, the camp shirt in L and the carry-on pant in 31." A customer with a hands-busy moment (driving, walking the dog, kid in the lap) can speak the order without reciting a SKU like `BM13211.679NATL`. Even shorter forms work — "I want that camp shirt in a large" — because the agent has the lookbook context from the page or the conversation.
- **Agents parse natural language.** Modern LLM-backed agents resolve "Natural Draped Linen Deuce Coupe Camp Shirt" to a Pima SKU as easily as they'd parse `{"sku":"BM13211.679NATL"}` — and the resolution path uses the existing `GET /products?q=…` endpoint, no new contract to maintain.
- **The HTML stays clean.** The page is a curated lookbook a customer can airdrop or screenshot and share, not a JSON dump.

The HTML still stamps full structured info on each piece's checkbox as `data-` attributes (`data-name`, `data-size`, `data-sku`, `data-price-cents`, `data-url`) so a power user, scraper, or future-feature can read the canonical SKU directly without resolving by name. The customer-visible handoff is prose; the wire-friendly form is right there in the DOM if anything wants it.

### What the agent does on paste-back (or voice)

The agent receives prose like the block above (or a one-line voice-style dictation) and runs **workflow #4 path B (MPP)** in `SKILL.md`. The shape of the receiving conversation:

1. **Detect the handoff.** Heuristics: text mentions "Buck Mason" + lookbook context + a list of items (bulleted or comma-separated) with sizes. Don't require an exact format — the customer might trim the paragraph or speak a fragment.
2. **Resolve each named item to a Pima SKU.** For each line, search `GET /mcp/buckmason/products?gender=<m|w>&q=<distinctive substring of the name>` and pick the `id` (the `q` quirk discussed in `references/mcp-api.md` applies — short distinctive substrings beat long phrases). Then `GET /products/<id>` and pick the variant matching the customer's stated size. If a name is ambiguous (rare on Buck Mason's catalog, but possible — e.g., "the linen pant" when there are several), ask the customer one disambiguation question naming the candidates.
3. **Reconcile against the lookbook context** if available. If the agent still has the conversation context that generated the lookbook, the resolution is unambiguous — "the camp shirt" maps to the one shown in Look 01. The `lookbook_id` line in the prose (`LA Mellow Weekend Lookbook (2026-05-09)`) lets the agent re-load that context from `~/.buck-mason-stylist/wishlist.jsonl` if it's been started fresh in a new session.
4. **Gather the rest conversationally — one round trip, defaults assumed.** Default: ship to `profile.md → shipping`, no coupon, apply all available customer credit. Restate as: *"Shipping to <street>, no coupon, applying $X in credit. Anything to change?"* Accept either "go ahead" or a one-line correction (`pickup at Abbot Kinney`, `code SPRING25`, `skip credit`).
5. **Spot price drift** by comparing the customer's "subtotal at pick" (from the prose, when present) against the live phase-1 line-item subtotal. >1% variance → surface the diff in plain English before reading the total back.
6. **Then proceed** with the standard MPP cycle: phase-1 POST → restate total → `link-cli spend-request create` → push-approve → phase-2 POST with `acknowledged_total_cents`. Full mechanics in `references/mpp.md`.
7. **On success, append the order** to `~/.buck-mason-stylist/wishlist.jsonl` with the lookbook id, item names, sizes, resolved SKUs, and `order_id`. Cross-session memory for future "you bought the camp shirt last week — different color this time?" conversations.

**Voice-only conversations** skip the paste step entirely. The agent sees a generated lookbook in its session, the customer says "buy the camp shirt and the chinos in my usual sizes," and the agent maps "camp shirt" + "chinos" to the items it just rendered. The prose handoff format is what makes that possible — it's the same vocabulary the customer would use spontaneously.

### Aesthetic — match buckmason.com

**Read `references/brand-style.md` before generating an `html-cart` lookbook.** It's the extracted style guide from `buckmason.com` itself (homepage, a collections page, a PDP) — fonts, colors, type scale, button shape, image ratios — and it overrides any "editorial" instinct the model might bring. Quick reminders, but the doc is the source of truth:

- **Background is pure white (`#FFFFFF`)**. Off-white (`#F3F1EF`) is a banner accent, not a page color.
- **One typeface family**: Acumin Pro (body) + Acumin Pro Condensed (every label / headline / button / nav). Self-contained `html-cart` falls back to `"Helvetica Neue Condensed", "Helvetica Neue", Helvetica, Arial, sans-serif` for the condensed face. **No serifs anywhere** — don't reach for Georgia, Canela, Söhne, Inter.
- **Letter-spacing on uppercase: 0.02em (≈2%)**. Exact value matters; the brand reads tight.
- **Headlines stay small.** PDP h1 is ~20px. Don't render display-size titles (40px+); imagery carries the visual weight, not type.
- **Sharp corners**: `border-radius: 1px` on CTAs and form controls. No pills.
- **Hero / product crops**: **3:4 portrait** (`width / height = 0.75`). Not 4:5, not 1:1, not 16:9.
- **No visible section dividers.** Section identity comes from short uppercase eyebrow labels (e.g., `LOOK 01`) + whitespace, not from rules.
- **Send to my stylist** button: black background, white text, Acumin Pro Condensed 700, ~14px, +2% letter-spacing, uppercase, full-width, sharp corners.

### Skeleton — additions on top of `html`

**Re-test responsive after every layout change.** The cart bar, the handoff modal, and the per-piece checkbox column add fixed-position + grid changes that the inherited mobile/tablet breakpoints from `html` cover, but it's easy to regress. Walk the three viewport tiers (390 / 768 / 1280) at least once before shipping a layout edit. Full rules in § "Responsive — mobile / tablet / desktop" above.


```html
<!-- inside <head><style>…</style></head>, append: -->
<style>
  .piece { position: relative; padding-left: 32px; }
  .piece input[type="checkbox"] { position: absolute; left: 0; top: 14px; appearance: none; width: 16px; height: 16px; border: 1px solid #1a1a1a; cursor: pointer; }
  .piece input[type="checkbox"]:checked { background: #1a1a1a; }
  .piece input[type="checkbox"]:checked::after { content: ""; position: absolute; left: 4px; top: 0; width: 4px; height: 10px; border: solid #fff; border-width: 0 2px 2px 0; transform: rotate(45deg); }
  #cart-bar { position: fixed; bottom: 0; left: 0; right: 0; background: #1a1a1a; color: #faf8f4; padding: 16px 32px; display: none; justify-content: space-between; align-items: center; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; }
  #cart-bar.show { display: flex; }
  #cart-bar button { background: #faf8f4; color: #1a1a1a; border: 0; padding: 12px 24px; font: inherit; letter-spacing: .18em; cursor: pointer; }
  #handoff { display: none; position: fixed; inset: 40px; background: #faf8f4; z-index: 10; padding: 32px; overflow: auto; box-shadow: 0 0 60px rgba(0,0,0,.3); }
  #handoff.show { display: block; }
  #handoff pre { background: #fff; border: 1px solid #ddd; padding: 16px; font-size: 12px; white-space: pre-wrap; word-break: break-all; }

  /* Brand outline button — used for "Select all looks" + "Select this outfit" */
  .bm-btn-outline { display: inline-block; font-family: var(--bm-cond, sans-serif); font-weight: 600; font-size: 12px; letter-spacing: 0.02em; text-transform: uppercase; color: #1a1a1a; background: transparent; border: 1px solid #1a1a1a; padding: 12px 20px; min-height: 44px; cursor: pointer; transition: background 120ms, color 120ms; }
  .bm-btn-outline:hover { background: #1a1a1a; color: #fff; }
  .bm-btn-outline.selected { background: #1a1a1a; color: #fff; }
  .bm-btn-outline.selected::before { content: "✓ "; }
  #select-all-btn { margin-top: 16px; }
  .select-outfit { margin-top: 20px; align-self: flex-start; }

  /* Full-screen image lightbox */
  .look-hero img, .piece img { cursor: zoom-in; }
  #lightbox { position: fixed; inset: 0; background: rgba(0,0,0,0.94); display: none; align-items: center; justify-content: center; z-index: 20; padding: 32px; cursor: zoom-out; }
  #lightbox.show { display: flex; }
  #lightbox img { max-width: min(100%, 1600px); max-height: 100%; object-fit: contain; cursor: default; display: block; }
  #lightbox .close { position: absolute; top: 12px; right: 12px; background: transparent; color: #fff; border: 0; font: 24px/1 var(--bm-cond, sans-serif); cursor: pointer; padding: 12px 16px; min-height: 44px; min-width: 44px; }
  @media (max-width: 699px) { #lightbox { padding: 12px; } }
</style>

<!-- per .piece, prepend a checkbox. The customer-visible handoff is plain
     prose composed from data-name/data-size at copy time; data-sku is
     stamped for any downstream consumer that wants the canonical id without
     re-resolving (power users, future features). -->
<input type="checkbox"
       data-name="Brown / Natural Gun Club Graduate Jacket"
       data-size="L"
       data-sku="GUN-CLUB-JACKET-BROWN-NATURAL-L"
       data-qty="1"
       data-price-cents="69800">

<!-- before </body>, add the cart bar + handoff modal: -->
<div id="cart-bar">
  <span><span id="cart-count">0</span> selected · <span id="cart-total">$0</span></span>
  <button onclick="openHandoff()">Send to my stylist</button>
</div>
<!-- Per-section markup the builder emits:
     • Each <section class="look" data-look="<id>"> wraps a look. The
       data-look attribute is what scopes the per-outfit selector.
     • A <button class="bm-btn-outline select-outfit"
         data-target-look="<id>" onclick="toggleLook('<id>', this)">
         Select this outfit
       </button> sits at the bottom of each look's piece list (after the
       Look subtotal).
     • A <button id="select-all-btn" class="bm-btn-outline"
         onclick="toggleAll(this)">Select all looks</button>
       lives on the cover, after the description. -->

<!-- Full-screen image lightbox; opens on any .look-hero img or .piece img click. -->
<div id="lightbox" onclick="closeLightbox(event)">
  <button class="close" type="button" aria-label="Close image" onclick="closeLightbox(event, true)">×</button>
  <img id="lightbox-img" alt="">
</div>

<div id="handoff">
  <h2>Tell your stylist</h2>
  <p style="color:#666;font-size:13px;">Speak this aloud to a voice agent, or paste it into a chat. Your agent will confirm shipping or pickup, coupon, and credit before charging.</p>
  <pre id="handoff-text"></pre>
  <button id="copy-btn" onclick="copyHandoff(this)" style="background:#1a1a1a;color:#faf8f4;border:0;padding:12px 24px;letter-spacing:.02em;text-transform:uppercase;font-size:11px;cursor:pointer;">Copy to clipboard</button>
  <button onclick="closeHandoff()" style="background:transparent;border:1px solid #1a1a1a;padding:12px 24px;letter-spacing:.02em;text-transform:uppercase;font-size:11px;margin-left:8px;cursor:pointer;">Close</button>
</div>

<script>
  // Lookbook id + display label stamped at build time.
  const LOOKBOOK_ID    = "2026-04-26-sonoma";              // builder substitutes
  const LOOKBOOK_TITLE = "Three Looks for Sonoma";          // builder substitutes
  const LOOKBOOK_DATE  = "2026-04-26";                      // builder substitutes; YYYY-MM-DD
  function selected() {
    return [...document.querySelectorAll('.piece input[type="checkbox"]:checked')].map(el => ({
      name:  el.dataset.name,
      size:  el.dataset.size,
      qty:   parseInt(el.dataset.qty, 10),
      cents: parseInt(el.dataset.priceCents, 10),
    }));
  }
  function refresh() {
    const items = selected();
    const cents = items.reduce((a, i) => a + i.cents * i.qty, 0);
    document.getElementById('cart-count').textContent = items.length;
    document.getElementById('cart-total').textContent = '$' + (cents / 100).toFixed(2);
    document.getElementById('cart-bar').classList.toggle('show', items.length > 0);
  }
  function fmtMoney(c) { return '$' + (c / 100).toFixed(c % 100 === 0 ? 0 : 2); }
  function buildHandoffText() {
    const items = selected();
    if (items.length === 0) return '';
    const subtotal = items.reduce((a, i) => a + i.cents * i.qty, 0);
    const lines = items.map(i => {
      const qtyPart = i.qty > 1 ? ` (×${i.qty})` : '';
      return `• ${i.name} — size ${i.size} — ${fmtMoney(i.cents)}${qtyPart}`;
    });
    return [
      `Buck Mason — ${LOOKBOOK_TITLE} (${LOOKBOOK_DATE})`,
      '',
      `I'd like to order:`,
      ...lines,
      '',
      `Subtotal at pick: ${fmtMoney(subtotal)}`,
      `Please confirm shipping or pickup, any coupon or credit, and run checkout.`,
    ].join('\n');
  }
  function openHandoff() {
    document.getElementById('handoff-text').textContent = buildHandoffText();
    document.getElementById('handoff').classList.add('show');
  }
  function closeHandoff() { document.getElementById('handoff').classList.remove('show'); }
  let copyResetTimer = null;
  async function copyHandoff(btn) {
    try {
      await navigator.clipboard.writeText(document.getElementById('handoff-text').textContent);
    } catch (e) {
      // Fallback for older browsers / non-secure contexts
      const r = document.createRange(); r.selectNode(document.getElementById('handoff-text'));
      getSelection().removeAllRanges(); getSelection().addRange(r);
      document.execCommand('copy'); getSelection().removeAllRanges();
    }
    btn.dataset.original = btn.dataset.original || btn.textContent;
    btn.textContent = '✓ Copied';
    btn.disabled = true;
    clearTimeout(copyResetTimer);
    copyResetTimer = setTimeout(() => {
      btn.textContent = btn.dataset.original;
      btn.disabled = false;
    }, 1800);
  }
  document.addEventListener('change', e => {
    if (e.target.matches('.piece input[type="checkbox"]')) { refresh(); refreshSelectButtons(); }
  });

  // "Select this outfit" + "Select all looks" toggles
  function lookCheckboxes(lookId) { return [...document.querySelectorAll(`.look[data-look="${lookId}"] .piece input[type="checkbox"]`)]; }
  function allCheckboxes()        { return [...document.querySelectorAll('.piece input[type="checkbox"]')]; }
  function toggleLook(lookId, btn) {
    const boxes = lookCheckboxes(lookId);
    const allChecked = boxes.length > 0 && boxes.every(b => b.checked);
    boxes.forEach(b => { b.checked = !allChecked; });
    refresh(); refreshSelectButtons();
  }
  function toggleAll(btn) {
    const boxes = allCheckboxes();
    const allChecked = boxes.length > 0 && boxes.every(b => b.checked);
    boxes.forEach(b => { b.checked = !allChecked; });
    refresh(); refreshSelectButtons();
  }
  function refreshSelectButtons() {
    document.querySelectorAll('.select-outfit').forEach(btn => {
      const boxes = lookCheckboxes(btn.dataset.targetLook);
      const allChecked = boxes.length > 0 && boxes.every(b => b.checked);
      btn.classList.toggle('selected', allChecked);
      btn.textContent = allChecked ? 'Outfit selected' : 'Select this outfit';
    });
    const allBtn = document.getElementById('select-all-btn');
    if (allBtn) {
      const all = allCheckboxes();
      const everySelected = all.length > 0 && all.every(b => b.checked);
      allBtn.classList.toggle('selected', everySelected);
      allBtn.textContent = everySelected ? 'Deselect all' : 'Select all looks';
    }
  }

  // Lightbox: open on any look-hero or piece thumbnail click
  function openLightbox(src, alt) {
    const lb = document.getElementById('lightbox');
    const img = document.getElementById('lightbox-img');
    img.src = src; img.alt = alt || '';
    lb.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
  function closeLightbox(ev, force) {
    if (!force && ev && ev.target && ev.target.id === 'lightbox-img') return; // ignore clicks on the image
    document.getElementById('lightbox').classList.remove('show');
    document.body.style.overflow = '';
  }
  document.addEventListener('click', e => {
    const img = e.target.closest('.look-hero img, .piece img');
    if (img) {
      e.preventDefault();
      e.stopPropagation();   // don't toggle the underlying piece checkbox
      openLightbox(img.dataset.fullsize || img.src, img.alt);
    }
  }, true);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(null, true); });
</script>
```

### What the builder must stamp at generation time

For the prose handoff to read naturally and the agent to resolve names cleanly, the builder needs five things on each `.piece` and three at the page level.

Per-piece (`<input type="checkbox">` on each `.piece`):

1. `data-name` — the product's full display name as returned by `/products/<id>` (`name` field), e.g. `Natural Draped Linen Deuce Coupe Camp Shirt`. This is what shows in the prose handoff and what the agent searches for on resolution.
2. `data-size` — the picked size string (`L`, `31`, `32x32`, `10.5`).
3. `data-sku` — the canonical Pima SKU name from `variants[].sku`. **Stamped for any downstream consumer that wants to skip name-resolution** (a future "Add to bag on Buck Mason" link, a power-user scraper, an alternate non-prose handoff). Not consumed by the prose modal itself.
4. `data-price-cents` — integer cent price at lookbook generation. Drives the running cart total and the "Subtotal at pick" line in the handoff.
5. `data-qty` — usually `1`; here for completeness if a future builder ever stamps multi-qty.

Page level (`<script>` constants substituted at build time):

- `LOOKBOOK_ID` — `<date>-<event>` slug used for filenames and cross-session memory in `~/.buck-mason-stylist/wishlist.jsonl`.
- `LOOKBOOK_TITLE` — the human-readable title that goes into the prose ("Three Looks for Sonoma," "LA Mellow Weekend").
- `LOOKBOOK_DATE` — `YYYY-MM-DD`, displayed parenthetically after the title.

### Server-side behavior — confirmed against `pima-master`

These were verified against `app/services/mcp/checkout.rb` and `app/controllers/mcp_controller.rb` and are stable assumptions for `html-cart`:

- **`/checkout` accepts pickup at both top-level and per-item** — `pickup_location_slug` / `pickup_location_id` at the checkout level applies as a default to any line item without its own; per-item `pickup_location_slug` / `pickup_location_id` / `pickup_location_name` overrides for mixed ship+pickup carts. Pickup-disabled locations return `pickup_disabled` in the line-item errors. The agent gathers pickup conversationally on paste-back; the HTML never embeds it.
- **Checkout line items use resolved SKUs.** `/checkout` takes `{ sku: <sku-name>, quantity }` directly (it does *not* read `size`). The handoff matches `/checkout`; resolve product name + size to SKU before preflight.
- **Phase-1 totals include TaxJar sales tax** (estimated against the customer's `fulfillment_address` for ship items and the pickup_location for pickup items). Phase 2's preflight then re-runs `Order#update_taxes!` against the persisted Order so the customer's `acknowledged_total_cents` matches what's charged.
- **Coupon validation is strict** — the preflight builds a real `pending` Order, runs `Coupon#applicable?` (the same 25+ rules POS uses), and on failure raises `PreflightFailed('coupon_not_applicable', …)` → 422 with `error.code: "coupon_not_applicable"`. No Stripe call. Surface the reason verbatim from `error.message`.
- **Customer credits actually debit** via `CustomerCreditTransaction#complete!` (DB-locked, capped at live balance). Drained codes return `credit_no_balance` in `credit_status[]`.

---

## Hosting the HTML lookbook online

**Read `references/hosting-options.md`.** It carries the full capability-aware menu: probe scripts, ranked transports (Cloudflare Pages → Netlify → Vercel → Surge → Gist → S3 → 0x0.st), per-transport deploy commands, sticky preference persistence in `profile.md`, and the design rules around confirm-before-publish and "tool installed but unauthenticated is a soft-no." The agent runs the probe, picks the top transport that's actually usable, asks once, and deploys. Don't reproduce that decision tree here.

For Cloudflare Pages, **voting is part of the default deploy**, not part of the deterministic HTML builder. `scripts/deploy-lookbook.sh` injects the vote UI, copies Pages Functions, renders `wrangler.toml`, and smoke-tests `/api/votes` when given `--kv-id` or `$LOOKBOOK_VOTES_KV_ID`. Missing KV id is a setup blocker; use `--no-voting` only for an explicitly read-only static lookbook. Full details live in `references/voting.md`.

After hosting, hand the URL back to the customer + offer a one-line "Open it" + a "Select Look 01 for checkout — $1,164" button (workflow 4).

---

## Common build pitfalls

1. **Plain-text URLs in PPT** — Keynote/PowerPoint do not auto-link. Wire `run.hyperlink.address` at generation time. Same applies to PDF if you ever add that format.
2. **Forgetting in-your-size stock filter** — generic "available online" is wrong; the customer wants per-size. Compute by SKU IDs, not Product IDs.
3. **HTML without base64 embed** — `file://` references break the moment the file moves. Always embed for portability.
4. **Hero PNG too large** — 2 MB × 3 looks = 6 MB of inline data → email rejected by some servers. Pre-resize to 1024px JPEG.
5. **Setting drift dropping anchor pieces** — gpt-image-2 sometimes drops outer layers. See `references/image-generation.md` "gpt-image-2 hint inventory" for the JACKET LOCK pattern.
