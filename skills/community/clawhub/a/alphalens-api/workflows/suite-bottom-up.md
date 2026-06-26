# Bottom-Up Market Intelligence Suite

When a user asks for a "bottom-up mapping", "bottom-up analysis", "deep dive", or "full mapping" for a company, **always produce all three outputs as a linked suite**. Never stop at just the market map.

**Prerequisite:** You should only be here if the Mapping Workflow Selection section in SKILL.md routed you to the bottom-up path. If the user asked for a simple "market map", use `workflows/market-map-org.md` instead.

> **Data disclosure:** This orchestrator workflow delegates to market-map-product, investor-network, and peer-benchmark workflows. Each sends organization/product IDs to the AlphaLens API and fetches favicons from Google's public service. Confirm with the user before running the full suite on more than 20 organizations.

## Critical: Bottom-up mapping always uses product-centric maps

The market map component must be **product-centric** (one tab per qualifying product). This means:
- Always fetch the anchor company's products first
- Always run the Step 0 product scoring formula
- Always use product-level similarity (`/search/products/{id}/similar`) as the primary signal source
- Org-level similarity is a supplement, not the primary driver

If you skip product scoring and collapse to a single org-level map, you are **not following the bottom-up workflow** — you are running the simpler org-level workflow and mislabeling it.

---

## Execution order

1. Read `workflows/market-map-product.md` and build the tabbed market map
2. Read `workflows/investor-network.md` and build the investor network using the companies discovered in step 1
3. Read `workflows/peer-benchmark.md` and build the peer benchmark using the closest peers from step 1

Load each workflow file when you reach that phase — not all at once.

---

## Output files

The three outputs are standalone HTML files. Each is fully self-contained — favicons are base64-encoded inline, no proxy required.

| File | What it shows |
|---|---|
| `{anchor}-market-map.html` | Product-centric tabbed market map (one cluster grid per product) |
| `{anchor}-investor-network.html` | D3 force-directed graph of investors + portfolio companies |
| `{anchor}-peer-benchmark.html` | Headcount growth, funding, capital efficiency + qualitative positioning for 5 closest peers |

---

## Consistent site-wide navigation (required on all three pages)

Every page gets the **same sticky dark top nav bar** — same HTML, just the `sn-active` class moves to the current page:

```html
<nav id="site-nav">
  <a class="sn-brand" href="{anchor}-market-map.html">
    <span class="brand-initial">{first_letter}</span> {Anchor Name}
  </a>
  <div class="sn-links">
    <a class="sn-link [sn-active?]" href="{anchor}-market-map.html">Market Map</a>
    <a class="sn-link [sn-active?]" href="{anchor}-investor-network.html">Investor Network</a>
    <a class="sn-link [sn-active?]" href="{anchor}-peer-benchmark.html">Peer Benchmark</a>
  </div>
  <div class="sn-action"><!-- page-specific export button --></div>
</nav>
```

```css
#site-nav { background:#1a202c; display:flex; align-items:center; padding:0 28px; height:44px; position:sticky; top:0; z-index:200; }
.sn-brand  { color:#fff; font-size:13px; font-weight:700; margin-right:20px; text-decoration:none; display:flex; align-items:center; gap:8px; }
.brand-initial { width:20px; height:20px; border-radius:4px; background:#d69e2e; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; color:#fff; }
.sn-links  { display:flex; align-items:center; gap:2px; flex:1; }
.sn-link   { font-size:12px; font-weight:500; padding:5px 12px; border-radius:6px; color:#a0aec0; text-decoration:none; display:flex; align-items:center; gap:5px; transition:all .15s; }
.sn-link:hover   { color:#fff; background:rgba(255,255,255,.08); }
.sn-link.sn-active { color:#1a202c; background:#fff; font-weight:600; }
.sn-action { display:flex; align-items:center; gap:8px; }
.sn-export { font-size:12px; font-weight:600; padding:5px 13px; border-radius:6px; border:1px solid rgba(255,255,255,.2); background:transparent; cursor:pointer; color:#e2e8f0; }
```

Note: the brand mark uses a coloured letter avatar (CSS-only) rather than a favicon, so no proxy or base64 fetch is needed for the nav bar.
