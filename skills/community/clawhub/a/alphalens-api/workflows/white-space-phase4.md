# Phase 4: ICP Expansion Grid (Lateral Move)

**Purpose:** Test whether the anchor's core product mechanics represent white space in adjacent industries. Strip the industry jargon, keep the mechanics, and query against a different ICP.

> **Data disclosure:** This workflow sends organization/product IDs and feature descriptions to the AlphaLens API.

---

## Step 4a — ICP Extraction

LLM reasoning task — extract the **pure mechanics** of each product:

From the product description, strip all industry-specific language and extract:
- What does this product **do** at the mechanical level? (e.g., "routes documents based on rules", "enriches records with external data", "automatically categorizes input using ML")
- What is the **core workflow automation**?
- What industry terms can be removed?

Then define 2-3 **target ICPs** (adjacent but distinct from the anchor's current market):
- Target ICP 1: A vertical where this mechanic would apply but isn't currently served by modern tools
- Target ICP 2: A horizontal adjacency where the mechanic is relevant but the current market uses legacy/generic tools

> **Example ICP extraction:**
> - Product: "AI-powered compliance routing for FinTech" → Mechanics: "automated document routing based on classification rules" → ICPs: "Healthcare compliance", "Legal document workflows", "Government procurement"
> - Product: "Sales engagement platform" → Mechanics: "automated outreach sequencing with engagement tracking" → ICPs: "Recruitment engagement", "Nonprofit fundraising", "Political campaign outreach"

---

## Step 4b — ICP Expansion Queries

For each product, run queries for each target ICP:

```bash
# Product 1 — ICP expansion queries
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search?description={mechanic}%20for%20{icp1}&limit=50&is_headquarters=true" > $WORKDIR/p1_icp1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search?description={mechanic}%20for%20{icp2}&limit=50&is_headquarters=true" > $WORKDIR/p1_icp2.json &

# Also run the anchor's current ICP for baseline comparison
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search?description={mechanic}%20for%20{anchor_icp}&limit=50&is_headquarters=true" > $WORKDIR/p1_icp_anchor.json &

wait
```

---

## Step 4c — Cross-reference with Funding Data

For each query result, fetch funding data on the top 5 returned companies to assess market maturity:

```bash
# For each unique org_id in the ICP results, fetch funding in parallel
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{org_id1}/funding" > $WORKDIR/funding_org1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/entities/organizations/{org_id2}/funding" > $WORKDIR/funding_org2.json &
# ... in same block ...
wait
```

---

## Step 4d — LLM Reasoning: Lateral White Space Assessment

For each ICP, analyze:

**Inputs to LLM:**
- Total competitors returned
- Are the competitors **modern** (founded post-2015, active) or **legacy** (old incumbents)?
- Funding levels of top competitors: are they well-funded (showing venture validation) or bootstrapped?
- Is the competition **vertically specialized** (purpose-built for that ICP) or **horizontal** (same tool applied to ICP)?

**LLM Task — classify each ICP expansion:**

| Signal | ICP Classification |
|---|---|
| Dense modern well-funded competitors in that ICP | **Occupied** — not white space |
| Sparse results, mostly legacy/incumbents, no recent funding | **Legacy-Crowded** — white space for modern challenger |
| No results at all for that ICP | **Empty** — high confidence white space |
| Results exist but are horizontal tools, not vertical specialists | **Horizontal-Crowded** — white space for vertical purpose-built |

**Confidence signals for lateral move:**
- No AlphaLens-indexed competitors + no legacy incumbents = high confidence white space
- No recent funding rounds in ICP = market hasn't been validated by venture capital
- High funding in anchor ICP + zero funding in adjacent ICP = capital hasn't followed the adjacency

---

## Step 4e — Render ICP Expansion Grid

Build a grid with products as rows, ICPs as columns:

```html
<div class="icp-expansion-grid">
  <h3>ICP Expansion Grid</h3>
  <table>
    <thead>
      <tr>
        <th>Product</th>
        <th>Anchor ICP (Baseline)</th>
        <th>ICP 1 (Healthcare)</th>
        <th>ICP 2 (Legal)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Product A</td>
        <td class="cell-dense">45 competitors<br><span class="status occupied">Occupied</span></td>
        <td class="cell-sparse">3 competitors<br><span class="status empty">Empty — High Confidence</span></td>
        <td class="cell-medium">12 competitors<br><span class="status legacy-crowded">Legacy-Crowded</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.cell-dense    { background: #fed7d7; }
.cell-medium   { background: #fefcbf; }
.cell-sparse   { background: #c6f6d5; }
.cell-empty    { background: #38a169; color: #fff; }
.status.occupied      { color: #c53030; }
.status.empty         { color: #22543d; font-weight: 600; }
.status.legacy-crowded { color: #744210; }
```

Attach this section into the main `white-space.md` output under `<section id="phase4">`.
