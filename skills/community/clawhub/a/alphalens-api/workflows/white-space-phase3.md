# Phase 3: Feature Survival Matrix (Subtract and Swap)

**Purpose:** Break the anchor's products into component features and test which feature combinations have competitive coverage. This reveals which features are **table stakes** (everyone has them, required to compete) vs. **differentiators** (few survive without them, creates leverage).

> **Data disclosure:** This workflow sends product feature descriptions to the AlphaLens `search-products` API.

---

## Step 3a — Feature Decomposition

LLM reasoning task — decompose each product into 3-5 key features:

From the product description and `key_features` array, extract:
- What are the **core functional capabilities** of this product?
- Which features are **primary** (defining the product category)?
- Which features are **secondary** (nice-to-have, differentiation)?

> Be strict: if removing a feature means the product is no longer recognizable as the category, it's a table stakes feature. If removing it just makes the product less appealing but still recognizable, it's secondary.

---

## Step 3b — Combinatorial Search Queries

For each product, run these queries in parallel:

```bash
# Product 1 — feature combination queries
# Format: query each feature combination as a search description

# Full combo (A+B+C — anchor's full feature set)
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search?description={feature_A}%20{feature_B}%20{feature_C}&limit=50&is_headquarters=true" > $WORKDIR/p1_abc.json &

# Omit A (B+C)
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search?description={feature_B}%20{feature_C}&limit=50&is_headquarters=true" > $WORKDIR/p1_bc.json &

# Omit B (A+C)
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search?description={feature_A}%20{feature_C}&limit=50&is_headquarters=true" > $WORKDIR/p1_ac.json &

# Omit C (A+B)
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search?description={feature_A}%20{feature_B}&limit=50&is_headquarters=true" > $WORKDIR/p1_ab.json &

# Swap: replace C with new feature D
curl -s -H "API-Key: $KEY" "$API/api/v1/search/products/search?description={feature_A}%20{feature_B}%20{feature_D}&limit=50&is_headquarters=true" > $WORKDIR/p1_abd.json &

wait
```

> **Note:** AlphaLens does not support boolean exclusion (NOT queries). This is why "omit A" means explicitly querying B+C — we observe which competitors survive on that combination alone.
>
> **New feature D:** The user should specify a candidate feature they are considering adding. If no new feature is provided, skip the swap query and replace with a "single feature" query to establish baseline coverage.

---

## Step 3c — LLM Reasoning: Feature Survival Analysis

For each combination query, analyze:

**Inputs to LLM:**
- Total competitors returned per combination
- Cosine distance quality (lower = more direct competition)
- Are the surviving competitors recognizable players or obscure?
- Does removing Feature A cause competitors to drop out, or do many survive on B+C?

**LLM Task — build the survival matrix and classify features:**

| Combination | Competitors | Interpretation |
|---|---|---|
| A+B+C (full) | 45 | Anchor is in a dense category |
| B+C (no A) | 38 | Feature A is **not table stakes** — most competitors survive without it |
| A+C (no B) | 12 | Feature B may be **table stakes** — many competitors drop when removed |
| A+B (no C) | 30 | Feature C is **not table stakes** |
| A+B+D (swap) | 8 | Adding D and removing C dramatically reduces competition — potential white space |

**Feature classification:**

| Classification | Definition | Signal |
|---|---|---|
| **Table Stakes** | Removing it causes most competitors to drop out; required to compete | Few survive on the complement |
| **Differentiator** | Many competitors survive without it; not required but valued | Most survive on the complement |
| **Novel** | Querying just this feature returns sparse results | Low baseline coverage |
| **Validated** | Swap query (A+B+D) returns fewer quality competitors | D is uncontested |

---

## Step 3d — Render Feature Survival Matrix

Build a visual matrix table:

```html
<div class="survival-matrix">
  <h3>Product 1 — Feature Survival Matrix</h3>
  <table>
    <thead>
      <tr>
        <th>Combination</th>
        <th>Features</th>
        <th>Competitors</th>
        <th>Classification</th>
        <th>Interpretation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Full (A+B+C)</td>
        <td class="feature-tags"><span class="tag">A</span><span class="tag">B</span><span class="tag">C</span></td>
        <td>45</td>
        <td>Anchor baseline</td>
        <td>Dense competitive cluster</td>
      </tr>
      <tr>
        <td>B+C</td>
        <td class="feature-tags"><span class="tag removed">A</span><span class="tag">B</span><span class="tag">C</span></td>
        <td>38</td>
        <td>A = Differentiator</td>
        <td>Most competitors survive without A</td>
      </tr>
      <!-- ... -->
    </tbody>
  </table>
</div>
```

```css
.tag { background: #3182ce; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
.tag.removed { background: #e2e8f0; color: #718096; text-decoration: line-through; }
.tag.added { background: #38a169; color: #fff; }
```

Attach this section into the main `white-space.md` output under `<section id="phase3">`.
