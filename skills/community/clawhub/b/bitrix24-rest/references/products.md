# Products and Product Rows

Use this file for the product catalog, product items, and attaching products to CRM entities (deals, quotes, invoices).

Scope: `crm`, `catalog`

## Product Catalog

- `crm.product.list` — list products (supports `order`, `filter`, `select`)
- `crm.product.add` — add product to CRM catalog
- `crm.product.get` — get product by ID
- `crm.product.update` — update product
- `crm.product.delete` — delete product
- `crm.product.fields` — field schema

Key fields: `ID`, `NAME`, `PRICE`, `CURRENCY_ID`, `CATALOG_ID`, `SECTION_ID`, `ACTIVE`, `MEASURE`, `DESCRIPTION`.

## Product Sections

- `crm.productsection.list` — list product sections (categories)
- `crm.productsection.add` — add section
- `crm.productsection.get` — get section
- `crm.productsection.update` — update section
- `crm.productsection.delete` — delete section

## Product Rows on CRM Entities

Product rows attach catalog products to deals, quotes, invoices, and smart processes.

- `crm.item.productrow.list` — list product rows (filter by `ownerId`, `ownerType`)
- `crm.item.productrow.get` — get one product row by ID
- `crm.item.productrow.set` — set product rows on entity (replaces all existing rows!)
- `crm.item.productrow.delete` — delete a product row
- `crm.item.productrow.getAvailableForPayment` — get rows available for payment

Owner type short codes: `L` = lead, `D` = deal, `Q` = quote, `SI` = smart invoice, dynamic types use `T{entityTypeId}`.

### Product row fields

- `productId` — ID from catalog (optional, can use `productName` alone)
- `productName` — product name (auto-filled from catalog if `productId` given)
- `price` — price per unit including discounts and taxes
- `quantity` — quantity (default 1)
- `discountTypeId` — 1 = absolute, 2 = percentage
- `discountRate` — discount in %
- `discountSum` — discount in absolute value
- `taxRate` — tax rate in %
- `taxIncluded` — `Y`/`N`
- `measureCode` — unit of measure code
- `sort` — sort order

## Common Use Cases

### List all products

```bash
python3 scripts/bitrix24_call.py crm.product.list \
  --param 'select[]=ID' \
  --param 'select[]=NAME' \
  --param 'select[]=PRICE' \
  --param 'select[]=CURRENCY_ID' \
  --param 'order[NAME]=ASC' \
  --json
```

### Add a product to catalog

```bash
python3 scripts/bitrix24_call.py crm.product.add \
  --param 'fields[NAME]=Widget Pro' \
  --param 'fields[PRICE]=1500' \
  --param 'fields[CURRENCY_ID]=RUB' \
  --param 'fields[ACTIVE]=Y' \
  --json
```

### Get product rows of a deal

```bash
python3 scripts/bitrix24_call.py crm.item.productrow.list \
  --param 'filter[ownerId]=123' \
  --param 'filter[ownerType]=D' \
  --json
```

### Set product rows on a deal

This replaces all existing product rows:

```bash
python3 scripts/bitrix24_call.py crm.item.productrow.set \
  --param 'ownerType=D' \
  --param 'ownerId=123' \
  --param 'productRows[0][productId]=456' \
  --param 'productRows[0][price]=1500' \
  --param 'productRows[0][quantity]=2' \
  --param 'productRows[1][productName]=Custom Service' \
  --param 'productRows[1][price]=5000' \
  --param 'productRows[1][quantity]=1' \
  --json
```

## Working Rules

- `crm.item.productrow.set` overwrites all existing rows — always include all desired rows.
- `crm.product.*` uses UPPER_CASE field names.
- `crm.item.productrow.*` uses camelCase field names.
- Filter prefix operators work on `crm.product.list`: `>=PRICE`, `%NAME`.
- `CATALOG_ID` filter is useful when multiple catalogs exist.

## Good MCP Queries

- `crm product list add fields`
- `crm item productrow set list`
- `crm productsection`
- `catalog product`
