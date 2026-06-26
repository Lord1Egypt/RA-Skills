# Structured Data Extraction Reference

Complete reference for extracting structured data from 40+ platforms via `bdata pipelines`.

## Command Syntax

```bash
bdata pipelines <type> [params...] [options]
bdata pipelines list  # List all available types
```

## All Options

| Flag | Description | Default |
|------|-------------|---------|
| `--format <fmt>` | Output format: `json`, `csv`, `ndjson`, `jsonl` | `json` |
| `--timeout <seconds>` | Polling timeout | `600` |
| `-o, --output <path>` | Write output to file | stdout |
| `--json` | Force JSON output | *(off)* |
| `--pretty` | Pretty-print JSON | *(off)* |

## How Pipelines Work

1. CLI sends a trigger request to Bright Data's Web Data API
2. Receives a `snapshot_id`
3. Polls until data collection is complete
4. Returns structured JSON (or CSV/NDJSON)

Default timeout: 600 seconds (10 minutes). Increase with `--timeout` for large datasets.

---

## E-Commerce

| Type | Platform | Parameters | Returns |
|------|----------|------------|---------|
| `amazon_product` | Amazon | `<url>` | Price, title, rating, images, specs, seller |
| `amazon_product_reviews` | Amazon | `<url>` | Reviews with rating, text, date, verified status |
| `amazon_product_search` | Amazon | `<keyword> <domain_url>` | Search results with products |
| `walmart_product` | Walmart | `<url>` | Price, title, rating, availability |
| `walmart_seller` | Walmart | `<url>` | Seller info and metrics |
| `ebay_product` | eBay | `<url>` | Listing details, bids, price |
| `bestbuy_products` | Best Buy | `<url>` | Product details and pricing |
| `etsy_products` | Etsy | `<url>` | Listing details, seller info |
| `homedepot_products` | Home Depot | `<url>` | Product specs and pricing |
| `zara_products` | Zara | `<url>` | Product details and sizes |
| `google_shopping` | Google Shopping | `<url>` | Price comparison across sellers |

### Examples
```bash
# Amazon product details
bdata pipelines amazon_product "https://amazon.com/dp/B09V3KXJPB"

# Amazon search
bdata pipelines amazon_product_search "wireless headphones" "https://amazon.com"

# Amazon reviews
bdata pipelines amazon_product_reviews "https://amazon.com/dp/B09V3KXJPB"

# Walmart product
bdata pipelines walmart_product "https://walmart.com/ip/123456"

# Export to CSV
bdata pipelines amazon_product "https://amazon.com/dp/B09V3KXJPB" --format csv -o product.csv
```

---

## Professional Networks

| Type | Platform | Parameters | Returns |
|------|----------|------------|---------|
| `linkedin_person_profile` | LinkedIn | `<url>` | Name, headline, experience, education, skills |
| `linkedin_company_profile` | LinkedIn | `<url>` | Company info, size, industry, about |
| `linkedin_job_listings` | LinkedIn | `<url>` | Job details, requirements, salary |
| `linkedin_posts` | LinkedIn | `<url>` | Post content, engagement metrics |
| `linkedin_people_search` | LinkedIn | `<url> <first> <last>` | Matching profiles |
| `crunchbase_company` | Crunchbase | `<url>` | Funding, employees, investors |
| `zoominfo_company_profile` | ZoomInfo | `<url>` | Company data, contacts, tech stack |

### Examples
```bash
# LinkedIn profile
bdata pipelines linkedin_person_profile "https://linkedin.com/in/satyanadella"

# LinkedIn company
bdata pipelines linkedin_company_profile "https://linkedin.com/company/microsoft"

# People search
bdata pipelines linkedin_people_search "https://linkedin.com/search/results/people" "Jane" "Smith"

# Crunchbase
bdata pipelines crunchbase_company "https://crunchbase.com/organization/openai"
```

---

## Social Media — Instagram

| Type | Parameters | Returns |
|------|------------|---------|
| `instagram_profiles` | `<url>` | Bio, followers, following, post count |
| `instagram_posts` | `<url>` | Caption, likes, comments count, media |
| `instagram_reels` | `<url>` | Reel data, views, engagement |
| `instagram_comments` | `<url>` | Comment text, author, likes |

```bash
bdata pipelines instagram_profiles "https://instagram.com/natgeo"
bdata pipelines instagram_posts "https://instagram.com/p/..."
bdata pipelines instagram_reels "https://instagram.com/reel/..."
bdata pipelines instagram_comments "https://instagram.com/p/..."
```

---

## Social Media — TikTok

| Type | Parameters | Returns |
|------|------------|---------|
| `tiktok_profiles` | `<url>` | Bio, followers, likes, video count |
| `tiktok_posts` | `<url>` | Video details, views, engagement |
| `tiktok_shop` | `<url>` | Product data from TikTok Shop |
| `tiktok_comments` | `<url>` | Comment text, author, likes |

```bash
bdata pipelines tiktok_profiles "https://tiktok.com/@username"
bdata pipelines tiktok_posts "https://tiktok.com/@username/video/..."
bdata pipelines tiktok_shop "https://tiktok.com/..."
bdata pipelines tiktok_comments "https://tiktok.com/@username/video/..."
```

---

## Social Media — Facebook

| Type | Parameters | Returns |
|------|------------|---------|
| `facebook_posts` | `<url>` | Post content, reactions, shares |
| `facebook_marketplace_listings` | `<url>` | Listing price, location, details |
| `facebook_company_reviews` | `<url> [num]` | Reviews with rating and text |
| `facebook_events` | `<url>` | Event details, date, location |

```bash
bdata pipelines facebook_posts "https://facebook.com/page/posts/..."
bdata pipelines facebook_marketplace_listings "https://facebook.com/marketplace/item/..."
bdata pipelines facebook_company_reviews "https://facebook.com/company" 25
bdata pipelines facebook_events "https://facebook.com/events/..."
```

---

## Social Media — YouTube

| Type | Parameters | Returns |
|------|------------|---------|
| `youtube_profiles` | `<url>` | Channel name, subscribers, video count |
| `youtube_videos` | `<url>` | Title, views, likes, description |
| `youtube_comments` | `<url> [num]` | Comment text, author, likes (default: 10) |

```bash
bdata pipelines youtube_profiles "https://youtube.com/@channel"
bdata pipelines youtube_videos "https://youtube.com/watch?v=..."
bdata pipelines youtube_comments "https://youtube.com/watch?v=..." 50
```

---

## Social Media — Other

| Type | Platform | Parameters | Returns |
|------|----------|------------|---------|
| `x_posts` | X (Twitter) | `<url>` | Tweet text, likes, retweets, replies |
| `reddit_posts` | Reddit | `<url>` | Post content, score, comments |

```bash
bdata pipelines x_posts "https://x.com/user/status/..."
bdata pipelines reddit_posts "https://reddit.com/r/sub/comments/..."
```

---

## Google Services

| Type | Platform | Parameters | Returns |
|------|----------|------------|---------|
| `google_maps_reviews` | Google Maps | `<url> [days]` | Reviews with rating, text, date (default: 3 days) |
| `google_play_store` | Google Play | `<url>` | App details, rating, reviews |
| `google_shopping` | Google Shopping | `<url>` | Price comparison data |

```bash
bdata pipelines google_maps_reviews "https://maps.google.com/maps/place/..." 7
bdata pipelines google_play_store "https://play.google.com/store/apps/details?id=..."
```

---

## Other Platforms

| Type | Platform | Parameters | Returns |
|------|----------|------------|---------|
| `apple_app_store` | Apple App Store | `<url>` | App details, rating, reviews |
| `reuter_news` | Reuters | `<url>` | Article content, date, author |
| `github_repository_file` | GitHub | `<url>` | Repository file content |
| `yahoo_finance_business` | Yahoo Finance | `<url>` | Stock price, financials, company data |
| `zillow_properties_listing` | Zillow | `<url>` | Property details, price, features |
| `booking_hotel_listings` | Booking.com | `<url>` | Hotel details, price, amenities |

```bash
bdata pipelines apple_app_store "https://apps.apple.com/app/..."
bdata pipelines yahoo_finance_business "https://finance.yahoo.com/quote/AAPL"
bdata pipelines zillow_properties_listing "https://zillow.com/homedetails/..."
bdata pipelines booking_hotel_listings "https://booking.com/hotel/..."
```

---

## Output Formats

```bash
# JSON (default)
bdata pipelines amazon_product "<url>"

# CSV (great for spreadsheets)
bdata pipelines amazon_product "<url>" --format csv -o product.csv

# NDJSON (one JSON object per line — great for streaming)
bdata pipelines amazon_product "<url>" --format ndjson

# Pretty JSON (human-readable)
bdata pipelines amazon_product "<url>" --pretty
```

## Tips

- **Always prefer pipelines over scrape + parse** when a pre-built extractor exists — structured JSON is more reliable than parsing markdown.
- **Check `bdata pipelines list`** first — new extractors are added regularly.
- **Increase timeout for large datasets** — `--timeout 1200` for big jobs.
- **Use CSV for spreadsheet workflows** — `--format csv -o data.csv` exports cleanly.
- **Pipeline jobs are async internally** — the CLI handles polling automatically, but you can increase the timeout if needed.
