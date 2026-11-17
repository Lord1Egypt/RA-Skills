---
name: "danish-grocery-deals"
description: "Scrape Danish supermarket weekly tilbudsaviser (Lidl, Rema 1000, Netto, Meny, 365 discount) from the Tjek API and push filtered wow deals to ntfy.sh"
---

# Danish Grocery Deals (Tilbudsavis) + ntfy.sh

Weekly scraper for Danish supermarket tilbudsaviser (Lidl, Rema 1000, Netto,
Meny, 365 discount) that pushes only the genuinely cheap "wow" deals to your
phone via ntfy.sh, plus a full organized deal list as a file attachment.

## What it does

- Reads the weekly digital aviser of 5 Danish chains via the Tjek API
  (the platform behind etilbudsavis.dk and the stores' own aviser)
- Picks the current/upcoming weekly catalog per store, paginates all offers
- Extracts weight, per-kg / per-l / per-piece prices and discount %
- Keeps only "wow" deals: interest matches below a per-category price bar,
  or any deal with >= 40% discount, capped at 18 items
- Publishes to ntfy.sh: the wow summary + the full list as an attachment
  (full list ordered by supermarket, then by category)
- Dedupes per day so re-runs don't spam

## Files

- `scripts/tilbudsavis.py`  scraper (Tjek API, metrics, wow filter, full list)
- `scripts/notify.py`       publisher (runs scraper, pushes to ntfy.sh)
- `templates/config.json`   stores, interests, wow thresholds, ntfy settings
- `templates/deals-notify.service` / `.timer`  systemd weekly schedule

## Setup

1. Copy `templates/config.json` next to the two scripts (same directory).
2. Fill in the config:
   - `api_key`: Tjek API browser key (see "Tjek API notes" below)
   - `ntfy.topic`: your ntfy.sh topic (use a random suffix for privacy)
   - `stores`: dealer ids for chains (defaults cover the 5 Danish chains)
   - `interests`: keyword lists, exclude lists, and wow thresholds
3. Test: `python3 tilbudsavis.py` prints the summary between markers
4. Notify: `python3 notify.py` runs the scraper and pushes to ntfy.sh
5. Schedule weekly (Sunday morning, when all new aviser are out):
   systemd timer (see templates) or `0 9 * * 0` cron

## Config reference

```jsonc
{
  "api_key": "YOUR_TJEK_API_KEY",
  "api_base": "https://squid-api.tjek.com",
  "ntfy": { "url": "https://ntfy.sh", "topic": "tilbudsavis-RANDOM", "token": "" },
  "stores": [
    { "id": "71c90", "name": "Lidl", "avis_url": "https://etilbudsavis.dk/Lidl" },
    { "id": "11deC", "name": "Rema 1000", "avis_url": "https://etilbudsavis.dk/REMA-1000" },
    { "id": "9ba51", "name": "Netto", "avis_url": "https://etilbudsavis.dk/Netto" },
    { "id": "267e1m", "name": "Meny", "avis_url": "https://etilbudsavis.dk/MENY" },
    { "id": "DWZE1w", "name": "365 discount", "avis_url": "https://etilbudsavis.dk/365discount" }
  ],
  "interests": [
    {
      "category": "Oksekod",
      "emoji": "🥩",
      "keywords": ["oksekod", "bøf", "steak", "mørbrad", ...],
      "exclude": ["steak fries", "pommes"],
      "wow": { "max_price_per_kg": 60, "min_discount_pct": 40 }
    }
  ]
}
```

### Wow filter per interest
- `max_price_per_kg` / `max_price_per_l` / `max_price_per_piece`: keep deal if
  unit price is at or below this bar
- `min_discount_pct`: keep deal if discount vs "før" price is >= this
- Any deal with >= 40% discount also qualifies for the general wow section
- Cap: `MAX_WOW_ITEMS = 18`, `MAX_PER_INTEREST = 4` (edit in tilbudsavis.py)

### Tjek API notes (gotchas)
- Catalogs: `GET /v2/catalogs?dealer_id=<id>` (camelCase `retailerId` is IGNORED)
- Offers: `GET /v2/offers?catalog_id=<id>&limit=100&offset=<n>` (max limit 100,
  paginate by offset; filter results client-side by `catalog_id`)
- Dealer ids (DK): Lidl `71c90`, Rema 1000 `11deC`, Netto `9ba51`,
  Meny `267e1m`, 365 discount `DWZE1w`. Discover others via
  `GET /v2/dealers?country=DK&limit=200&page=N`
- The browser API key is embedded in etilbudsavis.dk's JS bundle
  (`assets/entry-client-*.js`, look for `apiKey:{browser:...}`); it is a
  public read key, no account needed
- Avis weeklies: Lidl/Rema start Sunday, Netto Saturday, Meny/365 Thursday.
  Run Sunday morning to catch all five

### ntfy.sh notes
- Message limit is 4096 bytes; `notify.py` chunks longer text automatically
  (titles get " (1/2)" suffixes)
- Attachments (full deal list) must POST to `https://ntfy.sh/<topic>` with a
  `Filename:` header; posting to the root path fails with 413
- Public topics: use a random topic suffix, or set `ntfy.token` to a ntfy.sh
  access token and the script adds an Authorization header

## Troubleshooting
- `HTTP 400` on catalogs: you used `retailerId` instead of `dealer_id`
- `HTTP 400/500` on offers: limit > 100, or `catalogId` (camelCase) instead of
  `catalog_id`
- `HTTP 413` on attachment: file > ntfy.sh limit, or wrong URL path
- Empty wow list: thresholds too strict (raise `max_price_per_kg` or lower
  `min_discount_pct`), or the week has no standout deals
