# Lookbook acceptance checklist

The single source of truth for "is this lookbook ready to share with the customer." Every `html` / `html-cart` / `ppt` lookbook clears these gates **before** the agent emits the URL or filename. The checklist is operationalized as `scripts/validate-lookbook.py` — run it; if it exits non-zero, fix the failure rather than narrating around it.

## Local checks (run against the deploy directory before upload)

| # | Check | Pass criterion |
|---|---|---|
| L1 | `index.html` exists | File present, ≥ 4 KB |
| L2 | All product links absolute + on-brand | Every `<a href>` matching `/products/` resolves to `https://www.buckmason.com/products/<slug>` |
| L3 | Prices present per piece | At least one `$\d+` token within each `.piece` block |
| L4 | Stock lines present per piece | Each `.piece` carries an `In stock` / `Low (N)` / `Out of stock` substring (the bucket strings from `/mcp/buckmason/stock`) |
| L5 | AI try-on disclosure present (premium tier only) | Page contains "AI-generated" or "AI try-on" text, in cover or footer — required when any look hero came from gpt-image-2 |
| L6 | OG meta tags present + absolute | `og:url`, `og:image`, `twitter:image` each resolve to URLs starting with `https://`, **not** containing `{{ABSOLUTE_PAGE_URL}}` / `{{ABSOLUTE_OG_IMAGE_URL}}` placeholders |
| L7 | `og.jpg` present + correctly sized (multi-file deploys) | File exists in deploy dir, ~1200×630, `.jpg` mimetype, < 500 KB |
| L8 | Per-piece checkboxes carry the full data set (`html-cart` only) | Every `.piece input[type="checkbox"]` has `data-name`, `data-size`, `data-sku`, `data-qty`, `data-price-cents` |
| L9 | Subtotals and look totals match piece prices | Per-look total equals the sum of piece prices in that look (rendered via JS only — verify the data attrs sum cleanly) |
| L10 | No broken inline references | No `data-fullsize=""`, no `<img src="">`, no `href="#"` placeholders |

## Deployed checks (run after `wrangler pages deploy` against the live URL)

| # | Check | Pass criterion |
|---|---|---|
| D1 | Page returns HTTP 200 | `curl -sI <page-url>` first line is `HTTP/2 200` (or `HTTP/1.1 200 OK`) |
| D2 | `og.jpg` returns HTTP 200 + `image/jpeg` | `curl -sI <og-url>` shows `200` + `content-type: image/jpeg` |
| D3 | Each `look<N>.jpg` returns 200 (multi-file deploys) | One per look section; if any 404s, redeploy with the missing asset |
| D4 | Meta tags survived the deploy | The page body still contains all 13 OG/Twitter tags (no template substitution dropped them) |
| D5 | Resolved URLs in OG metadata are reachable | The `og:url` and `og:image` URLs in the served HTML themselves return 200 (catches mismatched-alias bugs where the page deployed but the OG URL points at a stale/wrong subdomain) |
| D6 | Unfurl preview works | Hit `https://www.opengraph.xyz/url/<encoded-url>` in a browser, or scrape with a `User-Agent: facebookexternalhit/1.1` and confirm the meta tags are visible |

## Warnings (non-blocking, surface to the customer if present)

| # | Warning | When |
|---|---|---|
| W1 | Hosted publicly | Any deploy to `*.pages.dev`, `*.netlify.app`, `*.vercel.app`, `*.surge.sh`, `0x0.st`, `gist.github.com` — surface "anyone with this link can view" before sending |
| W2 | Look hero is on-model, not AI try-on | When the lookbook degraded to editorial tier — say so in the agent's reply ("here's the editorial fallback — set `OPENAI_API_KEY` for AI try-on") |
| W3 | One or more pieces are out of stock | When any piece's stock label is `Out of stock` — explicit one-line note ("the X is currently out — I left it in the lookbook for context but you can't add it to a cart") |
| W4 | Low stock on any piece | When any piece is `Low (N)` — surface the count so the customer can decide |

## Failure handling

A failed local check **blocks the deploy**. The agent fixes the artifact and retries — never deploys a broken lookbook and tells the customer to ignore the broken parts.

A failed deployed check **blocks the share**. The agent either redeploys (if the failure is recoverable, e.g. og.jpg upload failed mid-flight) or surfaces the failure to the customer and offers the local file as a fallback.

The validate script returns one of:

- `0` — all checks pass; safe to share
- `1` — one or more local checks failed (block deploy)
- `2` — one or more deployed checks failed (block share)

Warnings (`W*`) never affect the exit code; they print to stderr with a `WARN:` prefix.

## Composition with other docs

- **Per-format must-haves** in `references/output-formats.md` define WHAT each piece needs (price, stock, link, total). This checklist is HOW we verify they made it through.
- **Hosting flow** in `references/hosting-options.md` describes the deploy steps. Run this checklist against the local artifact pre-deploy and against the URL post-deploy.
- **Brand style** in `references/brand-style.md` is the visual contract — it's not in this checklist (style drift is harder to assert programmatically than presence-of-link), but a layout regression that breaks the responsive grid would surface as a structural failure here.
