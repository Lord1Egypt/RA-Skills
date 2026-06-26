# Quotes and Invoices

Use this file for commercial proposals (quotes), new smart invoices, and legacy invoices.

Scope: `crm`

## Quotes

- `crm.quote.add` — create a quote
- `crm.quote.list` — list quotes (supports `order`, `filter`, `select`)
- `crm.quote.get` — get a quote by ID
- `crm.quote.update` — update a quote
- `crm.quote.delete` — delete a quote
- `crm.quote.fields` — field schema
- `crm.quote.productrows.get` — get product rows of a quote
- `crm.quote.productrows.set` — set product rows on a quote

Key fields: `TITLE`, `STATUS_ID`, `OPPORTUNITY`, `CURRENCY_ID`, `COMPANY_ID`, `CONTACT_ID`, `DEAL_ID`, `ASSIGNED_BY_ID`, `BEGINDATE`, `CLOSEDATE`, `COMMENTS`, `OPENED`.

Status values: `DRAFT`, `SENT`, `APPROVED`, `DECLINED`, etc.

## Smart Invoices (New)

New invoices use the universal `crm.item.*` API with `entityTypeId=31`.

- `crm.item.list` with `entityTypeId=31` — list invoices
- `crm.item.add` with `entityTypeId=31` — create invoice
- `crm.item.update` with `entityTypeId=31` — update invoice
- `crm.item.delete` with `entityTypeId=31` — delete invoice
- `crm.item.fields` with `entityTypeId=31` — field schema

## Legacy Invoices (Deprecated)

`crm.invoice.*` methods are deprecated. Use `crm.item.*` with `entityTypeId=31` for new invoices.

## Common Use Cases

### Create a quote

```bash
python3 scripts/bitrix24_call.py crm.quote.add \
  --param 'fields[TITLE]=Quote for services' \
  --param 'fields[STATUS_ID]=DRAFT' \
  --param 'fields[CURRENCY_ID]=RUB' \
  --param 'fields[OPPORTUNITY]=50000' \
  --param 'fields[COMPANY_ID]=1' \
  --param 'fields[ASSIGNED_BY_ID]=1' \
  --json
```

### List quotes

```bash
python3 scripts/bitrix24_call.py crm.quote.list \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=STATUS_ID' \
  --param 'select[]=OPPORTUNITY' \
  --param 'order[ID]=DESC' \
  --json
```

### Get quote product rows

```bash
python3 scripts/bitrix24_call.py crm.quote.productrows.get \
  --param 'id=42' \
  --json
```

### Create a new smart invoice

```bash
python3 scripts/bitrix24_call.py crm.item.add \
  --param 'entityTypeId=31' \
  --param 'fields[title]=Invoice for order' \
  --param 'fields[currencyId]=RUB' \
  --param 'fields[opportunity]=15000' \
  --param 'fields[companyId]=1' \
  --json
```

### List smart invoices

```bash
python3 scripts/bitrix24_call.py crm.item.list \
  --param 'entityTypeId=31' \
  --param 'select[]=id' \
  --param 'select[]=title' \
  --param 'select[]=stageId' \
  --param 'select[]=opportunity' \
  --json
```

## Working Rules

- `crm.quote.*` uses UPPER_CASE field names.
- `crm.item.*` with `entityTypeId=31` uses camelCase field names.
- For new invoices, prefer `crm.item.*` over deprecated `crm.invoice.*`.
- Quote product rows: use `crm.quote.productrows.set` (not `crm.item.productrow.set`).
- Invoice product rows: use `crm.item.productrow.set` with `ownerType=SI`.

## Good MCP Queries

- `crm quote add list fields productrows`
- `crm item invoice entityTypeId 31`
- `crm invoice add list`
