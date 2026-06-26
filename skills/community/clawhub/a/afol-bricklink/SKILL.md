---
name: bricklink
description: Use the self-contained BrickLink API CLI for OAuth1-signed catalog, pricing, order, inventory, feedback, coupon, shipping, notification, and member-note workflows with guarded marketplace writes.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [lego, afol, bricklink, marketplace, inventory, pricing]
    related_skills: [brickowl]
---

# BrickLink AFOL skill

Use this skill when the user asks for BrickLink item lookup, price guides, known colors, images, supersets/subsets, item mapping, orders, inventory, feedback, coupons, notifications, shipping methods, member ratings, or private member notes.

Primary interface: `scripts/bricklink`.

The skill is self-contained for archive distribution and wraps the BrickLink API directly using checked-in references inside this skill directory:
- OpenAPI reference: `references/openapi/bricklink.yaml`
- Domain guidance: `references/prompts/bricklink-tools.txt`
- CLI source: `scripts/bricklink_cli.py`

Do not scrape vendor docs or invent parameters when the checked-in OpenAPI reference covers the endpoint. If the reference is insufficient, say what is missing.

## Authentication

Required environment variables:

```bash
export BRICKLINK_API_CONSUMER_KEY=...
export BRICKLINK_API_CONSUMER_SECRET=...
export BRICKLINK_API_TOKEN_VALUE=...
export BRICKLINK_API_TOKEN_SECRET=...
```

Optional override:

```bash
export BRICKLINK_API_BASE_URL=https://api.bricklink.com/api/store/v1
```

Never print, commit, log, or paste the real OAuth credentials. Commands should reference the `BRICKLINK_API_*` variables only indirectly through the CLI.

BrickLink auth placement matters:
- Every API request is OAuth 1.0a signed with an `Authorization: OAuth ...` header.
- Credentials do not belong in query parameters or JSON request bodies.
- GET query parameters are included in the OAuth signature base string.
- POST/PUT/DELETE JSON request bodies are not where OAuth credentials live.

The CLI handles this split, which is the main reason to use it instead of ad-hoc curl.

## CLI quick reference

Run commands from this skill directory:

```bash
scripts/bricklink --help
scripts/bricklink colors
scripts/bricklink color --color-id 11
scripts/bricklink categories
scripts/bricklink item --type SET --no 75192-1
scripts/bricklink item-price --type SET --no 75192-1 --guide-type sold --new-or-used N --currency-code EUR
scripts/bricklink item-colors --type PART --no 3001
scripts/bricklink item-mapping --type PART --no 3001 --color-id 5
scripts/bricklink element-mapping --element-id 4211111
scripts/bricklink inventory-list --item-type SET --status Y
scripts/bricklink orders --direction in --status PAID
scripts/bricklink order --order-id 123456
scripts/bricklink notifications
scripts/bricklink coupons
scripts/bricklink shipping-methods
scripts/bricklink member-ratings --username example_user
scripts/bricklink member-notes --username example_user
```

Mutating commands are guarded. They do nothing unless passed `--yes`; use `--dry-run` first:

```bash
scripts/bricklink inventory-create --dry-run \
  --json '{"item":{"type":"PART","no":"3001"},"color_id":5,"quantity":1,"unit_price":"0.12","new_or_used":"U"}'

scripts/bricklink inventory-update --dry-run --inventory-id 123456 \
  --json '{"quantity":2,"unit_price":"0.15"}'

scripts/bricklink inventory-delete --dry-run --inventory-id 123456
scripts/bricklink order-status --dry-run --order-id 123456 --json '{"status":"PACKED"}'
scripts/bricklink feedback-create --dry-run --json '{"order_id":123456,"rating":"POSITIVE","comment":"Thank you"}'
scripts/bricklink coupon-create --dry-run --json '{"buyer_name":"example_user","discount_rate":5}'
scripts/bricklink member-notes-update --dry-run --username example_user --json '{"note":"Asked about train parts"}'
```

## Safety rules

Read-only by default:
- `colors`, `color`, `categories`, `category`
- `item`, `item-images`, `item-supersets`, `item-subsets`, `item-price`, `item-colors`
- `item-mapping`, `element-mapping`
- `orders`, `order`, `order-items`, `order-messages`, `order-feedback`
- `inventory-list`, `inventory`
- `feedback`, `feedback-view`
- `notifications`, `coupons`, `coupon`
- `shipping-methods`, `shipping-method`
- `member-ratings`, `member-notes`

Mutating operations require explicit user confirmation in the current conversation before execution:
- `inventory-create`, `inventory-update`, `inventory-delete`
- `order-update`, `order-status`, `order-payment-status`, `order-drive-thru`
- `feedback-create`, `feedback-reply`
- `coupon-create`, `coupon-update`, `coupon-delete`
- `member-notes-create`, `member-notes-update`, `member-notes-delete`

Stored credentials are not permission. Before any mutation, restate the exact action, endpoint, target ID/user/order, payload summary, and whether the action is destructive. Wait for explicit confirmation such as "yes, update BrickLink inventory 123456".

The CLI enforces this mechanically: mutating commands fail unless `--yes` is passed, and `--dry-run` prints the request shape with credentials redacted as environment-variable references.

If the user asks to "sell", "list", "update inventory", "delete lot", "leave feedback", or "create a coupon" without naming a platform and both BrickLink/BrickOwl could apply, ask which marketplace to use before mutating anything.

## Endpoint coverage

- `GET /orders` via `orders`
- `GET /orders/{order_id}` via `order`
- `PUT /orders/{order_id}` via `order-update --yes`
- `GET /orders/{order_id}/items` via `order-items`
- `GET /orders/{order_id}/messages` via `order-messages`
- `GET /orders/{order_id}/feedback` via `order-feedback`
- `PUT /orders/{order_id}/status` via `order-status --yes`
- `PUT /orders/{order_id}/payment_status` via `order-payment-status --yes`
- `POST /orders/{order_id}/drive_thru` via `order-drive-thru --yes`
- `GET /inventories` via `inventory-list`
- `POST /inventories` via `inventory-create --yes`
- `GET /inventories/{inventory_id}` via `inventory`
- `PUT /inventories/{inventory_id}` via `inventory-update --yes`
- `DELETE /inventories/{inventory_id}` via `inventory-delete --yes`
- `GET /items/{type}/{no}` via `item`
- `GET /items/{type}/{no}/images/{color_id}` via `item-images`
- `GET /items/{type}/{no}/supersets` via `item-supersets`
- `GET /items/{type}/{no}/subsets` via `item-subsets`
- `GET /items/{type}/{no}/price` via `item-price`
- `GET /items/{type}/{no}/colors` via `item-colors`
- `GET /feedback` via `feedback`
- `POST /feedback` via `feedback-create --yes`
- `GET /feedback/{feedback_id}` via `feedback-view`
- `POST /feedback/{feedback_id}/reply` via `feedback-reply --yes`
- `GET /colors`, `GET /colors/{color_id}` via `colors`, `color`
- `GET /categories`, `GET /categories/{category_id}` via `categories`, `category`
- `GET /notifications` via `notifications`
- `GET /coupons`, `GET /coupons/{coupon_id}` via `coupons`, `coupon`
- `POST /coupons`, `PUT /coupons/{coupon_id}`, `DELETE /coupons/{coupon_id}` via guarded coupon commands
- `GET /settings/shipping_methods`, `GET /settings/shipping_methods/{method_id}` via shipping commands
- `GET /members/{username}/ratings` via `member-ratings`
- `GET /members/{username}/my_notes` via `member-notes`
- `POST/PUT/DELETE /members/{username}/my_notes` via guarded member-note commands
- `GET /item_mapping/{type}/{no}` via `item-mapping`
- `GET /item_mapping/{element_id}` via `element-mapping`

Treat order, buyer, address, payment, feedback, coupon, inventory, and private-note data as private. Summarize only what the user needs.

## Known BrickLink endpoint quirks

BrickLink item `type` values are uppercase API enums such as `SET`, `PART`, and `MINIFIG`. Do not pass BrickOwl-style title-case types.

The item mapping endpoints are overloaded:
- Use `item-mapping --type PART --no <part-no> --color-id <color-id>` for `GET /item_mapping/{type}/{no}`. The checked-in OpenAPI restricts `type` to `PART` here.
- Use `element-mapping --element-id <element-id>` for `GET /item_mapping/{element_id}`.

Price guide defaults can hide intent. Set `--guide-type sold|stock`, `--new-or-used N|U`, and `--currency-code` explicitly when the user asks for a price estimate.

Subsets and supersets shape changes with `--break-minifigs` and `--break-subsets`; keep those flags explicit instead of guessing.

## Mutating workflows

Do not run these with `--yes` until the user explicitly confirms the exact action.

### Create inventory

Draft the JSON from current state or user-provided details, then inspect it:

```bash
scripts/bricklink inventory-create --dry-run --json "$INVENTORY_JSON"
```

Confirmation prompt shape:

```text
Confirm BrickLink inventory create: item <type>/<no>, color <color_id>, quantity <qty>, price <unit_price>, condition <new_or_used>. This creates live marketplace inventory.
```

Then:

```bash
scripts/bricklink inventory-create --yes --json "$INVENTORY_JSON"
```

### Update or delete inventory

Read the lot first with `inventory --inventory-id`. Only update fields the user named. Deletion is destructive and needs immediate confirmation naming the inventory ID.

```bash
scripts/bricklink inventory-update --dry-run --inventory-id "$INVENTORY_ID" --json "$PATCH_JSON"
scripts/bricklink inventory-delete --dry-run --inventory-id "$INVENTORY_ID"
```

### Orders, feedback, coupons, and member notes

For order status/payment changes, feedback, coupons, and private member notes, draft the exact JSON and show it before execution. Do not infer tone for feedback or notes; ask the user to approve exact text.

```bash
scripts/bricklink order-status --dry-run --order-id "$ORDER_ID" --json "$ORDER_STATUS_JSON"
scripts/bricklink feedback-reply --dry-run --feedback-id "$FEEDBACK_ID" --json "$REPLY_JSON"
scripts/bricklink coupon-update --dry-run --coupon-id "$COUPON_ID" --json "$COUPON_JSON"
scripts/bricklink member-notes-delete --dry-run --username "$USERNAME"
```

## Live smoke checks

Local, no-network checks:

```bash
python3 -m py_compile scripts/bricklink_cli.py
scripts/bricklink inventory-delete --dry-run --inventory-id 123456
python3 -m unittest discover -s tests -p 'test_*.py'
scripts/validate-skills.sh
git diff --check
```

Read-only smoke check, only when all four `BRICKLINK_API_*` credentials are configured:

```bash
scripts/bricklink colors
```

Summarize only response shape: status, top-level keys, and rough counts. Never paste private account/order/inventory/member-note data or credential values.

## Common pitfalls

1. Treating credentials as consent. They are not. Writes still require explicit user intent.
2. Putting OAuth credentials in query parameters or JSON bodies. BrickLink uses OAuth1 `Authorization` headers.
3. Using BrickOwl item type casing. BrickLink item types are uppercase API enums.
4. Mixing up `item-mapping` and `element-mapping`; the paths look similar but answer opposite questions.
5. Running full set price breakdowns for casual questions. Start with targeted item or set price guide calls unless the user approved fan-out.
6. Guessing item type or color ID. Use `/colors`, `/items/{type}/{no}/colors`, and item mapping endpoints instead of inventing IDs.
7. Mutating the wrong marketplace. If BrickLink and BrickOwl are both configured and the user only says "my store", ask which platform before writing.
8. Posting feedback or member notes from inferred tone. Draft first; let the user approve exact text.
9. Bulk inventory changes without a reviewed ID list. Require exact inventory IDs and payload summaries before touching live listings.

## Verification checklist

- [ ] `BRICKLINK_API_CONSUMER_KEY`, `BRICKLINK_API_CONSUMER_SECRET`, `BRICKLINK_API_TOKEN_VALUE`, and `BRICKLINK_API_TOKEN_SECRET` are referenced only as env vars.
- [ ] Read-only smoke check uses `GET /colors` or another harmless endpoint.
- [ ] Price guide and item lookup examples are read-only.
- [ ] Inventory/order/feedback/coupon/member-note writes require explicit user intent and `--yes`.
- [ ] Dry runs do not require credentials and do not call the network.
- [ ] Destructive deletes require immediate confirmation with exact IDs.
- [ ] Endpoint coverage matches `references/openapi/bricklink.yaml`.
- [ ] Large price-breakdown fan-out asks approval before execution.
