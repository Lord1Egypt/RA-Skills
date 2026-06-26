# Org-Level Market Map Workflow

Use this when the user asks for a quick competitive landscape or "market map" and has NOT requested a bottom-up analysis. This is simpler and faster than the product-centric approach — it produces a single-page cluster grid based on organization-level similarity.

> **Data disclosure:** This workflow sends organization IDs and domains to the AlphaLens API and fetches favicons from Google's public service. Confirm with the user before running enrichment on more than 20 organizations.

---

## Step 1 — Resolve the anchor company

- Resolve via `GET /api/v1/entities/organizations/by-domain/{domain}`.
- Note its `organization_id`, `active_domain`, `venture_organization_index_status`, and `logo_url`.

---

## Step 2 — Fan out AlphaLens similarity searches — ALL CALLS IN PARALLEL

**Critical rule: never make AlphaLens API calls sequentially. Always use `curl ... &` with `wait`.**

```bash
WORKDIR=$(mktemp -d)
API="https://api-production.alphalens.ai"

# Fire org-level similarity + all secondary anchors simultaneously
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{anchor_id}/similar?limit=50&is_headquarters=true" > $WORKDIR/r_anchor.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/by-domain/competitor1.com" > $WORKDIR/r_c1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/by-domain/competitor2.com" > $WORKDIR/r_c2.json &
# ... all 20-30 calls in the same block ...

# Base64-encode each company favicon during the fan-out
curl -s "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://{domain1}&size=128" | base64 -w0 > $WORKDIR/favicon_domain1.txt &
curl -s "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://{domain2}&size=128" | base64 -w0 > $WORKDIR/favicon_domain2.txt &
# ... one curl | base64 per company in the same block ...

wait   # collect all results before reading
```

Only fetch favicons for public domains returned by AlphaLens — never for internal or private hostnames.

This turns a 60-second sequential loop into a 2–3 second parallel sweep. Never use a for-loop over sequential curl calls.

- Run `GET /api/v1/search/organizations/{organization_id}/similar?limit=50&is_headquarters=true` from the anchor.
- Immediately use the top returned companies as **secondary anchors** and fan out again — companies like risk/compliance, alt data, and niche CRMs only appear in the second ring.
- Always paginate (`offset`) on promising anchors rather than stopping at page 1. Missing obvious players is almost always a pagination issue, not a data gap.
- Use `limit=50` — the default of 24 misses too much.
- If a favicon curl returns empty (no favicon for that domain), use a letter avatar fallback instead.

---

## Step 3 — Supplement with your own knowledge

After the AlphaLens fan-out, apply your own knowledge of the space to identify companies that *should* be on the map but weren't returned. For each one:

1. **Check AlphaLens** via `GET /api/v1/entities/organizations/by-domain/{domain}`.
   - If the response is empty, the lookup itself triggers indexing — include the company with `.pending` styling.
   - Check `venture_organization_index_status`: `indexed` | `indexing` | `indexing_failed`.
   - If `indexing_failed`, include with `.pending` styling.
   - If `indexed`, include at full opacity.

2. Fetch its favicon in the same parallel block above.

---

## Step 4 — Cluster the results

Group companies by shared characteristics (business model, buyer, use case, go-to-market). Aim for 5–10 named clusters. Never use "Other" as a cluster name. Good cluster names describe the buyer outcome, not the technology (e.g. "AI Due Diligence Platforms" not "AI Tools").

Do **not** show approximate company counts in cluster subtitles — they imply the map is exhaustive when it's curated.

---

## Step 5 — Render the HTML market map

Embed each company's favicon as a base64 data URI:

```html
<!-- Use base64 favicon so the HTML is fully self-contained -->
<img src="data:image/png;base64,$(cat $WORKDIR/favicon_domain1.txt)" alt="">

<!-- Letter avatar fallback for missing favicons -->
<div class="logo-wrap" style="width:44px;height:44px;border-radius:8px;background:hsl(H,52%,56%);
  display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:16px;">
  A
</div>
```

**Design rules (non-negotiable):**
- Always **light mode** — `background: #f7f8fc`, dark text. **Never dark mode on any page, including the investor network graph.** Dark mode breaks favicon legibility and makes the graph unreadable.
- **No emojis in tab labels, cluster titles, section headers, or button text.** Use plain text only.
- CSS 3-column grid. Each cluster: distinct coloured border, **white background (`#fff`) — no tinted or pastel fills**. Good border palette: red/amber/yellow/blue/green/purple/teal/grey/pink.
- Each company: `<a class="company" href="https://app.alphalens.ai/discover/organization/{active_domain}" target="_blank">` wrapping a 44×44px white logo tile + name below.
- **Anchor company**: gold border + glow (`border: 2px solid #d69e2e; box-shadow: 0 0 10px rgba(214,158,46,0.3)`).
- **Indexed companies**: full opacity, solid border.
- **Indexing / pending companies** (just triggered or reindexing): `opacity: 0.65`, dashed border, italic name.
- **indexing_failed companies**: `opacity: 0.5`, dashed grey border, `?` suffix on name.
- Legend at bottom. No company counts in subtitles.
- "Click any logo to open its AlphaLens profile" in the subtitle.

---

## Step 6 — PDF export

The HTML is fully self-contained (favicons embedded as base64), so `html2pdf.js` works without any proxy or CORS issues:

```js
html2pdf().set({
  margin: 12,
  filename: 'market-map.pdf',
  image: { type: 'jpeg', quality: 0.98 },
  html2canvas: {
    scale: 2, useCORS: false, allowTaint: false,
    backgroundColor: '#f7f8fc',
    windowWidth: Math.max(document.documentElement.scrollWidth, 1560),
    scrollX: 0, scrollY: 0
  },
  jsPDF: { unit: 'mm', format: 'a2', orientation: 'landscape' },
  pagebreak: { mode: 'avoid-all' }
}).from(document.body).save();
```
- Set `visibility: hidden` (not `display: none`) on the export button before rendering — hides it from the PDF without shifting layout.
- A2 landscape gives enough room for a 3-column layout without clipping.

---

## Common pitfalls

- **Domain mismatch**: AlphaLens `active_domain` ≠ public domain (e.g. Ironclad → `thisisironclad.com`). Use AlphaLens domain for the profile link.
- **Duplicate entries**: looking up `robin.ai` when `robinai.com` already exists creates a duplicate. Always check by name if the domain lookup returns a brand-new ID.
- **Pagination**: missing obvious players is almost always a page 1 limitation, not absence from AlphaLens. Paginate with `offset` and use secondary anchors.
- **Empty favicon**: if a domain has no favicon, `curl | base64` returns empty — always provide the letter avatar as a fallback.
