---
name: easyship-official
description: "Official Easyship Integration. Ship, label, track & pickup across 550+ couriers in 200+ countries. Connects to mcp.easyship.com — no install required"
homepage: https://github.com/easyship/easyship-mcp
source: https://github.com/easyship/easyship-mcp
tools:
  - get_rates
  - track_shipment
  - create_shipment
  - update_shipment
  - list_shipments
  - get_shipment
  - delete_shipment
  - cancel_shipment
  - create_label
  - get_shipment_documents
  - list_pickups
  - get_pickup
  - cancel_pickup
  - get_pickup_slots
  - create_pickup
  - list_pickup_shipments
  - list_transactions
  - list_billing_transactions
  - validate_address
  - analytics_top_destinations
  - analytics_shipments
  - analytics_shipped
  - analytics_shipment_status
  - analytics_top_couriers
  - analytics_sale_channels
mcp:
  server: https://mcp.easyship.com
  transport: streamable-http
env:
  EASYSHIP_API_ACCESS_TOKEN:
    required: true
    description: "Easyship API token — get one at https://app.easyship.com/connect"
metadata:
  openclaw:
    primaryEnv: EASYSHIP_API_ACCESS_TOKEN
    requires:
      env:
        - EASYSHIP_API_ACCESS_TOKEN
---

> v0.4.0 — 25 tools across shipping, tracking, pickups, billing, address validation, and analytics.

## Shipping rates

### get_rates

Use when the user asks about shipping costs, delivery times, courier options, or the cheapest/fastest way to ship.

**Required inputs:** origin country, destination country, parcel weight, dimensions (length/width/height).

**Optional (improves accuracy):** city, state, postal code, street address for origin and destination. Item category or HS code for duty estimates.

**Presenting results:**
- Show a comparison table: courier name, price, currency, estimated delivery days.
- Sort by price (lowest first) unless the user asks for fastest.
- If you used assumed/estimated data (e.g. generic postal codes), tell the user the rates are estimates.

## Shipments

### create_shipment

The primary tool for creating shipments and buying labels.

**For "ship this" / "buy a label":** set `buy_label: true` and `buy_label_synchronous: true` with `format: "url"` in printing options. Extract the label URL from `shipping_documents` in the response and present it as a clickable link.

**For a specific courier** (e.g. "buy a label with UPS Ground"): call `get_rates` first to find the `courier_id`, then pass it in `courier_settings`.

**Without a specific courier:** omit `courier_service_id` — the API auto-selects best value. Do NOT call `get_rates` first.

**Required inputs:** complete origin and destination addresses (contact name, email, phone, street, city, country code, and company name for origin), parcel weight, item description and customs value.

### update_shipment / get_shipment / list_shipments / delete_shipment / cancel_shipment

- `get_shipment` — retrieves full shipment details. Also use this to get label/document download URLs (pass `format="URL"`).
- `list_shipments` — filter by state, date range, country, etc. Supports label_state, delivery_state, shipment_state filters.
- `delete_shipment` — removes a shipment that hasn't shipped yet.
- `cancel_shipment` — cancels a shipped shipment (only if label failed or shipment not yet in transit).

### create_label

The preferred way to buy a label for an existing shipment. Use this instead of passing `buy_label` via `update_shipment`.

**Required input:** `easyship_shipment_id`.

**Optional:** `courier_service_id` (omit to auto-select), `format` (url/pdf/png/zpl, default "url"), `label`/`commercial_invoice`/`packing_slip` page sizes, `remarks`.

**After calling:** Find the `shipping_documents` entry with `"category": "label"` and present its URL as a clickable link. Include packing slip and commercial invoice URLs if present.

### get_shipment_documents

Returns metadata only (content type, size). For actual document downloads, use `get_shipment` with `format="URL"` instead.

## Tracking

### track_shipment

Use when the user asks to track a package, check delivery status, or says "where's my shipment."

**Required input:** either `easyship_shipment_id` or `platform_order_number` — at least one must be provided.

**Presenting results:**
- Current status, last known location, estimated delivery date.
- List recent tracking checkpoints.

## Pickups

### get_pickup_slots → create_pickup

**Workflow for scheduling a pickup:**
1. Get the `courier_service_id` from the shipment via `get_shipment`
2. Call `get_pickup_slots` to find available dates and time windows
3. Present options to the user (or pick the earliest if they want the closest)
4. Call `create_pickup` with the chosen slot, date, and shipment IDs

All shipments in a pickup must use the same courier and have labels pending or generated.

### list_pickups / get_pickup / cancel_pickup / list_pickup_shipments

Standard CRUD for managing existing pickups.

## Address validation

### validate_address

Validates both US domestic and international addresses in a single tool. Omit `country_alpha2` or pass "US" for domestic; any other country code routes to international validation.

> Requires an updated contract with Easyship.

## Billing

### list_transactions / list_billing_transactions

View transaction history filtered by type (shipment, pickup, claim, policy, payment), date range, or shipment ID.

## Analytics

Six analytics tools, all defaulting to a 90-day lookback if the user doesn't specify a date range:

| Tool | Use for | Returns |
|------|---------|---------|
| `analytics_shipments` | Shipment volume and trends | Total count + daily time series |
| `analytics_shipped` | Past shipping activity confirmation | Whether account has ever shipped |
| `analytics_shipment_status` | Status distribution | Counts by status (in-progress breakdown) |
| `analytics_top_destinations` | Where shipments go | Countries/zones ranked by volume |
| `analytics_top_couriers` | Courier usage breakdown | Couriers ranked by shipment count |
| `analytics_sale_channels` | Sales channel breakdown | Channels ranked by shipment count |

## General

- Easyship supports 550+ couriers across 200+ countries/territories.
- An API token is required. If not configured, direct the user to: https://app.easyship.com/connect
- All prices are returned in the user's Easyship account currency unless specified otherwise.
- Always confirm destructive actions (delete/cancel) with the user before executing.
