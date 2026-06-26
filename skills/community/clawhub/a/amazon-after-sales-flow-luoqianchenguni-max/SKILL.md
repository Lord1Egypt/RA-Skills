---
name: amazon-after-sales-flow
description: Automate Amazon after-sales end-to-end: open 2025 orders, open order details, run contact flow, and draft/send seller messages with explicit send confirmation.
---

# Amazon After-Sales Flow

Playwright-based Amazon after-sales automation with explicit send confirmation.

## Runtime Requirements

This skill requires a JS runtime and Playwright binaries.

Required environment:
- Node.js >= 18
- npm dependencies installed
- Playwright Chromium installed

Expected setup before use:
- `npm install`
- `npx playwright install chromium`

## Full-Flow Behavior

1. Open Amazon orders page (`year` from input when provided).
2. Find an order and open order details.
3. Run contact flow chain.
4. Type message and only send if explicitly confirmed.

## Input Modes

1. Natural language:
- `run amazon-after-sales-flow 2025`
- `execute amazon-after-sales-flow 2025`

2. JSON actions:
- `{"action":"run_full_flow", ...}`
- `{"action":"open_orders", ...}`
- `{"action":"run_contact_flow", ...}`
- `{"skill":"amazon_contact_flow","args":{...}}`

## Safety And Data Handling

- Legacy shell URL opener is removed.
- URL-only free text input is blocked.
- Sending requires both `auto_send=true` and `confirm_send=true`.
- The runtime can read page DOM on Amazon order/messaging pages to complete the workflow.
- Local artifacts may be stored in workspace files.
- No external upload endpoint is configured by default in this package.

## Output

Returns runtime JSON traces/results for executed actions.
