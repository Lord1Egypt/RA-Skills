# Skill: E-commerce New Product Research & Development

## Overview

This skill provides an end-to-end workflow for **new product research and development across e-commerce platforms** (e.g., Amazon, Shopee, SHEIN). It covers:

* Category data analysis
* Target segment identification
* Competitive and feature analysis
* Market gap discovery
* Product definition
* Validation and launch strategy

This framework is **category-agnostic** and applicable to both **private label and branded product development**.

---

## Inputs Required

| Input                   | Description                                          | Example                       |
| ----------------------- | ---------------------------------------------------- | ----------------------------- |
| Category export file    | Product data export from research tools or platforms | `.xlsx / .csv` export         |
| Target price range      | Desired selling price band                           | `$20 – $40`                   |
| Material / positioning  | Target quality tier and audience                     | `mid-tier / premium / budget` |
| SKU count goal          | Number of products to develop                        | `2–5 SKUs`                    |
| Sample specs (optional) | Prototype dimensions and features                    | `size, weight, components`    |

---

## Supported Data Sources

This workflow supports export files from:

* **Amazon tools**: Sorftime, Helium10, Jungle Scout, SIF
* **Shopee tools**: Shopdora, platform exports
* **SHEIN tools**: SHEIN selection assistant
* Any structured dataset containing product-level metrics

---

## Workflow Steps

---

### Step 1 — Category Overview

Parse the export file and produce:

* Total monthly and annual unit volume
* Seasonality trends (monthly demand peaks)
* Price distribution (bucketed by intervals)
* Top brands / sellers by SKU count and sales

**Typical fields to extract:**

```
Monthly Sales, Annual Sales, Price,
Gross Profit, Margin,
Category Rank, Subcategory,
Listing Age (days),
Review Count, Rating,
Brand / Seller,
Bullet Points / Description,
Dimensions, Weight
```

---

### Step 2 — Target Segment Deep Dive

Filter products by:

* Target price range
* Positioning (quality tier / material / use case)

Analyze:

* SKU count per sub-price band
* Average monthly sales per SKU
* Average margin per band
* Brand concentration per band

**Decision rule:**

Select the segment where:

* High average sales per SKU
* Low brand dominance / fragmentation

→ This indicates a **potential opportunity zone**

---

### Step 3 — Competitor & Feature Analysis

#### Brand Landscape

* Identify top brands by SKU count
* Analyze their pricing patterns
* Understand positioning (budget vs premium vs niche)

#### Feature / Attribute Analysis

Extract recurring attributes from titles, bullets, or descriptions:

Group into:

* Functional attributes (performance, utility)
* Design attributes (style, form factor)
* Usage attributes (scenarios, convenience)

For each attribute:

* Count number of SKUs
* Calculate average sales

**Interpretation:**

* High sales + low SKU count → opportunity
* High sales + high SKU count → competitive but validated
* Low sales → weak demand signal

---

### Step 4 — Market Gap Identification

Identify 3–5 opportunities using:

| Gap Type        | Criteria                                              | Signal                   |
| --------------- | ----------------------------------------------------- | ------------------------ |
| Attribute gap   | High demand attribute with low SKU presence           | Underdeveloped niche     |
| Positioning gap | Missing tier (e.g. mid-tier between budget & premium) | Pricing imbalance        |
| Format gap      | Inefficient or outdated product formats               | Optimization opportunity |
| Trend gap       | Emerging trend not yet saturated                      | Early mover advantage    |

---

### Step 5 — Product Definition (per SKU)

For each recommended SKU:

```
Product Name (working title)
Suggested Price: $XX.XX

Why this opportunity exists:
[Data-backed reasoning]

Positioning:
[Target audience + tier]

Core Specifications:
- Dimensions:
- Weight:
- Key components:
- Structure / format:

Variants:
[Color / style / version options]

Key Differentiation:
[Clear advantage vs competitors]

Estimated Margin:
~$XX (~XX%)

Launch Timing:
[Quarter / season]
```

---

### Step 6 — Sample / Prototype Validation

If prototype or spec sheet is available:

#### Dimension Validation

* Confirm size aligns with intended use case
* Benchmark against top competitors
* Check compatibility with primary usage scenarios

#### Feature Feasibility

* Validate physical feasibility of components
* Ensure no over-complexity or cost inefficiency
* Confirm manufacturability

#### Scoring (1–5 scale)

* Use-case fit
* Competitive differentiation
* Feature completeness
* Cost vs value balance
* Margin viability

---

### Step 7 — Social Proof Validation

Validate demand using external signals:

#### Platforms

* Reddit (category discussions, sentiment)
* Google Trends (search demand over time)
* Media / blogs (trend mentions)
* Social platforms (indirect trend signals)

#### Validation Criteria

* At least one product with strong sales performance in niche
* Evidence of growing or stable search demand
* Community or media discussion indicating awareness

---

### Step 8 — Keyword Advertising Framework

#### Tier 1 — Awareness

* Broad category and attribute keywords
* Goal: traffic discovery

#### Tier 2 — Conversion

* Specific long-tail keywords
* Use-case driven queries
* Goal: improve conversion rate

#### Tier 3 — Competitor Targeting

* Competitor brand + product type
* Goal: capture high-intent traffic

---

#### Campaign Structure

| Campaign       | Type           | Goal                |
| -------------- | -------------- | ------------------- |
| Auto discovery | Automated ads  | Keyword discovery   |
| Core keywords  | Manual broad   | Ranking             |
| Long-tail      | Phrase / exact | Conversion          |
| Competitor     | Exact          | Traffic capture     |
| Retargeting    | Display        | Conversion recovery |

---

### Step 9 — Launch Timeline

```
Phase 1: Initial launch (test demand)
Phase 2: Optimization (ads + listing improvements)
Phase 3: Expansion (variants / additional SKUs)
```

---

### Pre-launch Checklist

* Supplier validation
* Sample approval (quality, usability)
* Listing assets (images, descriptions)
* Pricing and promotion strategy
* Advertising budget allocation
* Review acquisition process

---

## Output Format

The workflow should produce:

1. Market Overview
2. Target Segment Analysis
3. Competitive Landscape
4. Market Gaps
5. Product Recommendations
6. Sample Validation (if applicable)
7. Social Proof Summary
8. Keyword Strategy
9. Launch Plan


