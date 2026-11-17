# Amazon New Layout Fixes (2026-07)

Session-specific details of the DOM structure changes and fixes applied to `amazon_handler.js`.

## Problem: Detail pages returning all-null fields

### Root Cause
1. `Accept-Encoding: identity` in `extraHTTPHeaders` + `setExtraHTTPHeaders` caused Amazon's JS to not render the product page content. Removing the header and the entire `setExtraHTTPHeaders` call fixed it.
2. Old `waitForTimeout(3000)` was too short for new JS-heavy pages. Added `waitForSelector('#productTitle, #dp', { timeout: 15000 })` for product-detail pages.

### New Amazon Detail Page DOM Structure (July 2026)

| Field | Old Selector/Regex | New Selector | Notes |
|---|---|---|---|
| title | `#productTitle` | `#productTitle` | Unchanged |
| brand | `#bylineInfo` | `#bylineInfo` | Returns "Brand: XXX" or "Visit the XXX Store" — must strip prefixes |
| seller | N/A | `#sellerProfileTriggerId` | New field, e.g. "BeataTap-SKALON" |
| bsr | `body.innerText` regex | `#prodDetails tr` th/td scan | Regex `Best Sellers Rank.*?#([\d,]+)` no longer matches; must scan `#prodDetails tr` rows |
| dateFirstAvailable | `body.innerText` regex | N/A — **100% missing** | Amazon no longer shows this on most product pages |
| details | `#productDetails_techSpec_section_1 tr` | `#prodDetails tr` | New layout uses `#prodDetails` instead of `#productDetails_techSpec_section_1` |

### Brand Cleanup Regex
```js
brand = brand.replace(/^Brand:\s*/i, '').replace(/^Visit the\s+/i, '').replace(/\s+Store$/i, '').trim();
```

### BSR Extraction (New Layout)
```js
document.querySelectorAll('#prodDetails tr').forEach(row => {
    const cells = row.querySelectorAll('th, td');
    if (cells.length >= 2) {
        const key = cells[0].textContent.trim().replace(/[:\s]+$/, '');
        const val = cells[1].textContent.trim();
        if (key.match(/Best Sellers Rank/i)) {
            const m = val.match(/#([\d,]+)/);
            if (m) bsr = parseInt(m[1].replace(/,/g, ''));
        }
    }
});
```

### Seller Extraction (3 methods, in order)
1. `#sellerProfileTriggerId` — most reliable (e.g. "BeataTap-SKALON")
2. `body.innerText.match(/Sold by\s+([\w\s\-\.]+)/i)` — fallback
3. `#prodDetails tr` row with "Ships from" or "Sold by" key — last resort

### Seller Data Garbage Filter (in analyze.py)
Some ASINs' `#sellerProfileTriggerId` captures Amazon comparison widget text:
```
"different sellers.\nShow details\nExplore more from across the store\nPage 1 of 7\n..."
```
Filter rule: if seller contains `\n`, "Show details", "Explore more", or "Page 1 of" → set to null.

## Proxy: Datacenter → ISP

| Proxy Type | Entry Domain | Amazon Works? |
|---|---|---|
| Datacenter (DDC) | `disp.oxylabs.io` | ❌ 100% soft-blocked (empty page) |
| ISP | `isp.oxylabs.io` | ✅ Working |

Changed `config/proxies.json` from `disp.oxylabs.io` to `isp.oxylabs.io`. Must `docker build` after changing proxies.json since it's COPY'd into the image.

## Search Page Limitation

`--pages 5` returns ~26 unique ASINs, not 100. Amazon search results contain many sponsored/duplicate listings. To get closer to Top 100:
- Use more pages (--pages 10) → returns ~234 unique ASINs (enough for Top 100)
- Or use keyword variations and merge results

## Search Page Pagination Fix (2026-07-04)

**Bug**: `amazon_handler.js` used `&pg=${pg}` for search page pagination. Amazon does NOT recognize `&pg=N` — it silently returns page 1 data for every page. This caused `--pages 10` to return only 29 unique ASINs (all from page 1, just duplicated 10 times).

**Fix**: Changed `&pg=N` to `&page=N` in the URL construction:
```js
// Before (broken):
if (pg > 1) url = job.url.includes('?') ? `${job.url}&pg=${pg}` : `${job.url}?pg=${pg}`;
// After (fixed):
if (pg > 1) url = job.url.includes('?') ? `${job.url}&page=${pg}` : `${job.url}?page=${pg}`;
```

**Verification**: `--pages 10` with `&page=N` returns 234 unique ASINs (vs 29 with `&pg=N`).

**Diagnosis tip**: If multi-page search scraping returns far fewer unique ASINs than expected, check the pagination parameter first.
