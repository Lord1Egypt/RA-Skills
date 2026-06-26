# Phase 2: Adjacency Gap Radar

**Purpose:** Map the upstream and downstream workflows around the anchor's products. White space often lives in the handoffs — the tools users need before they enter and after they exit the anchor's product.

> **Data disclosure:** This workflow sends product feature descriptions to the AlphaLens `search-customers` API to find adjacent companies.

---

## Step 2a — Define Upstream and Downstream Workflows

LLM reasoning task — identify the **workflow context** for each product:

For each product, answer:
1. **What must a user accomplish BEFORE using this product?** (upstream input workflow)
2. **What does a user do with the output FROM this product?** (downstream output workflow)

> This is LLM reasoning, not API calls. Use your knowledge of the product category and the anchor's specific product description to define realistic upstream/downstream workflows.
>
> Examples:
> - Product: AI-powered invoice processing → Upstream: "expense submission / receipt capture"; Downstream: "AP automation / financial reconciliation"
> - Product: Sales engagement platform → Upstream: "lead prospecting / list building"; Downstream: "CRM updating / pipeline management"

Define 1-2 upstream workflow descriptions and 1-2 downstream workflow descriptions per product.

---

## Step 2b — Search for Adjacent Workflow Products

Run `search-customers` queries for each upstream and downstream workflow:

```bash
# Upstream for Product 1
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search-customers?description=companies%20that%20need%20{upstream_workflow_1}&limit=50&is_headquarters=true" > $WORKDIR/p1_upstream1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search-customers?description=companies%20that%20need%20{upstream_workflow_2}&limit=50&is_headquarters=true" > $WORKDIR/p1_upstream2.json &

# Downstream for Product 1
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search-customers?description=companies%20that%20use%20{downstream_workflow_1}&limit=50&is_headquarters=true" > $WORKDIR/p1_downstream1.json &
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search-customers?description=companies%20that%20use%20{downstream_workflow_2}&limit=50&is_headquarters=true" > $WORKDIR/p1_downstream2.json &

# Repeat for Product 2 and Product 3 in the same block
wait
```

> **Why `search-customers` instead of `search`?** `search-customers` describes *who* buys the product and *what workflow they accomplish* — which directly maps to upstream/downstream handoff analysis. `search` matches on product descriptions, which may not capture workflow position.

---

## Step 2c — LLM Reasoning: Gap Severity Assessment

For each upstream/downstream query, analyze:

**Inputs to LLM:**
- Total results returned
- Are the results **purpose-built** for this specific workflow, or generic tools (e.g., "Excel", "Zapier", "email")?
- Do results share the same ICP as the anchor, or are they horizontal/generic?
- Quality of returned companies: funded, active, specialized?

**LLM Task — classify each adjacency:**

| Signal | Gap Classification |
|---|---|
| Results are purpose-built tools in the same ICP, well-funded | **Defended Adjacency** — competitors own this handoff |
| Results are generic horizontal tools, no vertical specialization | **Open Adjacency** — white space for vertical purpose-built tool |
| Few or no results at all | **Empty Adjacency** — high white space opportunity |
| Results exist but are fragmented (many small players, no dominant) | **Fragmented Adjacency** — M&A opportunity or consolidation potential |

Also assess: does the anchor company already have products covering these adjacencies? If yes, mark as **internal** — this is an expansion signal, not external white space.

---

## Step 2d — Render Adjacency Gap Radar

Build a radar/spider chart per product showing upstream and downstream coverage:

```html
<div class="adjacency-radar" id="radar-product1">
  <h3>Product 1 — Adjacency Gap Radar</h3>
  <div class="radar-chart">
    <!-- Rendered via Chart.js radar -->
  </div>
  <table class="adjacency-table">
    <thead>
      <tr><th>Workflow</th><th>Type</th><th>Competitors Found</th><th>Classification</th><th>Gap Severity</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>Lead Prospecting</td>
        <td>Upstream</td>
        <td>12</td>
        <td>Open Adjacency</td>
        <td>Medium</td>
      </tr>
      <!-- ... -->
    </tbody>
  </table>
</div>
```

Use Chart.js radar chart with one axis per upstream/downstream workflow, colored by gap severity.

Attach this section into the main `white-space.md` output under `<section id="phase2">`.
