---
name: amazon-search
description: Search Amazon product listings for a keyword and return structured JSON results. Results are cached by ASIN/uuid for incremental searches and saved automatically to `results/`.
env:
  - T2P_PROXY: "Optional: Proxy URL (e.g., http://127.0.0.1:7890 or socks5://127.0.0.1:1080). If not set, no proxy will be used."
  - T2P_IMAGE_DIR: "Optional: Custom directory for downloaded images (used with --download flag). Default: Windows: %LOCALAPPDATA%/trend2product/images, Linux/macOS: ~/.cache/trend2product/images"
---

# Amazon Search Skill
Search Amazon for products matching a keyword query and return structured JSON results.

## Prerequisites

Install [Bun](https://bun.sh) runtime:

```bash
curl -fsSL https://bun.sh/install | bash
```

Install skill dependencies:

```bash
cd skills/amazon-search
bun install
```

Install Playwright browsers (required for Amazon search):

```bash
cd skills/amazon-search/scripts
npm install
npx playwright install chromium
```

## Cookie

This skill uses **Playwright** to search Amazon directly in a headless browser. No manual cookie management is required.

### Playwright Prerequisites

Install npm dependencies and Playwright browsers:

```bash
cd skills/amazon-search/scripts
npm install
npx playwright install chromium
```

## Inputs
| Parameter       | Type | Description |
|-----------------|---|---|
| `keyword`         | string | Search keywords (e.g. `"t-shirt"`) |
| `proxy`         | string | Optional proxy URL. Can be set as argument value or via `--proxy` flag / `T2P_PROXY` env var. Supports HTTP/HTTPS and SOCKS5 proxies. |
| `price_min`    | number | Optional minimum price filter. Mapped to Amazon `low-price`. |
| `price_max`    | number | Optional maximum price filter. Mapped to Amazon `high-price`. |
| `--pages`      | number | Max number of pages to fetch (default: 1). Each page has ~20-60 results. |
| `--num-products` | number | Max number of products to fetch. Stops when limit is reached, even if more pages available. |
| `--incremental` | flag | Only output new results that haven't been cached before. |
| `--clear-cache` | flag | Clear cache for this keyword before searching. |
| `--output`      | string | Custom output directory for results (default: `results/`). |
| `--download`    | flag | Download product images after search using `@t2p/image-cache`. |

## Output Format
Returns a JSON object containing search metadata and an array of Amazon product objects.

Results are automatically saved to `results/<keyword>_<timestamp>_<count>.json`.

```json
{
  "keyword": "shirt",
  "timestamp": "2026-04-06T12:34:56.789Z",
  "count": 10,
  "items": [
    {
      "id_": "B09TPN9NJ6",
      "uuid": "418e2c7d-ccaa-4ca3-9d1b-6b4f3bd406b0",
      "original_image_url": "https://m.media-amazon.com/images/I/91YprRrDB4L._AC_UL960_FMwebp_QL65_.jpg",
      "title": "Amazon Essentials Men's Slim-Fit Crewneck T-Shirts, Short Sleeve",
      "item_page": "https://www.amazon.com/dp/B09TPN9NJ6",
      "rating": 4.4,
      "review_count": 1787,
      "price": "$19.99",
      "description": "Amazon Essentials Men's Slim-Fit Crewneck T-Shirts, Short Sleeve"
    }
  ]
}
```

### Item Fields

| Field | Type | Description |
|-------|------|-------------|
| `id_` | string | Amazon ASIN (Amazon Standard Identification Number) |
| `uuid` | string | Unique identifier from Amazon's data attributes |
| `original_image_url` | string | Product image URL (highest resolution from srcset) |
| `title` | string | Product title |
| `item_page` | string | Full URL to the product page |
| `rating` | number | Average rating (1-5) |
| `review_count` | number | Number of reviews |
| `price` | string | Price as displayed on Amazon (includes currency) |
| `description` | string | Product description (may be same as title if no separate description) |

## Execution

Use the script at `scripts/amazon_search.ts`.

All TypeScript files must be run with **Bun**:

```bash
# Simple search
bun run scripts/amazon_search.ts "shirt"
```

### Configuration Tool

Use `scripts/configure.ts` to generate environment variable commands and manage cache:

```bash
# Generate proxy setting command (copy and run the output)
bun run scripts/configure.ts proxy "http://127.0.0.1:7890"

# List cache files
bun run scripts/configure.ts listcache

# Clear cache for specific keyword
bun run scripts/configure.ts clearcache "shirt"

# Clear all caches
bun run scripts/configure.ts clearcache --all
```

## Usage Notes

- **Runtime**: All TypeScript files must be run with `bun run`
- **Search Method**: Uses **Playwright** to search Amazon directly in a headless browser (no manual cookie management needed)
- **Proxy Support**: Proxy is read from `T2P_PROXY` environment variable (or `--proxy` CLI flag). Supports both HTTP/HTTPS and SOCKS5 proxies (e.g., `socks5://127.0.0.1:1080`).
- **Cache & Deduplication**: Search results are cached to `resultscache/<sanitizedQuery>_cache.md`. Each line is an ASIN/uuid used for deduplication.
- **Incremental Mode**: Use `--incremental` to output only items not present in the cache.
- **Clear Cache**: Use `--clear-cache` to delete this keyword cache before searching, or use `scripts/configure.ts clearcache`.
- **Custom Output**: Use `--output=/path/to/dir` to save results to a custom directory.
- **Download Images**: Use `--download` to automatically download product images using `@t2p/image-cache` after search completes.

## Example
All commands use `bun run`:

```bash
# Simple search
bun run scripts/amazon_search.ts "t-shirt"

# Incremental search - only output new results not in cache
bun run scripts/amazon_search.ts "t-shirt" --incremental

# Clear cache before searching
bun run scripts/amazon_search.ts "t-shirt" --clear-cache --incremental

# Use proxy
bun run scripts/amazon_search.ts "t-shirt" --incremental --proxy "http://127.0.0.1:10809"

# Multi-page search (fetch 2 pages, ~40-120 results)
bun run scripts/amazon_search.ts "t-shirt" --pages=2

# Multi-page + incremental (only new items from all pages)
bun run scripts/amazon_search.ts "t-shirt" --pages=2 --incremental

# Limit to specific number of products (stops early if limit reached)
bun run scripts/amazon_search.ts "t-shirt" --pages=5 --num-products=50

# Specify custom output directory
bun run scripts/amazon_search.ts "t-shirt" --output=/path/to/custom/results

# Download images after search
bun run scripts/amazon_search.ts "t-shirt" --download

# Combined: search with download and custom output
bun run scripts/amazon_search.ts "t-shirt" --download --output=/path/to/results
```

## Error Handling
| Situation | What to do |
|---|---|
| HTTP 4xx/5xx / Search blocked | Amazon may be rate-limiting; try again later with a different proxy, or wait before retrying |
| Parse errors / empty results | Page layout may have changed; try different keywords, pages, or filters |
| Playwright launch errors | Ensure Playwright browsers are installed: `cd scripts && npx playwright install chromium` |
