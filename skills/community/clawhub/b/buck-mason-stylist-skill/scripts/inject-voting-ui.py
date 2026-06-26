#!/usr/bin/env python3
"""Inject a voting widget (thumbs up/down per look + per item) + favicon links
into a built lookbook's index.html.

This is a *post-build* step — the deterministic build (scripts/build-html-
lookbook.py) does NOT include voting by default. Voting is opt-in per
references/voting.md.

Usage:
  python3 scripts/inject-voting-ui.py --deploy-dir <path-to-deploy-dir>

The script reads:
  <deploy-dir>/index.html  — built by scripts/build-html-lookbook.py
  <deploy-dir>/thumb-*.jpg — referenced from the per-item rows

And produces an in-place rewrite of index.html with:
  - <!-- FAVICON -->  block in <head>  (favicon link tags)
  - <style id="vote-widget-css"> in <head>
  - <!-- VOTE-WIDGET --> <section class="vote"> before </body>
  - <script id="vote-widget-js"> before </body>

Idempotent: re-running strips the prior injection blocks and reinjects fresh.

Companion files an agent must also drop into the deploy dir before deploying:
  functions/api/vote.js      — copy from templates/voting/functions-api-vote.js
  functions/api/votes.js     — copy from templates/voting/functions-api-votes.js
  wrangler.toml              — copy from templates/voting/wrangler.toml.example
                               (fill in name, LOOKBOOK_ID, KV namespace id)
  favicon.ico, favicon-32.png, favicon-16.png, apple-touch-icon.png
                             — see references/voting.md for source URLs

See references/voting.md for the full architecture, the KV-namespace setup
incantation, and the security model.
"""
import argparse, pathlib, re, sys

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--deploy-dir", required=True, type=pathlib.Path,
                help="Path to the deploy directory (containing index.html)")
args = ap.parse_args()

PATH = args.deploy_dir / "index.html"
if not PATH.is_file():
    print(f"error: not found: {PATH}", file=sys.stderr); sys.exit(2)

html = PATH.read_text()

# ── 1. Discover look IDs + per-look pieces (SKU + name + thumb) from HTML ──
look_ids = sorted(set(re.findall(r'data-look="(look\d+)"', html)))
print(f"detected looks: {look_ids}")
if not look_ids:
    print("error: no <section data-look=lookN> found — was index.html built?", file=sys.stderr); sys.exit(2)

PIECE_RE = re.compile(
    r'<input[^>]*data-name="([^"]+)"[^>]*data-sku="([^"]+)"',
    re.S,
)
def LOOK_SECTION_RE(lid): return re.compile(rf'<section[^>]*data-look="{lid}".*?</section>', re.S)
EYEBROW_RE = re.compile(r'<div class="eyebrow">(.*?)</div>', re.S)

look_data = []
for lid in look_ids:
    m = LOOK_SECTION_RE(lid).search(html)
    if not m: continue
    block = m.group(0)
    eyebrows = EYEBROW_RE.findall(block)
    title = re.sub(r'<[^>]+>', '', eyebrows[0]).strip() if eyebrows else lid
    pieces = []
    for name, sku in PIECE_RE.findall(block):
        thumb_m = re.search(
            rf'data-sku="{re.escape(sku)}".*?<img src="(thumb-[^"]+)"',
            block, re.S,
        )
        thumb = thumb_m.group(1) if thumb_m else ""
        pieces.append({"name": name, "sku": sku, "thumb": thumb})
    look_data.append({"id": lid, "title": title, "pieces": pieces})
print(f"looks={len(look_data)}, items={sum(len(L['pieces']) for L in look_data)}")

# ── 2. Build the voting widget HTML ──────────────────────────────────────────
CSS = """
<style id="vote-widget-css">
.vote { margin: 4rem auto 2rem; max-width: 720px; padding: 2rem 1.5rem; border: 1px solid var(--bm-line); background: #fafaf8; }
.vote h2 { font-family: var(--bm-cond); font-weight: 700; font-size: 1.6rem; letter-spacing: 0.04em; text-transform: uppercase; margin: 0 0 0.25rem; }
.vote p.lead { color: var(--bm-mute); margin: 0 0 1.5rem; font-size: 0.95rem; }
.vote-block { border-top: 1px solid var(--bm-line); padding: 1rem 0; }
.vote-block:first-of-type { border-top: 0; }
.vote-look-header { display: flex; align-items: center; gap: 0.8rem; font-weight: 700; font-size: 1.05rem; margin-bottom: 0.6rem; }
.vote-look-header .eyebrow { font-family: var(--bm-cond); letter-spacing: 0.06em; text-transform: uppercase; color: var(--bm-mute); font-size: 0.85rem; }
.vote-row { display: flex; align-items: center; gap: 0.8rem; padding: 0.5rem 0; font-size: 0.95rem; }
.vote-row.item { padding-left: 1.2rem; }
.vote-row img.tn { width: 36px; height: 44px; object-fit: cover; border: 1px solid var(--bm-line); flex: 0 0 auto; }
.vote-row .label { flex: 1 1 auto; color: var(--bm-ink); line-height: 1.25; word-break: break-word; }
.vote-row.item .label { color: var(--bm-mute); font-size: 0.9rem; }
.thumbs { display: flex; gap: 0.4rem; flex: 0 0 auto; }
.thumb-btn { border: 1px solid var(--bm-line); background: white; border-radius: 100px; width: 38px; height: 38px; font-size: 1.05rem; line-height: 1; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; user-select: none; transition: background 0.12s, border-color 0.12s, transform 0.08s; }
.thumb-btn:hover { background: #f3f0eb; }
.thumb-btn:active { transform: scale(0.92); }
.thumb-btn.up.on   { background: #e8f3e8; border-color: #4a8a4a; }
.thumb-btn.down.on { background: #f6e7e3; border-color: #b1503e; }
.thumb-btn.dim     { opacity: 0.45; }
.vote-name, .vote-comment { display: block; width: 100%; padding: 0.6rem 0.7rem; margin-top: 0.75rem; border: 1px solid var(--bm-line); background: white; font: inherit; }
.vote-comment { min-height: 80px; resize: vertical; }
.vote-submit { margin-top: 1rem; background: #1c1c1c; color: white; border: 0; padding: 0.8rem 1.2rem; font-family: var(--bm-cond); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; cursor: pointer; width: 100%; }
.vote-submit:hover { background: #333; }
.vote-submit[disabled] { background: #999; cursor: default; }
.vote-status { margin-top: 0.8rem; font-size: 0.9rem; color: var(--bm-mute); min-height: 1.2em; }
.vote-status.ok { color: #2a7c2a; }
.vote-status.err { color: #b03030; }
</style>
"""

def thumbs_html(kind, target_id):
    return (
      f'<div class="thumbs" data-kind="{kind}" data-id="{target_id}">'
      f'<button type="button" class="thumb-btn up" data-vote="up" aria-label="thumbs up">👍</button>'
      f'<button type="button" class="thumb-btn down" data-vote="down" aria-label="thumbs down">👎</button>'
      f'</div>'
    )

blocks = []
for L in look_data:
    item_rows = "".join(
        f'<div class="vote-row item">'
        f'<img class="tn" src="{p["thumb"]}" alt="">'
        f'<span class="label">{p["name"]}</span>'
        f'{thumbs_html("item", p["sku"])}'
        f'</div>'
        for p in L["pieces"]
    )
    blocks.append(
        f'<div class="vote-block">'
        f'  <div class="vote-look-header"><span class="eyebrow">{L["title"]}</span></div>'
        f'  <div class="vote-row look">'
        f'    <span class="label">Overall — how do you feel about this look?</span>'
        f'    {thumbs_html("look", L["id"])}'
        f'  </div>'
        f'  {item_rows}'
        f'</div>'
    )

WIDGET = (
"""
<!-- VOTE-WIDGET -->
<section class="vote" aria-label="Vote on these looks">
  <h2>What do you think?</h2>
  <p class="lead">Thumbs up or down on each whole look and each individual piece. Comments encouraged.</p>
  <form id="vote-form">
"""
+ "".join(blocks) +
"""
    <input class="vote-name" name="voter" placeholder="Your name (so I know it's you)" maxlength="60" required>
    <textarea class="vote-comment" name="comment" placeholder="Optional comment — fit notes, vibe, hot takes…" maxlength="1000"></textarea>
    <button class="vote-submit" type="submit">Submit vote</button>
    <div class="vote-status" id="vote-status" aria-live="polite"></div>
  </form>
</section>
""")

SCRIPT = """
<script id="vote-widget-js">
document.querySelectorAll('.thumbs').forEach(group => {
  group.querySelectorAll('.thumb-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const current = group.dataset.value || '';
      const clicked = btn.dataset.vote;
      const next    = (current === clicked) ? '' : clicked;
      group.dataset.value = next;
      group.querySelectorAll('.thumb-btn').forEach(b => {
        const isOn = b.dataset.vote === next && next !== '';
        b.classList.toggle('on',  isOn);
        b.classList.toggle('dim', next !== '' && !isOn);
      });
    });
  });
});
document.getElementById('vote-form')?.addEventListener('submit', async e => {
  e.preventDefault();
  const form   = e.currentTarget;
  const btn    = form.querySelector('.vote-submit');
  const status = document.getElementById('vote-status');
  status.className = 'vote-status'; status.textContent = 'Submitting…';
  btn.disabled = true;
  const looks = {}, items = {};
  form.querySelectorAll('.thumbs').forEach(g => {
    if (!g.dataset.value) return;
    if (g.dataset.kind === 'look') looks[g.dataset.id] = g.dataset.value;
    else                            items[g.dataset.id] = g.dataset.value;
  });
  const payload = { voter: form.voter.value.trim(), comment: form.comment.value.trim(), looks, items };
  try {
    const r = await fetch('/api/vote', { method: 'POST', headers: {'content-type':'application/json'}, body: JSON.stringify(payload) });
    const j = await r.json();
    if (j.ok) { status.className='vote-status ok'; status.textContent='Thanks — vote recorded ❤️'; btn.textContent='Submitted'; }
    else { throw new Error(j.error || 'unknown error'); }
  } catch (err) {
    status.className='vote-status err'; status.textContent='Error: '+err.message; btn.disabled = false;
  }
});
</script>
"""

FAVICON_TAGS = """
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
  <link rel="shortcut icon" href="favicon.ico">
"""

# ── 3. Strip any prior injection, then inject fresh ──────────────────────────
html = re.sub(r'<!-- VOTE-WIDGET -->.*?</section>\s*', '', html, flags=re.S)
html = re.sub(r'<style id="vote-widget-css">.*?</style>\s*', '', html, flags=re.S)
html = re.sub(r'<script id="vote-widget-js">.*?</script>\s*', '', html, flags=re.S)
html = re.sub(r'<!-- FAVICON -->.*?<!-- /FAVICON -->\s*', '', html, flags=re.S)

favicon_block = "<!-- FAVICON -->" + FAVICON_TAGS + "<!-- /FAVICON -->\n"
html = html.replace("</head>", favicon_block + CSS + "\n</head>", 1)
html = html.replace("</body>", WIDGET + "\n" + SCRIPT + "\n</body>", 1)

PATH.write_text(html)
print(f"wrote {PATH} ({len(html)} bytes)")
