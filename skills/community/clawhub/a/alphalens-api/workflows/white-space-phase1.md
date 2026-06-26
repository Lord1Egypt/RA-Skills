# Phase 1: Saturation Map (The Mirror Test)

**Purpose:** Establish the red ocean. Map how the market currently perceives the anchor's products by running product-level similarity searches and analyzing competitive density.

> **Data disclosure:** This workflow sends organization/product IDs to the AlphaLens API and fetches favicons from Google's public service.

---

## Step 1a — Parallel 4-ring fan-out for each product

Run all four signal sources in a **single parallel bash block** — never sequentially. This mirrors the approach in [`market-map-product.md`](market-map-product.md) but adapted for white space density analysis.

```bash
WORKDIR=$(mktemp -d)
API="https://api-production.alphalens.ai"

# Ring 1: product-level similarity for each product (page 1 + page 2)
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid1}/similar?limit=50&offset=0&is_headquarters=true" > $WORKDIR/p1_prod0.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid1}/similar?limit=50&offset=50&is_headquarters=true" > $WORKDIR/p1_prod50.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid2}/similar?limit=50&offset=0&is_headquarters=true" > $WORKDIR/p2_prod0.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid2}/similar?limit=50&offset=50&is_headquarters=true" > $WORKDIR/p2_prod50.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid3}/similar?limit=50&offset=0&is_headquarters=true" > $WORKDIR/p3_prod0.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid3}/similar?limit=50&offset=50&is_headquarters=true" > $WORKDIR/p3_prod50.json &

# Ring 2: org-level similarity from anchor (page 1 + page 2)
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{org_id}/similar?limit=50&offset=0&is_headquarters=true" > $WORKDIR/org0.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{org_id}/similar?limit=50&offset=50&is_headquarters=true" > $WORKDIR/org50.json &

# Ring 3: known player sweep — domains you know in this space (20-40 domains)
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/by-domain/known1.com" > $WORKDIR/d1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/by-domain/known2.com" > $WORKDIR/d2.json &
# ... all known domains in the same block ...

# Ring 4: org similarity ring 2 — top 5 orgs from Ring 2, run their similarity
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{ring2_top1_id}/similar?limit=50&is_headquarters=true" > $WORKDIR/r2_1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{ring2_top2_id}/similar?limit=50&is_headquarters=true" > $WORKDIR/r2_2.json &

# Base64-encode company favicons in the same block
curl -s "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://{domain}&size=128" | base64 -w0 > $WORKDIR/favicon_domain.txt &
# ... one per domain, only for public domains returned by AlphaLens ...

wait
```

> **Why 4 rings?** Product similarity catches niche product lines inside large orgs. Org similarity ring 1 catches direct competitors. Known player sweep catches established names too large/small for similarity. Org similarity ring 2 catches niche players only reachable by pivoting through ring 1.
>
> **Why offset=50?** If page 2 (offset=50) returns quality matches, the competitive cluster is dense. Empty or low-quality page 2 = narrow cluster. This is the saturation density signal.

**Only fetch favicons for public domains returned by AlphaLens** — never for internal or private hostnames. If a favicon curl returns empty, use a CSS letter avatar fallback.

---

## Step 1b — Supplement with own knowledge (provenance-labeled)

After the AlphaLens fan-out, apply your own knowledge of the space to identify companies that *should* appear in the saturation map but weren't returned. For each one:

1. **Check AlphaLens** via `GET /api/v1/entities/organizations/by-domain/{domain}`.
   - If the response is empty, the lookup itself triggers indexing — include the company with `.agent-knowledge` styling (distinct from `.pending` which means indexing in progress).
   - Check `venture_organization_index_status`: `indexed` | `indexing` | `indexing_failed`.
   - If `indexing_failed`, include with `.agent-knowledge` styling.
   - If `indexed`, include at full opacity.

2. Fetch its favicon in the same parallel block as other favicons.

> **Provenance notice:** Companies added in this step come from the agent's own knowledge, not from AlphaLens. Always use `.agent-knowledge` styling (e.g., dashed border, italic label) so output viewers can distinguish AlphaLens-sourced data from agent-sourced additions. This step is critical for white space analysis: if you know of a company that *should* be in a crowded cluster but AlphaLens doesn't return it, that affects your saturation classification. A cluster that looks sparse in AlphaLens may actually be dense when supplemented with your knowledge.

---

## Step 1c — LLM Reasoning: Saturation Classification

For each product, analyze the combined results (page 1 + page 2):

**Inputs to LLM:**
- Total unique competitors returned
- Cosine distance distribution (mean, median, min, max)
- Quality of competitors: are they well-funded, recently raised, actively hiring?
- Page 2 density: how many quality matches appear on the second page?

**LLM Task — classify each product's saturation:**

| Signal | Classification |
|---|---|
| 50+ results on page 1, low mean cosine distance (< 0.06), page 2 also dense | **Red Ocean** — crowded, high direct competition |
| 20-49 results on page 1, moderate cosine distance (0.06–0.10), page 2 sparse | **Yellow Ocean** — defined market, some room |
| < 20 results on page 1, high cosine distance (> 0.10), page 2 near-empty | **Green Ocean** — sparse, potential white space |
| Zero results | **Empty** — no AlphaLens-indexed competitors in this product space |

Also note: are the competitors **vertically specialized** (same ICP) or **horizontally generic** (cross-industry tools)? Generic horizontal competitors are less threatening — the true red ocean is vertical specialization.

**Confidence level:** Assign High/Medium/Low confidence based on how definitive the signal is.

---

## Step 1d — Render Saturation Map

Build a simple HTML heatmap table — one row per product, with saturation color coding:

```html
<div class="saturation-map">
  <h3>Phase 1 — Saturation Map</h3>
  <table class="saturation-table">
    <thead>
      <tr><th>Product</th><th>Competitors (Page 1)</th><th>Page 2 Density</th><th>Classification</th><th>Confidence</th></tr>
    </thead>
    <tbody>
      <tr data-product="product1" class="ocean-red">
        <td>Product A</td>
        <td>47</td>
        <td>Dense</td>
        <td>Red Ocean</td>
        <td>High</td>
      </tr>
      <!-- ... -->
    </tbody>
  </table>
</div>
```

```css
.ocean-red    { background: #fed7d7; color: #c53030; }
.ocean-yellow { background: #fefcbf; color: #744210; }
.ocean-green  { background: #c6f6d5; color: #22543d; }
.ocean-empty  { background: #e2e8f0; color: #4a5568; }
.ocean-unknown { background: #bee3f8; color: #2c5282; }
```

Attach this section into the main `white-space.md` output under `<section id="phase1">`.
