# Peer Benchmark Workflow

Produce this as the third file in the Bottom-Up Suite. It gives a side-by-side picture of the anchor company against its closest peers: headcount trajectory, funding scale, capital efficiency, and qualitative positioning.

> **Data disclosure:** This workflow sends organization IDs to the AlphaLens API and fetches favicons from Google's public service.

---

## Step 1 — Identify 5 peers by size similarity

Run the anchor's org similarity search with `limit=30` and filter for companies with similar employee count (within ~3× of the anchor). Prefer companies that:
- Operate in the same product category (not just adjacent)
- Have a different story arc (one hypergrowth, one contracting, one bootstrapped) — contrast makes the chart readable
- Are indexed (not pending) so growth data is available

```bash
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{anchor_id}/similar?limit=30&is_headquarters=true"
```

---

## Step 2 — Check growth-metrics availability before committing to a peer

Some indexed companies have no LinkedIn headcount tracking. Always verify before choosing:

```bash
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{id}/growth-metrics" | jq '{hc:.headcount_metrics.headcount, ts_count:(.headcount_metrics.time_series|length), first:.headcount_metrics.time_series[0]}'
```

If `ts_count` is 0, the company has no headcount history — swap it for one that does. **Only include companies with `ts_count > 0`** in the benchmark.

> **Important**: growth-metrics data is updated asynchronously. If a company returns `ts_count: 0` on the first call but the user says they can see headcount data on the AlphaLens platform, **re-fetch it** — it may have synced since your cached call.

---

## Step 3 — Parallel fetch: growth metrics + funding for all peers

```bash
WORKDIR=$(mktemp -d)
API="https://api-production.alphalens.ai"

# Growth metrics for anchor + all peers
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{anchor_id}/growth-metrics" > $WORKDIR/gm_anchor.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{peer1_id}/growth-metrics"  > $WORKDIR/gm_peer1.json &
# ... all peers in same block ...

# Funding for anchor + all peers (already fetched for investor network — reuse)
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{anchor_id}/funding" > $WORKDIR/fn_anchor.json &
# ...
wait
```

**Growth-metrics response shape:**
```json
{
  "headcount_metrics": {
    "headcount": 232,
    "time_series": [
      { "date": "2021-02-01", "value": 84 },
      { "date": "2021-02-08", "value": 84 }
      // weekly data going back to ~2021
    ]
  },
  "linkedin_follower_metrics": { "followers": 0, "time_series": [] },
  "open_jobs_metrics": { "open_jobs": 12 },
  "web_traffic_metrics": {}
}
```

Downsample the weekly time series to **monthly** (take the last value per month) before passing to the chart — weekly is too noisy for a multi-line comparison.

---

## Step 4 — Compute derived metrics

For each company:

| Metric | Formula |
|---|---|
| **Growth %** | `(hc_last − hc_first) / hc_first × 100` (from earliest data point) |
| **Capital efficiency** | `total_funding_usd / current_headcount` ($/head — lower = more efficient) |
| **Momentum tag** | `> +20%` = growing · `-20% to +20%` = flat · `< -20%` = contracting |

---

## Step 5 — Build the benchmark page (Chart.js)

Use **Chart.js** (not D3) — simpler for static comparison charts. Load from CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

**Six visual components:**

**1. Headcount growth line chart** — all peers on a shared date axis, each line in its cluster colour. Use `spanGaps: true`, `tension: 0.35`, `pointRadius: 0`. Anchor company gets `borderWidth: 2.5`, others `1.5`.

**2. Current headcount horizontal bar** — `indexAxis: 'y'`, one bar per company, colours match.

**3. Growth % horizontal bar** — same layout. Bars for declining companies use a red tint (`#fc8181`) regardless of their cluster colour — makes contraction visually obvious.

**4. Total funding raised horizontal bar** — amounts in USD, tick labels formatted as `$XM` or `$XB`.

**5. Capital efficiency custom HTML bars** (not Chart.js) — render as CSS `<div>` bars with `width: N%` driven by each company's ratio vs. the max. Skip bootstrapped/PE-owned companies (they have $0 funding so the metric is meaningless). Add a note explaining what "lower = more efficient" means.

**6. Funding rounds timeline** — HTML/CSS dot plot. Each row = one company, each dot = one round. `left: N%` is derived from `(round_date − min_date) / date_span`. Dot size scales with `sqrt(amount / max_amount) × 28px`. Dot colour = stage (seed=green, Series A=blue, Series B=purple, etc.). Year tick labels below.

---

## Step 6 — Qualitative positioning cards

One card per company with three structured fields:

| Field | What to write |
|---|---|
| **Core Data Asset** | The unique data or proprietary signal the company owns that others can't easily replicate |
| **Who Buys It** | Buyer persona — role, industry, use case |
| **Verdict** | 2–3 sentence narrative: what they own, where they're heading, and how they relate to the anchor (direct threat / complement / adjacent) |

Base this on your training knowledge of each company plus the AlphaLens `organization_description` field. Keep each field to 2–4 sentences max.

---

## Step 7 — Company header cards

One card per company at the top of the page showing:
- Letter avatar (CSS-only, coloured by cluster) + name + HQ city + founded year
- Current headcount (large, in cluster colour)
- Total funding raised
- Growth badge: `+176% since 2021-02` / `-52% since 2023-02` / `+3% since 2023-06`

Anchor company card gets a gold border + subtle glow.

---

## What to look for and narrate

After building the benchmark, share these reads with the user:

- **Headcount divergence**: which peers grew together until a certain date, then separated? That inflection usually marks a fundraise or a product pivot.
- **The contracting peer**: if one peer is shrinking (FreightWaves-style), explain why — overextension, capital burn, market shift. It's cautionary context for the anchor.
- **Capital efficiency outlier**: the company that built the most headcount on the least funding is usually either bootstrapped (profitable from day one) or operating in a lower-cost labour market. Both are interesting signals.
- **The escaped peer**: a company that started in the same category but has grown 3–5× larger likely expanded into an adjacent category (e.g. Kpler: freight intelligence → commodity trading intelligence). This is either an acquisition risk or a product roadmap signal for the anchor.
- **Funding timeline gaps**: peers who last raised 3+ years ago and haven't grown headcount since are likely in a hold pattern — either profitable and not needing capital, or struggling to raise.

---

## Common pitfalls

- **Stale growth-metrics cache**: if `ts_count: 0` on first fetch, re-fetch before excluding a company. The API updates asynchronously and data often appears on a second call.
- **Mixed date ranges**: companies start tracking at different dates (some from 2021, some from 2023). Always note the start date on the growth badge — `+10% since 2021` is very different from `+10% since 2024`.
- **Bootstrapped vs. unfunded**: a company with `total_funding: 0` might be profitable/PE-owned (AXSMarine) or simply pre-raise. Check `funding_rounds` length — zero rounds + old founding year = likely profitable incumbent.
- **Company cards overflowing**: with 6 companies, cards can overflow on narrow viewports. Use `overflow-x: auto` on the cards container rather than forcing them into a grid.
