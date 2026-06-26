# Product-Centric Market Map Workflow

This is the market map component of the Bottom-Up Market Intelligence Suite. Use this — not the Org-Level Market Map Workflow — whenever the user asks for a "bottom-up mapping" or "deep dive".

It produces **one market map per qualifying product** on a single tabbed HTML page. Each tab has its own competitor set driven by product-level similarity, not org-level similarity. This is what makes bottom-up mappings more precise — a company with 3 products competes in 3 different spaces, and org-level similarity blurs them into one.

**Always run Step 0 first.** A raw product array almost always contains delivery channels and feature clusters masquerading as products. Mapping them wastes effort and produces noise.

> **Data disclosure:** This workflow sends organization IDs and product IDs to the AlphaLens API and fetches favicons from Google's public service. Confirm with the user before running enrichment on more than 20 organizations.

---

## Step 0 — Score and select real products (run before anything else)

Most companies in AlphaLens return 5–10 products. The majority are **delivery channels** (REST API, Chrome Extension, CRM Integrations, Bulk Data) or **feature clusters** (Proactive Sourcing as a sub-feature of a platform). These should never become their own market map.

**Scoring formula — apply to every product in the array:**

```
+40  is_primary_product: true
+10  per product_reference URL that is NOT the company homepage (dedicated solution/product page)
 +5  per distinct entry in product_target_audiences
  0  baseline

-50  product_name contains any of: api, rest, extension, bulk, integration, crm, webhook, export, sdk
-30  product_categories contains 'services' (not 'software')
-20  ALL product_references point only to the company homepage (no dedicated page)
-15  a key_feature of this product is also a key_feature of a higher-scoring product (subset signal)
```

**Decision rules:**
1. Compute score for every product
2. Keep only products with **score ≥ 20** (positive net signal)
3. Cap at **3 products maximum** — if more than 3 qualify, take the top 3 by score
4. **Pairwise distinctiveness check**: for any two qualifying products, ask — do they have >70% overlapping `product_target_audiences`? If yes, merge them into one map (they're the same product marketed twice)
5. **Job-to-be-done sanity check**: each surviving product should represent a different buyer action. If you can describe the remaining products as sequential stages of one workflow (e.g. Find → Receive → Enrich), that validates your selection

**Example — AlphaLens.ai (8 products → 3 maps):**

| Product | Score | Keep? |
|---|---|---|
| Proactive Sourcing | +55 | yes — primary, own solution page, 3 audiences |
| Inbound Deal Parsing | +55 | yes — primary, 2 solution pages, 2 audiences |
| Universal Enrichment Pipeline | +50 | yes — primary, own solution page, 3 audiences |
| Web Platform | +15 | no — below threshold; UI wrapper, homepage-only refs |
| CRM Integrations | -25 | no — "CRM" channel penalty |
| REST API v1 | -35 | no — "API/REST" channel penalty |
| Chrome Extension | -40 | no — "Extension" channel penalty |
| Bulk Data | -65 | no — "Bulk" + services category + homepage-only |

Result: **3 maps** — one per deal flow stage (Find → Receive → Enrich). The structural alignment to sequential workflow stages is the validation signal that the selection is correct.

**When NO products pass the threshold** (score ≥ 20): fall back to org-level similarity only and build a single map. The company likely hasn't been fully indexed at product level yet.

---

## Step 1 — Resolve the anchor company and fetch products

```bash
# 1a. Resolve the org
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/by-domain/{domain}"
# → get organization_id

# 1b. Get all products for that org
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{organization_id}/products?limit=20"
# → returns list of { id, product_name, product_description, is_primary_product, ... }
```

Pick the **2–3 products** that are most commercially distinct. Good signals:
- Different buyer personas (`product_target_audiences`)
- Different pricing pages or product URLs
- `is_primary_product: true` always included
- Skip minor features or add-ons that aren't standalone products

---

## Step 2 — Full 4-ring parallel fan-out (ALL calls fired simultaneously)

Run all four signal sources in a **single parallel bash block** — never sequentially.

```bash
WORKDIR=$(mktemp -d)
API="https://api-production.alphalens.ai"

# Ring 1: product-level similarity for each selected product
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid1}/similar?limit=50&is_headquarters=true" > $WORKDIR/prod1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid2}/similar?limit=50&is_headquarters=true" > $WORKDIR/prod2.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/{pid3}/similar?limit=50&is_headquarters=true" > $WORKDIR/prod3.json &

# Ring 2: org-level similarity from anchor (offset 0 + offset 50)
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{org_id}/similar?limit=50&offset=0&is_headquarters=true"  > $WORKDIR/org0.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{org_id}/similar?limit=50&offset=50&is_headquarters=true" > $WORKDIR/org50.json &

# Ring 3: domain lookups for known players (your own knowledge, 20-40 domains)
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/by-domain/known1.com" > $WORKDIR/d1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/by-domain/known2.com" > $WORKDIR/d2.json &
# ... all known domains in same block ...

# Ring 4: second-ring org similarity (top 5-8 orgs from Ring 2, run their similarity)
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{ring2_top1_id}/similar?limit=50&is_headquarters=true" > $WORKDIR/r2_1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/organizations/{ring2_top2_id}/similar?limit=50&is_headquarters=true" > $WORKDIR/r2_2.json &

# Base64-encode each company favicon in the same block
curl -s "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://{domain1}&size=128" | base64 -w0 > $WORKDIR/favicon_domain1.txt &
curl -s "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://{domain2}&size=128" | base64 -w0 > $WORKDIR/favicon_domain2.txt &
# ... one curl | base64 per company in the same block ...

wait   # ← everything lands here
```

Only fetch favicons for public domains returned by AlphaLens — never for internal or private hostnames.

**The four rings and what each catches:**

| Ring | Method | What it uniquely surfaces |
|---|---|---|
| 1 — Product similarity | `/search/products/{id}/similar` | Niche product lines inside large orgs; companies that org-level misses because their org description is too broad |
| 2 — Org similarity ring 1 | `/search/organizations/{id}/similar?limit=50&is_headquarters=true` | Direct org-level competitors; the obvious players |
| 3 — Known player sweep | `by-domain` for 20-40 domains you know | Established names that may be too large/small for similarity to surface (incumbents, emerging startups) |
| 4 — Org similarity ring 2 | `/search/organizations/{ring1_id}/similar?limit=50&is_headquarters=true` | Niche players only reachable by pivoting through a ring-1 result; almost never in ring 1 directly |

**Why product-level similarity is better than org-level for product maps:**
- Returns `product_name`, `organization_name`, `active_domain`, and cosine distance **in one call** — no second lookup needed
- Matches on product description + target audience embeddings, not just company-level embeddings
- Surfaces competitors that org-level similarity misses (niche product lines of large companies)

**Response shape** (all fields directly on each result item):
```json
{
  "product_name": "...",
  "organization_name": "...",
  "active_domain": "...",
  "organization_id": 123,
  "product_similar_cosine_distance": 0.041
}
```
Sort ascending by `product_similar_cosine_distance`. Skip result #0 (always self).

---

## Step 3 — Supplement with own knowledge (provenance-labeled)

After the product similarity fan-out, add companies you know should be there. Check each via `by-domain`, mark with `.agent-knowledge` styling (not `.pending` — that class is for AlphaLens indexing states). Always label agent-sourced companies distinctly so viewers can tell what came from AlphaLens vs. the agent's own knowledge.

---

## Step 4 — Cluster per product, then build the tabbed HTML page

**Design rules:** Follow `workflows/market-map-org.md` Step 5 exactly for the base grid, cluster styling, anchor gold border, and PDF export settings. The following additions apply specifically to the tabbed product map:

- Build **one `<section class="map-section">` per product** inside a single HTML file
- Use **tab buttons** at the top to switch between maps
- Each tab gets its own colour palette (e.g. Ocean=blues, Air=ambers, Carbon=greens)
- Anchor company appears on **every** tab with gold border
- Map sections default to `display: none`; `.active` sets `display: block`
- PDF export **must collate all tabs** into a single PDF (one page per tab). Never export only the active tab. Temporarily show all `.map-section` divs, clone them into a container, export the container, then restore original state.

```js
// Tab switcher
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.map-section').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.target).classList.add('active');
  });
});
```

HTML structure:
```html
<nav class="product-tabs">
  <button class="tab-btn active" data-target="map-product1">Product 1</button>
  <button class="tab-btn" data-target="map-product2">Product 2</button>
  <button class="tab-btn" data-target="map-product3">Product 3</button>
</nav>
<section id="map-product1" class="map-section active">...</section>
<section id="map-product2" class="map-section">...</section>
<section id="map-product3" class="map-section">...</section>
```

Map sections default to `display: none`; `.active` sets `display: block`.

---

## Common pitfalls

- **Self appears first**: the anchor company's own product is always result #0 in similarity search — skip it
- **Low cosine distance = more similar** (it's a distance, not a score) — sort ascending, take lowest values
- **Product search `?description=...` query** (free text) performs poorly vs. product ID similarity — always prefer ID-based similarity after resolving the product
- **One company, multiple products**: a competitor may appear on multiple tabs if they have separate products for each space — that's correct, don't deduplicate across tabs
- **`GET /api/v1/entities/organizations/{id}/products`** only returns products for companies already indexed by AlphaLens — won't work for pending/indexing orgs
