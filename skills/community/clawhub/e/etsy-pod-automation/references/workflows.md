# Etsy POD Automation Workflows

## 1. Trend Research Workflow
1. **Google Trends** – Use Apify Google Trends scraper to fetch weekly interest for keywords.
2. **Etsy Trending Searches** – Pull top 20 search terms via `sovereigntaylor/etsy-scraper`.
3. **Social Media Scan** – Use Apify Instagram/TikTok scrapers for visual trends.
4. **Score Trends** – Apply 5‑factor scoring (volume, growth, competition, Printify feasibility, longevity).\
   - ≥4.0 → create immediately\
   - 3.0‑3.9 → queue for next week\
   - <3.0 → monitor only.
5. Store results in `project/.cache/trends.json` for later steps.

## 2. Design Generation Workflow
1. Prompt AI (Claude/StableDiffusion) with trend keyword and product type.
2. Generate 3‑5 design variations.
3. Upscale images via `image_generate` (2x upscale).\
4. Save to `assets/designs/<keyword>/<variant>.png`.
5. Choose top‑ranked design (based on aesthetic score or user feedback).

## 3. Printify Product Creation Workflow
1. **Discover Shop ID** – `GET https://api.printify.com/v1/shops.json` → store `shop_id`.
2. **Select Blueprint** – `GET /v1/catalog/blueprints.json` → find matching product type (e.g., mug).
3. **Find Provider & Variant** – `GET /v1/catalog/blueprints/{id}/print_providers.json` then `/variants.json`.
4. **Calculate Pricing** – Use pricing formula from SKILL.md.
5. **Create Product** – `POST /v1/shops/{shop_id}/products.json` with:
   - `title` (SEO‑optimized)\
   - `description`\
   - `images` (auto‑mockups)\
   - `variants` (price, options)\
   - `tags` (13 tags from SEO workflow).
6. Store Printify `product_id` for later Etsy sync.

## 4. Etsy Listing Workflow
1. Retrieve Printify product details.
2. Prepare title (≤40 chars front‑loaded keyword) and description.
3. Generate 13 SEO tags (see SEO Tags workflow).
4. Upload images – if Printify mockups <2, generate lifestyle images via `image_generate` and attach.
5. Use Etsy API (`POST /v3/application/shops/{shop_id}/listings`) to create listing with price, shipping, inventory.
6. Save Etsy `listing_id`.

## 5. SEO Tag Generation Workflow
1. **Broad Tags** – 3‑4 high‑volume generic tags (e.g., `mug`, `gift`, `personalized`).\
2. **Long‑Tail Tags** – 8‑9 specific tags covering:
   - Product type & style\
   - Occasion/gift (`valentine‑gift`, `mother‑day‑mug`)\
   - Theme/aesthetic (`minimalist`, `floral`)\
   - Seasonal (`spring`, `summer`)\
   - Trending keywords from Trend Research.
3. Combine into a single comma‑separated list of 13 tags.
4. Validate tag length (<20 chars each) and uniqueness.

## 6. Social Media Promotion Workflow
1. Choose platforms (X, Instagram, Pinterest).
2. Prepare post copy – include product name, key benefit, and Etsy link.
3. Attach primary mockup image.
4. **X** – Use `post_tweet` MCP tool with `media_urls`.
5. **Instagram** – Use Composio two‑step API: create container → publish.
6. **Pinterest** – Browser automation: "Save from URL" with image.
7. Log post URLs in `project/.log/social/<date>.json`.

## 7. Performance Monitoring Workflow
### Daily Checks
- **Etsy Stats** – Pull visits, views, favorites via Etsy Stats API.
- **Search Visibility** – Scrape Etsy SEO page for warnings.
- **Printify Orders** – `GET /v1/shops/{shop_id}/orders.json` for fulfillment status.
### Weekly Review
1. Identify bottom 20 % listings (0 views after 14 days) → retire via Etsy API.
2. Identify top 20 % listings → create 2‑3 variations using Design Generation workflow.
3. Update tags/titles based on actual search data (download Etsy search terms report).
4. Adjust pricing if margin drifts.
5. Log metrics to `project/.metrics/weekly.json`.

## 8. Automation Schedule (Cron)
- **0 8 * * *** – Trend Scan (Workflow 1)\
- **30 9 * * *** – Product Creation (Workflows 2‑4)\
- **0 12 * * *** – Social Media Posting (Workflow 6)\
- **0 18 * * *** – Performance Monitor (Workflow 7)\
- **0 9 * * 1** – Weekly Review (Workflow 7 – weekly).

---

*All API calls require authentication tokens stored in `.env` (`PRINTIFY_API_TOKEN`, `ETSY_API_KEY`, `ETSY_SHOP_ID`). Ensure the token files are secured and not committed to version control.*
