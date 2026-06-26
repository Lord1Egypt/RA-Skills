# Investor Network Workflow

Produce this as the second file in the Bottom-Up Suite. It shows who is funding the landscape and where capital is concentrated or absent.

> **Data disclosure:** This workflow sends organization IDs to the AlphaLens API and fetches favicons from Google's public service. Confirm with the user before running enrichment on more than 20 organizations.

---

## Step 1 — Fetch funding data and favicons for all indexed companies in parallel

```bash
WORKDIR=$(mktemp -d)
API="https://api-production.alphalens.ai"

# Fetch funding for each company
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{org_id1}/funding" > $WORKDIR/fn1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{org_id2}/funding" > $WORKDIR/fn2.json &
# ... one call per company in the same block ...

# Base64-encode each company favicon in the same block
curl -s "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://{domain1}&size=128" | base64 -w0 > $WORKDIR/favicon_domain1.txt &
curl -s "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://{domain2}&size=128" | base64 -w0 > $WORKDIR/favicon_domain2.txt &
# ... one curl | base64 per company in the same block ...

wait
```

Only fetch favicons for public domains returned by AlphaLens — never for internal or private hostnames.

The response shape is:
```json
{
  "funding_rounds": [
    {
      "id": 0,
      "raised_date": "2026-03-25",
      "raised_amount_usd": 0,
      "investment_stage": "string",
      "investments": [
        { "investor_details": { "name": "string", "url": "string", "is_organization": true, "image_url": "string" } }
      ]
    }
  ],
  "total_funding_usd": 0,
  "index_status": "string"
}
```

Skip companies still pending/indexing — they won't have funding data yet. If a favicon curl returns empty, use a coloured letter avatar instead.

---

## Step 2 — Extract and deduplicate investors

Parse each funding round's `investments` array:
- Skip entries where `investor_details.name` is null (anonymous investors)
- Deduplicate: one edge per unique (investor, company) pair — a single investor appearing across multiple rounds of the same company counts as one link
- Track `count` per investor (number of distinct companies they've backed in this landscape)
- Preserve `investment_stage` on each link for colouring

---

## Step 3 — Build the D3 force-directed network graph

Create a standalone HTML file. The HTML is fully self-contained — favicons are base64-encoded inline, no proxy required.

**Node types:**
- **Company nodes**: larger circles, coloured by cluster (same palette as the market map), with the favicon embedded as a base64 data URI. Size optionally scaled by `total_funding_usd`. Anchor company gets gold border + glow.
- **Investor nodes**: smaller circles, grey. Size scales with `count` (number of companies backed). Multi-company investors are darker with a name label; solo investors are light grey with just an initial.

**Edge styling:**
- Colour edges by the target company's cluster colour for visual association
- Opacity ~0.35 so the graph doesn't get cluttered

**Force simulation setup (key settings):**
```js
d3.forceSimulation(nodes)
  .force('link', d3.forceLink(edges).id(d => d.nodeId)
    .distance(d => src.count >= 2 ? 80 : 40)
    .strength(d => src.count >= 2 ? 0.5 : 1.0))
  .force('charge', d3.forceManyBody()
    .strength(d => d.type === 'company' ? -400 : (d.count >= 2 ? -50 : -15)))
  .force('center', d3.forceCenter(width/2, height/2).strength(0.04))
  .force('boundX', d3.forceX(width/2).strength(0.08))
  .force('boundY', d3.forceY(height/2).strength(0.08))
  .force('collision', d3.forceCollide().radius(d => r(d) + (d.type === 'investor' ? 2 : 8)))
```

**Hard-clamp in tick handler** — this is critical to keep all nodes in view without panning:
```js
.on('tick', () => {
  nodes.forEach(d => {
    d.x = Math.max(PAD + r(d), Math.min(width - PAD - r(d), d.x));
    d.y = Math.max(PAD + r(d), Math.min(height - PAD - r(d), d.y));
  });
  // update link and node positions...
})
```

---

## Step 4 — Controls

Add these interactive controls in the header:
1. **Cluster filter buttons** — one per cluster, same colours as market map. Clicking one shows only that cluster's companies + their investors, hiding everything else.
2. **"Hide Solo Investors" toggle** — removes all investor nodes with `count === 1`, leaving only cross-portfolio investors. This is the most analytically valuable view: it immediately reveals which investors have placed multiple bets in the space.
3. Stats counter (bottom-right): total companies, total investors, total links, cross-portfolio count.

---

## Step 5 — Interaction

- **Hover any node**: dims all unconnected nodes and edges; shows tooltip with name, cluster/count, portfolio companies, total funding
- **Click a company node**: opens its AlphaLens profile (`https://app.alphalens.ai/discover/organization/{active_domain}`)
- **Drag nodes**: pinned while dragging, released on mouseup
- **Scroll to zoom / drag to pan**: standard D3 zoom behaviour
- **Export PNG**: serialise the SVG and draw to canvas at 2× DPR

---

## What to look for and narrate

After building the network, share these insights with the user:
- **Cross-portfolio investors**: who has backed 2+ companies? Are they government (NASA, SBIR) or private VCs? Named private cross-portfolio investors are the most interesting signal.
- **Isolated companies**: companies with no investor halos are pre-seed, grant-funded, or defence-contract-only — a different risk/return profile.
- **Geographic capital clusters**: do US, European, and Asian companies draw from entirely separate investor pools? No shared investors = fragmented ecosystem.
- **Funding density**: large halos = many investors and rounds; sparse halos = early or unfunded. This directly tells you where market validation has and hasn't happened.

---

## Common pitfalls

- **Many investors, low signal**: with 150+ investors most will only appear once. "Hide Solo Investors" is the go-to view for insight; always offer it as the default framing.
- **Data artefacts**: "Crunchbase" sometimes appears as an investor (it's a data source, not an investor). Filter or ignore entries whose name matches known data platforms.
- **Individuals vs. organisations**: `is_organization: false` entries can be angel investors (legitimate) or data noise. Keep them — they often reveal founder-to-founder investment patterns.
- **Pending companies have no funding data**: only call the funding endpoint for indexed companies.
- **Viewport containment**: always hard-clamp `d.x` and `d.y` in the tick handler in addition to using boundary forces — forces alone are not sufficient to guarantee all nodes stay in view.
- **Empty favicon**: if a domain has no favicon, the curl returns empty — always provide a coloured letter avatar as a fallback.
