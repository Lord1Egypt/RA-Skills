---
name: rollinggo-hotel
description: Hotel search and pricing via the RollingGo CLI. Use when the user wants to search hotels by destination, filter by date/star/budget/tags/distance, inspect hotel detail and room pricing, or look up hotel tags. Trigger phrases — "search hotels", "find hotels near", "hotel detail", "hotel pricing", "hotel tags", "rollinggo".
homepage: https://mcp.agentichotel.cn
metadata:
  {
    "openclaw": {
      "emoji": "🏨",
      "primaryEnv": "AIGOHOTEL_API_KEY",
      "requires": {
        "anyBins": ["rollinggo", "npx", "node", "uvx", "uv"],
        "env": ["AIGOHOTEL_API_KEY"]
      },
      "install": [
        {
          "id": "node",
          "kind": "node",
          "package": "rollinggo",
          "bins": ["rollinggo"],
          "label": "Install rollinggo (npm)"
        },
        {
          "id": "uv",
          "kind": "uv",
          "package": "rollinggo",
          "bins": ["rollinggo"],
          "label": "Install rollinggo (uv)"
        }
      ]
    }
  }
---

# RollingGo Hotel CLI

## When to Use

✅ **Use this skill when:**
- **Searching Candidates:** User wants to find hotels near a specific city, landmark, or address (e.g., "Find hotels near Tokyo Disneyland").
- **Complex Filtering:** User needs to narrow down options using natural language queries combined with exact dates, guest count, star ratings, budget limits, or distance radius.
- **Tag & Brand Matching:** User wants to find hotels with specific attributes (e.g., "family friendly", "breakfast included", "Marriott") by first checking the tag dictionary to build exact filters.
- **Deep Dive & Pricing:** User wants to inspect detailed room plans, real-time pricing, cancellation policies, or availability for a specific hotel ID.
- **Comparison & Evaluation:** User wants to compare multiple candidate hotels based on returning structured data and current rates.
- **Hotel Booking:** User is ready to select a room and book a hotel. The returned booking URLs and detail page links can be provided to guide the user to complete their reservation.

❌ **Don't use this skill when:**
- User asks about non-hotel travel booking (flights, trains, transfers, car rentals).

## API Key

Resolution order: `--api-key` flag → `AIGOHOTEL_API_KEY` env var.

No key yet? Apply at: https://mcp.agentichotel.cn/apply

## Runtime

Choose based on user's environment. Load the matching reference file and keep it for the session.

- **`npm`, `npx`, Node, or no preference:** Load [references/rollinggo-npx.md](references/rollinggo-npx.md)
- **`uv`, `uvx`, PyPI, or Python:** Load [references/rollinggo-uv.md](references/rollinggo-uv.md)
- **Parity check or both:** Load both references

Default when unspecified → **npm/npx** (broader env compatibility).

## Primary Workflow

Run these steps in order unless the user is already at a later step.

1. Clarify: destination, dates, nights, occupancy, budget, stars, tags, distance
2. If tag filters needed → run `hotel-tags` first to get valid tag strings
3. Run `search-hotels` → parse JSON → extract `hotelId`
4. Run `hotel-detail --hotel-id <id>` for room plans and pricing
5. If results are weak → loosen filters and retry

## Commands Quick Reference

```bash
# Discover tags
rollinggo hotel-tags

# Search hotels (minimum required flags)
rollinggo search-hotels \
  --origin-query "<user's natural language request>" \
  --place "<destination>" \
  --place-type "<value from --help>"

# Hotel detail with pricing
rollinggo hotel-detail \
  --hotel-id <id> \
  --check-in-date YYYY-MM-DD \
  --check-out-date YYYY-MM-DD \
  --adult-count 2 --room-count 1

# Discover all flags
rollinggo search-hotels --help
rollinggo hotel-detail --help
```

## Key Rules

- `--place-type` must use exact values from `rollinggo search-hotels --help`
- `--star-ratings` format: `min,max` e.g. `4.0,5.0`
- `--format table` allowed **only** on `search-hotels`; rejected by `hotel-detail` and `hotel-tags`
- `--child-count` must match the count of `--child-age` flags
- `--check-out-date` must be later than `--check-in-date`
- Prefer `--hotel-id` over `--name` whenever available

## Output

- stdout → result payload (JSON by default)
- stderr → errors only
- Exit `0` success · `1` HTTP/network failure · `2` CLI validation failure
- Results include booking URLs and hotel detail page links for downstream use

## Filter Loosening (when no results)

Try in order: remove `--star-ratings` → increase `--size` → increase `--distance-in-meter` → remove tag filters → widen dates or budget
