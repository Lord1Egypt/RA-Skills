# Amazon After-Sales Flow Skillpack

Playwright-based automation for Amazon after-sales workflows (orders -> order details -> contact flow -> message draft/send).

## Runtime And Install Expectations

This package is NOT instruction-only.

Requirements:
- Node.js >= 18
- npm
- Playwright browser binaries (Chromium)

Install:
- `npm install`
- `npx playwright install chromium`

## OpenClaw Usage

Natural-language trigger examples:
- `run amazon-after-sales-flow 2025`
- `execute amazon-after-sales-flow 2025`

Default full flow:
- open orders -> open order details -> run contact flow -> type message -> optionally send

## Sending Safeguard

Message sending is gated:
- `auto_send=true` AND `confirm_send=true` are both required to send.
- Otherwise it only types draft text.

## Data Scope

The runtime can read visible DOM content from Amazon pages required for this workflow:
- order pages
- order details pages
- messaging pages

It may save local artifacts (for example screenshots/DOM snippets) inside the local skill workspace.
No external upload endpoint is configured by default in this package.

## Included Skills

- `order_reader`
- `evidence_builder`
- `message_drafter`
- `form_filler`
- `amazon_product_detector`
- `amazon_orders_scraper`
- `amazon_orders_opener`
- `amazon_order_details_fetcher`
- `amazon_price_checker`
- `amazon_review_scraper`
- `amazon_contact_flow`
- `message_monitor`
- `price_alert_manager`
- `case_exporter`
