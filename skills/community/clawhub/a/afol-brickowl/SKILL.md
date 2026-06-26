---
name: brickowl
description: Use the BrickOwl API through the included CLI for catalog lookup, inventory, orders, wishlists, and safe marketplace writes.
version: 1.0.0
---

# BrickOwl AFOL skill

Use this skill when the user asks for BrickOwl catalog lookup, BrickOwl store inventory, BrickOwl orders, BrickOwl wishlist creation, or BrickOwl marketplace listing management.

Primary interface: `scripts/brickowl`.

The skill is self-contained for archive distribution and wraps the BrickOwl API directly using checked-in references inside this skill directory:
- OpenAPI reference: `references/openapi/brickowl.yaml`
- Domain guidance: `references/prompts/brickowl-tools.txt`
- CLI source: `scripts/brickowl_cli.py`

Do not scrape vendor docs or invent parameters when the checked-in OpenAPI reference covers the endpoint. If the reference is insufficient, say what is missing.

## Authentication

Required environment variable:

```bash
export BRICKOWL_API_KEY=...
```

Optional override:

```bash
export BRICKOWL_BASE_URL=https://api.brickowl.com/v1
```

Never print, commit, log, or paste the real API key. Commands should reference `$BRICKOWL_API_KEY` only indirectly through the CLI.

BrickOwl auth placement matters:
- GET endpoints send `key` as a query parameter.
- POST endpoints send `key` in the `application/x-www-form-urlencoded` request body.

The CLI handles that split, which is the main reason to use it instead of ad-hoc curl.

## CLI quick reference

Run commands from this skill directory:

```bash
scripts/brickowl --help
scripts/brickowl user
scripts/brickowl id-lookup --id 75192-1 --type Set --id-type set_number
scripts/brickowl catalog-search --query "Millennium Falcon" --type Set --page 1
scripts/brickowl inventory-list --page 1
scripts/brickowl orders --status Pending --page 1
scripts/brickowl order --order-id 12345
```

Mutating commands are guarded. They do nothing unless passed `--yes`; use `--dry-run` first:

```bash
scripts/brickowl inventory-create --dry-run \
  --boid 123456 \
  --quantity 1 \
  --price 850.00 \
  --condition news

scripts/brickowl inventory-update --dry-run \
  --lot-id 12345 \
  --price 599.99

scripts/brickowl inventory-delete --dry-run --lot-id 12345
scripts/brickowl wishlist-create --dry-run --name "Wanted parts" --description "For next build"
scripts/brickowl bulk --dry-run --requests-json '[{"path":"/user"}]'
```

## Safety rules

Read-only by default:
- `user`
- `catalog-search`
- `id-lookup`
- `inventory-list`
- `orders`
- `order`

Mutating operations require explicit user confirmation in the current conversation before execution:
- `inventory-create`
- `inventory-update`
- `inventory-delete`
- `wishlist-create`
- `bulk` whenever any embedded request mutates data

Stored credentials are not permission. Before any mutation, restate the exact action, lot/item identifiers, quantity, price, condition, wishlist name, or bulk request list and wait for explicit confirmation such as "yes, create it" or "confirm update lot 123".

The CLI enforces this mechanically: mutating commands fail unless `--yes` is passed, and `--dry-run` prints the request shape with the API key redacted.

If the user asks to "sell", "list", "update inventory", or "delete lot" without naming a platform and both BrickLink/BrickOwl could apply, ask which marketplace to use before mutating anything.

## Endpoint coverage

- `GET /catalog/search` via `catalog-search`
- `GET /catalog/id_lookup` via `id-lookup`
- `GET /inventory/list` via `inventory-list`
- `POST /inventory/create` via `inventory-create --yes`
- `POST /inventory/update` via `inventory-update --yes`
- inventory deletion through `inventory-delete --yes`, implemented as `POST /inventory/update` with `delete=true`
- `GET /order/list` via `orders`
- `GET /order/view` via `order`
- `POST /wishlist/create_list` via `wishlist-create --yes`
- `GET /user` via `user`
- `POST /bulk` via `bulk --yes`

Treat inventory, order, buyer, address, cost, and personal-note data as private. Summarize only what the user needs.

## Known BrickOwl lookup rule

Use `id-lookup` for known external IDs. Do not abuse fuzzy catalog search as an ID lookup tool.

Good:

```bash
scripts/brickowl id-lookup --id 75192-1 --type Set --id-type set_number
```

Useful `id_type` values from the checked-in spec:
- `item_no`
- `design_id`
- `bl_item_no`
- `set_number`

Use `catalog-search` only when the user gives a fuzzy text query or asks to browse/search by words:

```bash
scripts/brickowl catalog-search --query "Millennium Falcon" --type Set --page 1
```

## Mutating workflows

Do not run these with `--yes` until the user explicitly confirms the exact action.

### Create an inventory lot

Required fields: `boid`, `quantity`, `price`, `condition`. Valid create conditions are lowercase BrickOwl condition IDs: `news`, `newc`, `newi`, `usedc`, `usedi`, `usedn`, `usedg`, `useda`, `other`. Plain `New` is not valid for `inventory-create`.

Confirmation prompt shape:

```text
Confirm BrickOwl inventory create: BOID <boid>, quantity <qty>, price <price>, condition <condition>, optional color_id <color_id>, optional external_id <external_id>.
```

Then:

```bash
scripts/brickowl inventory-create --yes --boid "$BOID" --quantity "$QUANTITY" --price "$PRICE" --condition "$CONDITION"
```

### Update an inventory lot

Use `--lot-id` or `--external-lot-id`, plus only the fields the user asked to change. For quantity, distinguish:
- `--absolute-quantity`: set quantity to this exact value.
- `--relative-quantity`: add/subtract this amount.

Confirmation prompt shape:

```text
Confirm BrickOwl lot update: lot_id <lot_id> / external_lot_id <external_lot_id>; changes: <fields>.
```

Then:

```bash
scripts/brickowl inventory-update --yes --lot-id "$LOT_ID" --price "$PRICE"
```

### Delete an inventory lot

Deletion is destructive and needs especially explicit confirmation naming the lot ID.

```bash
scripts/brickowl inventory-delete --yes --lot-id "$LOT_ID"
```

### Create a wishlist

Confirmation prompt shape:

```text
Confirm BrickOwl wishlist creation: name "<name>", description "<description>".
```

Then:

```bash
scripts/brickowl wishlist-create --yes --name "$WISHLIST_NAME" --description "$WISHLIST_DESCRIPTION"
```

### Bulk requests

Bulk has a lower rate limit: 200 requests/minute. Inspect every embedded request before deciding whether it is read-only or mutating.

If any embedded request is POST to inventory or wishlist endpoints, require explicit confirmation for the whole batch and summarize each write. Do not hide writes inside a bulk payload.

```bash
scripts/brickowl bulk --yes --requests-json "$BULK_REQUESTS_JSON"
```

## BrickOwl limitations and routing

BrickOwl API does not provide marketplace offer data from other sellers. If the user asks for current marketplace prices/offers on BrickOwl, explain that limitation and suggest BrickLink pricing if available, or direct them to BrickOwl.com for manual marketplace browsing.

BrickOwl is appropriate for:
- validating BrickOwl catalog IDs / BOIDs
- managing the authenticated user's own BrickOwl inventory
- viewing the authenticated user's BrickOwl orders
- creating BrickOwl wishlists

It is not appropriate for API-based cross-seller price discovery.

## Verification

Local, no-network checks:

```bash
python3 -m py_compile scripts/brickowl_cli.py
scripts/brickowl inventory-create --dry-run --boid 123 --quantity 1 --price 9.99 --condition news
python3 -m unittest discover -s tests -p 'test_*.py'
scripts/validate-skills.sh
```

Read-only smoke check, only when `BRICKOWL_API_KEY` is configured:

```bash
scripts/brickowl user
```
