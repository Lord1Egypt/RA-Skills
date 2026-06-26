---
name: farmos-marketing
description: Query grain marketing positions, contracts, delivery schedules, inventory, and revenue data. Requires authentication — manager role minimum for dashboard, admin for full access.
tags: [farming, marketing, grain, contracts]
---

# FarmOS Marketing

Grain marketing positions, contracts, deliveries, settlements, inventory, and revenue analysis for a corn/soybean operation with 3 entities across ~4,000 acres.

## When This Skill Triggers

- "What's our marketing position?"
- "How much corn have we sold?"
- "Show the dashboard summary"
- "Any deliveries coming up?"
- "What's our average corn price?"
- "Bushels remaining to sell?"
- "Revenue by entity"
- "Show open contracts"
- "Basis levels?"
- "Settlement history"

## Data Completeness

1. **Dashboard endpoint truncates results.** Use `/api/integration/dashboard` for summary stats only — NOT for listing positions, deliveries, or settlements.
2. **Always state the total count** of records returned: "Found 23 open positions totaling 145,000 bushels of corn."
3. **If a query returns suspiciously few results**, say so: "I'm only seeing 3 positions — that may be incomplete."
4. **Use authenticated endpoints for complete data** — integration endpoints are for quick summaries, not full listings.
5. **If an endpoint fails**, report the failure rather than silently showing partial data.

## Authentication

This skill accesses protected FarmOS endpoints that require a JWT token.

**To get a token:** Run the auth helper with the appropriate role:
```bash
TOKEN=$(~/clawd/scripts/farmos-auth.sh admin)
# or for manager-level access:
TOKEN=$(~/clawd/scripts/farmos-auth.sh manager)
```

**To use the token:** Include it as a Bearer token:
```bash
curl -H "Authorization: Bearer $TOKEN" http://100.102.77.110:8013/api/endpoint
```

**Token expiry:** Tokens last 15 minutes. If you get a 401 response, request a new token.

**Role mapping:** Check the sender's role in `~/.clawdbot/farmos-users.json`. If the user is not admin or manager, tell them they don't have access to marketing data.

## API Base

http://100.102.77.110:8013

## Integration Endpoints (No Auth — for cross-module data)

These provide summary data without authentication. Use for quick lookups and cron jobs.

### Dashboard Summary
GET /api/integration/dashboard

Returns: Contract counts, bushels sold, delivery schedule stats, recent settlements.

### Revenue Summary
GET /api/integration/revenue?crop_year=2025&entity_id=1

Returns: Revenue by crop (corn/soybeans), by month, contracted vs projected. Use for cash flow analysis.

### Entities
GET /api/integration/entities

Returns: All farm entities with id, name, type, short_code. Use to map entity names to IDs.

### Fields with Ownership
GET /api/integration/fields?entity_id=1

Returns: Fields with acres, entity ownership shares.

### Acres Summary
GET /api/integration/acres-summary

Returns: Total acres by entity with field counts and ownership shares.

### Settlements by Month
GET /api/integration/settlements-by-month?crop_year=2025&entity_id=1

Returns: Monthly settlement amounts for cash flow timing.

### Crop Years
GET /api/integration/crop-years

Returns: Available crop years with current year flag.

## Authenticated Endpoints (JWT Required)

### Dashboard Summary (Full)
GET /api/dashboard/summary?crop_year=2025
Authorization: Bearer {token}
Requires: manager+

Returns comprehensive marketing dashboard:
- Crop year settings (expected yield, expected price per crop)
- Per-entity, per-crop breakdown:
  - total_bushels, hedged/sold/basis/hta/open bushels
  - percent_marketed
  - contracted_revenue, projected_revenue, settled_revenue
  - needs_bushel_transfer warnings
- Totals by crop

This is the primary endpoint for "how are we positioned?" questions.

### Positions (Contracts)
GET /api/positions?crop_year=2025
Authorization: Bearer {token}
Requires: manager+

Query params: crop_year, crop (corn|soybeans), entity_id, status (open|fulfilled|cancelled), type (Hedge|Cash Sale|Basis|HTA)

Returns: List of marketing positions/contracts with:
- contract_number, crop, type, entity
- quantity (bushels), entry_price, basis
- delivery_start, delivery_end, buyer
- status, lifecycle info

### Positions Export
GET /api/positions/export?crop_year=2025
Authorization: Bearer {token}
Requires: manager+

Returns: CSV export of all positions.

### Deliveries (Scale Tickets)
GET /api/deliveries?crop_year=2025
Authorization: Bearer {token}

Returns: Delivery records with ticket numbers, dates, quantities, moisture, test weight.

### Settlements (Payments)
GET /api/settlements?crop_year=2025
Authorization: Bearer {token}

Returns: Settlement records — payments received from buyers.

### Inventory
GET /api/inventory?crop_year=2025
Authorization: Bearer {token}

Returns: Current grain inventory status — what's in bins vs sold vs delivered.

### Crop Year Settings
GET /api/crop-year-settings?crop_year=2025
Authorization: Bearer {token}

Returns: Expected yield and expected price per crop for the year. These drive projected revenue and percent marketed calculations.

## Key Concepts

- **Position types:** Hedge (futures only), Cash Sale (flat price), Basis (basis only), HTA (futures locked, basis open)
- **Percent marketed:** bushels_sold / total_expected_bushels x 100
- **Entity:** A farm legal entity (e.g., "Fields of Dreams", "ILMG"). Each has its own positions and production.
- **Crop year:** The year the crop is grown (2025 = planted spring 2025, harvested fall 2025, may deliver into 2026).
- **Bushel transfers (PIK):** When one entity is oversold, bushels transfer from another entity to cover.

## Cross-Module Context

The team agent's marketing access is read-only and logistics-scoped. Use it to connect delivery deadlines to field operations:

**Marketing → Field Ops:**
- During harvest and delivery windows, check delivery schedules when discussing field work priorities. Delivery commitments determine which fields get harvested first: "There's a 5,000-bu bean delivery to ADM due next week. Priority on the bean fields."
- When crew asks about harvest sequencing or field priorities, reference delivery deadlines and contract obligations.
- Flag tight timelines: "Cargill delivery window closes in 10 days and you've only delivered 60% of that contract. Might want to bump those fields up."

**Marketing → Equipment:**
- During harvest, connect delivery deadlines to equipment availability: "You've got 3 deliveries due this week — make sure the grain cart and trucks are ready."

Don't cross-reference marketing on every field ops question. This matters during harvest, delivery windows, and when logistics questions come up. Not during routine spraying or maintenance.

## Usage Notes

- Always include crop_year parameter (default to current: 2025, use 2026 when appropriate).
- The dashboard summary is the best "big picture" endpoint.
- For specific contract questions, use positions with filters.
- Revenue data from integration endpoints doesn't require auth — good for cron jobs and summaries.
- When discussing positions, include the entity name, crop, type, quantity, and price.
- Flag any positions marked as "needs_bushel_transfer" — this means an entity has sold more than it can produce.
- The entities are: check /api/integration/entities for current list and IDs.
