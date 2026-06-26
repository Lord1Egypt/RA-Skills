# Smart Processes and Funnels

Use this file for smart processes (custom CRM types), funnels/categories, stages, and stage history.

Scope: `crm`

## Entity Type IDs

Standard types:

- `1` — lead
- `2` — deal
- `3` — contact
- `4` — company
- `5` — old invoice (deprecated)
- `7` — quote
- `31` — new invoice (smart invoice)
- `128+` — custom smart processes

Discover custom types with `crm.type.list`.

## Smart Process Types

- `crm.type.list` — list all smart process types (filter by `title`, `entityTypeId`, `isCategoriesEnabled`, etc.)
- `crm.type.get` — get one type by `id`
- `crm.type.add` — create a new smart process type
- `crm.type.update` — update a smart process type
- `crm.type.delete` — delete a smart process type

## Items (Universal API)

`crm.item.*` works for deals, leads, contacts, companies, quotes, invoices, and all custom smart processes. The `entityTypeId` parameter is always required.

- `crm.item.list` — list items (requires `entityTypeId`, supports `select`, `filter`, `order`)
- `crm.item.get` — get one item by `id` and `entityTypeId`
- `crm.item.add` — create item (requires `entityTypeId` and `fields`)
- `crm.item.update` — update item
- `crm.item.delete` — delete item
- `crm.item.fields` — get field schema for an entity type

Filter operators are prefixes on the key: `>=dateCreate`, `!stageId`, `%title`.

## Funnels (Categories)

- `crm.category.list` — list funnels for a type (requires `entityTypeId`)
- `crm.category.get` — get one funnel
- `crm.category.add` — create funnel
- `crm.category.update` — update funnel
- `crm.category.delete` — delete funnel
- `crm.category.fields` — field schema

## Stages and Statuses

- `crm.status.list` — list statuses/stages (filter by `ENTITY_ID`)
- `crm.stagehistory.list` — stage change history (requires `entityTypeId`)

Stage history `TYPE_ID` values:

- `1` — create
- `2` — intermediate stage change
- `3` — final stage
- `5` — funnel change

`STAGE_SEMANTIC_ID`: `P` = in progress, `S` = success, `F` = fail.

## Common Use Cases

### List all smart process types

```bash
python3 scripts/bitrix24_call.py crm.type.list --json
```

### List items of a smart process

```bash
python3 scripts/bitrix24_call.py crm.item.list \
  --param 'entityTypeId=128' \
  --param 'select[]=id' \
  --param 'select[]=title' \
  --param 'select[]=stageId' \
  --param 'select[]=assignedById' \
  --json
```

### Create an item in a smart process

```bash
python3 scripts/bitrix24_call.py crm.item.add \
  --param 'entityTypeId=128' \
  --param 'fields[title]=New item' \
  --param 'fields[assignedById]=1' \
  --json
```

### Get field schema for a type

```bash
python3 scripts/bitrix24_call.py crm.item.fields \
  --param 'entityTypeId=128' \
  --json
```

### List funnels (categories) for deals

```bash
python3 scripts/bitrix24_call.py crm.category.list \
  --param 'entityTypeId=2' \
  --json
```

### Get stage history

```bash
python3 scripts/bitrix24_call.py crm.stagehistory.list \
  --param 'entityTypeId=2' \
  --param 'filter[>=CREATED_TIME]=2026-01-01T00:00:00' \
  --json
```

## Working Rules

- `entityTypeId` is mandatory for all `crm.item.*` and `crm.category.*` methods.
- Use `crm.type.list` to discover `entityTypeId` values for custom processes.
- Fields use camelCase in `crm.item.*` (e.g. `stageId`, `assignedById`, `categoryId`).
- For deal-specific methods (`crm.deal.*`), fields use UPPER_CASE (`STAGE_ID`, `CATEGORY_ID`).
- Always call `crm.item.fields` before writing custom field values.

## Good MCP Queries

- `crm type list add smart process`
- `crm item list add fields`
- `crm category list funnels`
- `crm stagehistory`
- `crm status list`
