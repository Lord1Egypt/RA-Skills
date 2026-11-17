---
name: ebay-lister
description: >-
  Turn photos of an item into a real, LIVE eBay listing — identifies the item, researches
  sold-comp pricing, assesses condition, fills the essential listing fields, then drives your
  logged-in Chrome to eBay, fills the Create-listing form (photos included), and PUBLISHES it.
  Triggers on `/sell`, or messages like "sell this on ebay", "list this on ebay", "make me an
  ebay listing", "what's this worth + list it" — especially when photos are attached. On "List
  it" eBay validates and the script fills any required field from the payload and retries; if it
  still can't satisfy a required field it falls back to saving a DRAFT (never publishes junk)
  and reports what's missing.
homepage: https://github.com/NelsonScott/ebay-lister
metadata: {"openclaw": {"emoji": "🏷️", "homepage": "https://github.com/NelsonScott/ebay-lister", "requires": {"bins": ["node"]}, "install": [{"kind": "node", "package": "playwright-core"}]}}
---

# ebay-lister

Photos in → a finished eBay listing out. The judgment (identify, price, grade) is yours; the
form-filling is `list.js`, which drives an already-logged-in Chrome over CDP.

The split of labor:
- **You (the agent)** do the judgment: read the photos, identify the item, research sold comps,
  grade condition, and assemble the listing fields. This is vision + web-search work.
- **`list.js`** does the deterministic browser work: connect to the logged-in Chrome over CDP,
  open eBay's Create-listing flow, upload the photos, fill the fields you assembled, and click
  **List it** to publish (falling back to a draft only if a required field can't be auto-filled).
  It prints `PUBLISHED_URL` (or `PUBLISH_BLOCKED` + `DRAFT_URL`).

## Setup (once)

1. `npm install` in this directory (pulls `playwright-core`).
2. Have a Chrome running with remote debugging enabled and **logged into eBay**. Default endpoint
   is `http://127.0.0.1:18800`.
3. `cp ebay-lister.config.example.json ebay-lister.config.json` and edit it — CDP endpoint,
   listing defaults (format, starting bid, duration), preferred shipping service, category-id
   shortcuts, and an optional notify command. That file is gitignored; with no config file at all
   the built-in defaults apply.

## When this fires

Only when the user clearly wants to sell/list something — `/sell`, or natural language like
"list this on ebay" / "sell this" / "make an ebay listing" / "what's this worth, throw it up".
A **bare photo with no such ask → do nothing.** If photos arrive with `/sell` or a selling
caption, go.

## Photos

Photos usually land in a media directory (wherever your chat/upload integration writes them) and
also reach you as vision content. **Treat all photos in the triggering message as ONE item** shot
from multiple angles — never split a batch into separate listings.

- **First photo = the anchor/ID shot.** Lean on it for brand, model, model number, serial.
- Remaining photos enrich the listing and document condition. They all get uploaded to eBay.
- **Resolution gotcha:** chat apps compress normal "photo" sends, which can blur small model
  numbers / serial labels. If you can't confidently read a critical label on the anchor shot,
  **ask for that one shot again as an uncompressed file attachment**. Don't guess a full model
  number from a blurry fragment.
- HEIC: if any inbound file is `.heic`/`.HEIC`, convert to JPEG before viewing/uploading
  (`pip install pillow-heif` then read_heif → PIL → save JPEG). eBay accepts JPEG/PNG.

Collect the absolute paths of every photo for this item — `list.js` needs them in order, anchor
first.

## Step 1 — Identify

Look at ALL photos before saying anything. Extract: brand/manufacturer, model name + number,
serial/part numbers, year/generation if determinable, size/capacity/color/material, and any
included accessories visible (cables, box, manuals, remotes). If text is only partly visible,
say so — don't invent. If you can't confidently ID it, ask one or two targeted questions (or for
a full-quality anchor shot) before researching. Don't research on a shaky ID.

## Step 2 — Research (sold comps)

Web-search to: confirm the exact model + specs; find recent **sold** prices (not active asks —
sold comps drive price) for the same/comparable item; note the typical sold range and the
condition those sold in; flag rarity, demand, discontinuation, or known defects/recalls that
move value. If sold data is thin, price off the closest comparable and say so. Don't fabricate a
precise number you can't support.

## Step 3 — Condition

Pick an eBay condition: **New / New other / Open box / Used / For parts or not working**. For
**Used**, add a sub-grade (Like New / Very Good / Good / Acceptable). List every visible flaw —
scratches, dents, scuffs, fading, missing parts, cracks, fraying. Overgrading causes returns and
bad feedback; if a surface isn't clearly shown, note it as "verify" rather than assuming clean.

## Step 4 — Assemble the listing payload

Build a JSON payload `list.js` consumes. Keep prose tight — buyers skim. Anything you omit that
has a config default (format, startingBid, durationDays, shipping service, categoryId hints) is
filled in from `ebay-lister.config.json`.

```json
{
  "title": "Brand Model Key-Spec Condition  (<=80 chars, keyword front-loaded, no L@@K/WOW/emoji)",
  "categoryQuery": "short keywords used to find the eBay category, e.g. 'apple iphone 11'",
  "categoryId": 139973,               // OPTIONAL but recommended — pins the category. 139973 = Video Games (prevents landing in "Cases & Boxes")
  "condition": "Used",
  "conditionGrade": "Very Good",
  "conditionNotes": "Light scuffs on bottom edge; screen clean; no cracks.",
  "format": "auction",                // omit to use the config default
  "durationDays": 7,                  // OPTIONAL auction length (1/3/5/7/10); omit for the config default
  "startingBid": 0.99,                // auctions need one; omit for the config default
  "price": 110.50,                    // optional Buy It Now alongside the auction (must be >=30% above startingBid)
  "itemSpecifics": {                  // key/value; fill every one you know
    "Brand": "Apple",
    "Model": "iPhone 11",
    "MPN": "...",
    "Color": "Red",
    "Storage Capacity": "64 GB"
  },
  "description": "2-4 short factual paragraphs: what it is + specs; condition incl. wear; what's included; relevant notes (smoke-free etc. ONLY if the seller confirmed they apply).",
  "shipping": { "weightLb": 0, "weightOz": 3, "lengthIn": 6, "widthIn": 4, "heightIn": 1 },
  "photos": ["/abs/path/anchor.jpg", "...anchor first..."],
  "draftId": "1234567890123"          // OPTIONAL — same as --draft-id: resume this draft instead of creating a new one
}
```

**Category — pass `categoryId` when you can.** eBay's category step is the one most likely to
stall. Add `"categoryId": "<id>"` so `list.js` selects it deterministically, or put a
keyword → id entry in `categoryIds` in the config and it gets applied automatically. Common ones:
`18871` = Cameras & Photo > Memory Cards (SD/microSD), `51071` = USB Flash Drives,
`171485` = Cell Phones & Smartphones, `139973` = Video Game Consoles. If you don't know it, omit
it — `list.js` falls back to "Continue without match", and if that fails it returns a
**`STUCK_AT=category`** report (see Step 5) listing the on-screen category radios so you can pick
one and re-run.

Field rules:
- **Title** <=80 chars, keyword-optimized, Brand + Model + Key Spec + Condition; include the model
  number if buyers search it. No ALL CAPS, no "L@@K"/"WOW", no emoji spam.
- **Item specifics** — fill every field you can determine; eBay will ask for category-specific
  ones (Storage Capacity, Screen Size, Material, Connectivity, etc.). Mark anything you couldn't
  determine in `conditionNotes`/description as "verify".
- **Price** — back it with the Step-2 comps in your summary; note auction vs fixed and why.
- **Shipping** — rough weight + dimensions from the item.

## Step 5 — Fill eBay and PUBLISH

Write the payload to a temp file and run `list.js`:

```bash
# normal flow — publishes the listing
node list.js --payload-file /tmp/ebay-payload.json --mode publish

# resume the draft you already created instead of starting a new one
node list.js --payload-file /tmp/ebay-payload.json --mode publish --draft-id 1234567890123
```

- **Always `--dry-run` first** the very first time (or whenever unsure): it validates the payload,
  checks every photo path exists, prints the effective config, and confirms CDP/Chrome
  reachability — without touching eBay.
- `--mode publish` walks eBay's prelist → listing form, uploads photos, fills the essentials, then
  clicks **List it**. On success it prints `PUBLISHED_URL=https://www.ebay.com/itm/<id>`.
- `--mode draft` clicks **Save for later** and prints `DRAFT_URL=<url>`; use it when the seller
  wants to review before going live.

**`--draft-id` — resume, don't duplicate.** Every prelist walk creates a NEW eBay draft, which is
why re-running a blocked listing used to leave a trail of duplicates. `list.js` prints
`DRAFT_ID=<id>` on every run: pass it back as `--draft-id <id>` (or `draftId` in the payload) and
the script goes straight to that draft's form, skips the prelist entirely, skips re-uploading
photos the draft already has, fills what's changed, and publishes. **Any re-run after a
`PUBLISH_BLOCKED` or a `DRAFT_URL` should use `--draft-id`.** If the id is wrong or expired it
stops with `STUCK_AT=draft-resume` rather than silently creating yet another draft.

**Format defaults live in the config**, not here: `format.default` (auction or fixed),
`format.startingBid`, `format.durationDays`. The shipped default is an auction with a low starting
bid plus an optional Buy It Now `price` (which must be >=30% above the starting bid).

**Fill only the ESSENTIALS — let eBay demand the rest.** Put in the payload: `title`, `photos`,
`condition` (+ `conditionGrade` for graded categories like video games), the price/format fields,
`description`, `shipping`, and only the item specifics you actually know. When `list.js` clicks
"List it", eBay validates and the recovery loop fills any genuinely required field from the
payload and retries. Over-stuffing specifics just burns time on fields eBay doesn't require.

**Publish-time recovery (automatic).** On `--mode publish`, `list.js` loops: List it → if eBay
blocks on a missing required field it reads the inline errors (matching eBay's exact
"The item specific &lt;Aspect&gt; is missing" wording, so it doesn't chase character counters or
field adornments), fills what it can from the payload, and retries (up to 3x). If it still can't
satisfy a required field it has **no payload data for**, it does NOT publish junk — it saves a
draft and prints `PUBLISH_BLOCKED=[...unresolved errors...]` followed by `DRAFT_URL=<url>`.
Surface the specific missing field(s) to the seller, then re-run with `--draft-id`.

**Stuck handoff (never hangs).** If `list.js` can't get past a step it bails within ~8s and prints
a structured report:

```
STUCK_AT=condition-select | product-match | prelist | draft-resume | form-not-ready
STUCK_URL=...          STUCK_SCREENSHOT=.../debug-stuck.png
STUCK_CATEGORIES=[{"value":"139973","label":"Video Games & Consoles > Video Games"}, ...]
STUCK_CONDITIONS=[{"value":"2750","label":"Like New"}, ...]   STUCK_BUTTONS=[...]
```

The prelist auto-navigates category → product-match → condition on its own (and handles the two
condition schemes: standard Used=3000 vs graded Like New=2750/Very Good=4000/...). If it *still*
stalls on a category ambiguity, read `STUCK_CATEGORIES`, add the right `value` to the payload as
`categoryId`, and re-run — with `--draft-id` if a draft already exists.

**Shipping gotcha:** weight must be WHOLE pounds + ounces (`weightLb:0, weightOz:3`) — a fractional
`weightLb` like 0.1 silently fails (the "Package size" error). A single run uploads each photo once.
**Best Offer** follows the config: `"bestOffer": "off"` (default) forces the toggle off and scrubs
offer language out of the description; `"leave"` keeps whatever eBay defaults to.

## Step 6 — Report

Report back:
- On success: the **live item link** (`PUBLISHED_URL` -> ebay.com/itm/&lt;id&gt;) — "it's live".
- On fallback (`PUBLISH_BLOCKED`): it saved a draft instead — give the `DRAFT_URL`, the `DRAFT_ID`
  to resume with, and the **exact missing field(s)** that need finishing before it can go live.
- A one-line recap: title, price + the comp reasoning, condition grade, format.
- Any **red flags**: fields to verify, missing buyer-expected angles to re-photograph, or category
  restrictions (brands/categories requiring authentication, prohibited/restricted/recalled items).

To push that report somewhere (a chat bot, ntfy, `mail`), set `notifyCommand` in
`ebay-lister.config.json` — `list.js` pipes the outcome to it on stdin (and as
`$EBAY_LISTER_MESSAGE`) after a publish, a draft save, or a block. Default is no notification at
all; this skill never messages anyone unless you configure it to.

## Credentials / login

`list.js` attaches to an already-running Chrome over CDP (`cdpUrl` in the config, default
`http://127.0.0.1:18800`) — so it relies on that Chrome already being **logged into eBay**. If it
isn't, `list.js` prints `EBAY_NOT_LOGGED_IN`; log into eBay once in that Chrome window, then
re-run. No eBay password is stored by this skill.

## Notes on tone/judgment

- Don't pad — every field earns its place. Honesty over optimism; an accurate listing sells
  faster with fewer returns than an inflated one.
- If the seller pushes back on a grade or price, explain from the comps rather than just deferring.
- Flag missing angles a buyer expects (all sides of a watch, electronics powered on) in red flags.

## Files

- `SKILL.md` — this file (the brain + workflow).
- `list.js` — CDP/Playwright form-filler. `--payload-file`, `--mode draft|publish`, `--draft-id`,
  `--dry-run`, `--debug`.
- `ebay-lister.config.example.json` — template for your local `ebay-lister.config.json`.
- `package.json` — depends on `playwright-core`.
- `README.md` — engineering notes: the real eBay DOM flow and every gotcha cracked so far.
- `runs.log` — append-only record of every fill attempt (created on first run).
