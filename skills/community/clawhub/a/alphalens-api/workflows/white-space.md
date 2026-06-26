# White Space Analysis

Use this when the user asks to find market white space, identify untapped positioning, discover uncontested product areas, or run a "blue ocean" analysis for a company. This workflow produces a structured white space report across 4 analytical phases.

**Trigger phrases:** "white space", "blue ocean", "uncontested", "market gap", "find positioning", "find the white space", "find uncontested"

**Prerequisite:** This workflow requires a domain as input. Unlike market map workflows that produce competitive landscapes of *existing* players, white space analysis produces a structured assessment of *absence* — where competition is thin, fragmented, or non-existent.

> **Data disclosure:** This orchestrator delegates to 4 phase workflows (saturation map, adjacency gap radar, feature survival matrix, ICP expansion grid). Each phase sends organization/product IDs and feature descriptions to the AlphaLens API. Confirm with the user before running on more than 20 organizations.

---

## What This Workflow Produces

| Phase | Output | LLM Reasoning Task |
|---|---|---|
| 1 — Saturation Map | Competitor density heatmap per product | Classify clusters as Red/Yellow/Green ocean |
| 2 — Adjacency Gap Radar | Upstream/downstream workflow coverage | Judge handoff fragmentation and gap severity |
| 3 — Feature Survival Matrix | A/B/C combinatorics survival table | Identify table stakes vs. differentiators |
| 4 — ICP Expansion Grid | Mechanics × ICP competitive density | Synthesize lateral white space opportunity |

The final output is a single HTML report with 4 sections, one per phase, with an LLM-generated executive summary and white space opportunity narrative at the end.

---

## How to Prompt

**Basic:**
- `Find the white space around ramp.com`
- `Run a blue ocean analysis for company.com`
- `Find uncontested positioning for zendesk.com`

**With Phase 3 (Subtract & Swap) specificity:**
- `Run white space analysis on ramp.com and test whether adding AI-based expense categorization would be uncontested`
- `Find positioning gaps for company.com using the subtract and swap method`

**With Phase 4 (ICP Translation) specificity:**
- `Run a white space analysis on ramp.com and test whether the same mechanics apply in the healthcare vertical`
- `Find lateral white space for company.com across the legal and compliance ICPs`

---

## Execution Order

```
1. Resolve domain → fetch products → score and select top 3
2. Phase 1: Saturation Map (per product)        → read [white-space-phase1.md]
3. Phase 2: Adjacency Gap Radar                  → read [white-space-phase2.md]
4. Phase 3: Feature Survival Matrix              → read [white-space-phase3.md]
5. Phase 4: ICP Expansion Grid                  → read [white-space-phase4.md]
6. LLM Synthesis: Executive summary + white space narrative
```

Load each phase file when you reach that step — not all at once. The phase files contain the detailed API calls and LLM reasoning tasks.

---

## Step 0 — Resolve Domain and Score Products

This step is identical to [`market-map-product.md` Step 0 and Step 1](market-map-product.md). Always start here before any white space analysis — the white space findings are anchored to the company's specific products.

### Step 0a — Resolve the anchor company

```bash
WORKDIR=$(mktemp -d)
API="https://api-production.alphalens.ai"

curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/by-domain/{domain}"
# → get organization_id, active_domain, logo_url
```

### Step 0b — Fetch all products

```bash
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{organization_id}/products?limit=20"
# → returns array of { id, product_name, product_description, is_primary_product, product_target_audiences, product_categories, product_references, key_features }
```

### Step 0c — Score and select top 3 products

Apply the scoring formula to each product:

```
+40  is_primary_product: true
+10  per product_reference URL that is NOT the company homepage
 +5  per distinct entry in product_target_audiences
  0  baseline

-50  product_name contains: api, rest, extension, bulk, integration, crm, webhook, export, sdk
-30  product_categories contains 'services'
-20  ALL product_references point only to the company homepage
-15  a key_feature overlaps with a higher-scoring product
```

**Decision rules:**
1. Compute score for every product
2. Keep only products with **score ≥ 20**
3. Cap at **3 products maximum** — take top 3 by score
4. **Pairwise distinctiveness check**: if two products share >70% overlapping `product_target_audiences`, merge them (same market map)
5. **Job-to-be-done sanity check**: surviving products should represent different buyer actions

> **If no products pass threshold (score < 20):** Fall back to org-level similarity only. The company likely lacks product-level indexing. Run a single saturation map on the org.

---

## Phase 1

Read [`white-space-phase1.md`](white-space-phase1.md) — Saturation Map (The Mirror Test).

---

## Phase 2

Read [`white-space-phase2.md`](white-space-phase2.md) — Adjacency Gap Radar.

---

## Phase 3

Read [`white-space-phase3.md`](white-space-phase3.md) — Feature Survival Matrix (Subtract and Swap).

---

## Phase 4

Read [`white-space-phase4.md`](white-space-phase4.md) — ICP Expansion Grid (Lateral Move).

---

## Step 5 — LLM Synthesis: Executive Summary and White Space Narrative

After all 4 phases are complete, run a final LLM reasoning pass to synthesize the findings into:

### 5a — Per-Product White Space Summary

For each product, synthesize:
1. **Saturation verdict** (Red/Yellow/Green from Phase 1)
2. **Biggest adjacency gap** (most severe open/empty adjacency from Phase 2)
3. **Key differentiator** (which feature is the real differentiator from Phase 3)
4. **Top ICP expansion opportunity** (highest confidence lateral white space from Phase 4)

### 5b — Overall White Space Opportunity Narrative

Structure the narrative around:
- **The core insight**: What is the single most actionable white space finding?
- **Confidence level**: How strong is the signal? (based on Phase 1-4 confidence indicators)
- **Strategic options**: Given the findings, what are the 2-3 possible strategic responses?
  - Option A: Enter the adjacency gap with a new product
  - Option B: Defend the current position against the identified differentiator threat
  - Option C: Lateral move into the validated ICP white space
- **Risk factors**: What could invalidate the white space finding? (incumbents pivoting, capital flooding in, regulatory changes)

### 5c — Render Executive Summary Section

```html
<div class="executive-summary">
  <h2>White Space Analysis — Executive Summary</h2>
  
  <div class="summary-card anchor">
    <h3>{Anchor Company} ({Domain})</h3>
    <p class="verdict">Overall White Space Verdict: <strong>{RED/YELLOW/GREEN}</strong></p>
    <p class="confidence">Confidence: <strong>{High/Medium/Low}</strong></p>
  </div>

  <div class="per-product-summaries">
    <!-- one card per product -->
  </div>

  <div class="strategic-options">
    <h3>Strategic Options</h3>
    <ol>
      <li><strong>Option A: {Name}</strong> — {2 sentence description}</li>
      <li><strong>Option B: {Name}</strong> — {2 sentence description}</li>
      <li><strong>Option C: {Name}</strong> — {2 sentence description}</li>
    </ol>
  </div>

  <div class="risk-factors">
    <h3>Risk Factors</h3>
    <ul>
      <li>{Risk 1}</li>
      <li>{Risk 2}</li>
    </ul>
  </div>
</div>
```

---

## Output File

Save the complete white space report as:

```
{anchor}-white-space.html
```

### Design Rules (non-negotiable)

Follow these consistently — they are the same standards used in all other AlphaLens workflows:

- **Light mode only** — `background: #f7f8fc`, dark text. Never dark mode.
- **No emojis** in section headers, table labels, or button text.
- **Favicon handling**: fetch via Google favicon service and base64-encode inline. If a favicon curl returns empty, use a CSS letter avatar (coloured circle with the company's initial). Never leave a company without a visual representation.
- **Anchor company**: if the anchor appears in any result set, give it a gold border + subtle glow (`border: 2px solid #d69e2e; box-shadow: 0 0 10px rgba(214,158,46,0.3)`).
- **Pending companies** (just triggered indexing): `opacity: 0.65`, dashed border, italic name.
- **Indexed companies**: full opacity, solid border.
- **Cluster/classification naming**: use buyer-outcome language, not technology labels. E.g., "Automated Compliance Routing" not "Workflow Automation Tool".

### HTML Structure

```html
<nav id="site-nav">
  <a class="sn-brand" href="{anchor}-white-space.html">
    <span class="brand-initial">{first_letter}</span> {Anchor Name}
  </a>
  <div class="sn-links">
    <a class="sn-link sn-active" href="{anchor}-white-space.html">White Space</a>
  </div>
</nav>

<section id="phase1">
  <h2>Phase 1 — Saturation Map</h2>
  <!-- saturation heatmap table -->
</section>

<section id="phase2">
  <h2>Phase 2 — Adjacency Gap Radar</h2>
  <!-- radar chart + adjacency table -->
</section>

<section id="phase3">
  <h2>Phase 3 — Feature Survival Matrix</h2>
  <!-- survival matrix table -->
</section>

<section id="phase4">
  <h2>Phase 4 — ICP Expansion Grid</h2>
  <!-- ICP grid table -->
</section>

<section id="executive-summary">
  <h2>Executive Summary</h2>
  <!-- synthesis narrative -->
</section>
```

### PDF Export

The HTML is fully self-contained (favicons embedded as base64), so `html2pdf.js` works without any proxy or CORS issues:

```js
html2pdf().set({
  margin: 12,
  filename: '{anchor}-white-space.pdf',
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

Set `visibility: hidden` (not `display: none`) on the export button before rendering — hides it from the PDF without shifting layout.

---

## Common Pitfalls

- **Phase 1 — Mistaking horizontal for vertical competition:** A search returning generic tools (Zapier, Excel) doesn't mean the vertical is crowded — it means the handoff is unspecialized. Always judge by vertical specificity.
- **Phase 2 — Defining upstream/downstream too broadly:** If your upstream is "all business software", you'll get meaningless results. Keep workflows specific to the product category.
- **Phase 3 — Feature decomposition too granular:** 3-5 features max. If you decompose into 20 sub-features, the combinatorial queries become noise.
- **Phase 4 — ICP extraction losing the core mechanic:** Strip industry jargon but don't strip the core innovation. "AI-powered" may be generic — "ML-based classification routing" is the mechanic.
- **Phase 5 — Overclaiming white space:** Absence from AlphaLens ≠ absence from the market. Always qualify findings with "AlphaLens-indexed" and note that private companies, pre-revenue startups, and internal tools may not appear.
