# SanMar skill — agent examples

Realistic prompts the SanMar skill handles, and the deterministic CLI calls to
make for each. Every tool is invoked the same way:

```bash
echo '<json-args>' | python3 scripts/sanmar.py <action>
```

Each call prints a single JSON object on stdout, or `{"error": {...}}` with a
non-zero exit code on failure. Credentials come from the `SANMAR_*` environment
variables, or can be passed inline in the stdin JSON (`customer_number`,
`username`, `password`, `environment`, `ftp_password`).

---

## 1. Catalog discovery by style

**Prompt:** "What colors and sizes does style PC55 come in?"

```bash
echo '{"style": "PC55"}' | python3 scripts/sanmar.py search-products
```

**Output:**

```json
{
  "style": "PC55",
  "title": "Port & Company Core Blend Tee",
  "weight": 5.0,
  "image": "https://cdn.sanmar.com/.../PC55.jpg",
  "colors": ["Athletic Heather", "Black", "Jet Black", "Navy"],
  "sizes": ["S", "M", "L", "XL", "2XL", "3XL", "4XL"],
  "variants": [
    {"style": "PC55", "color": "Black", "size": "L",
     "unique_key": "...", "inventory_key": "...", "size_index": "3",
     "image": "...", "piece_price": 7.52}
  ],
  "surface": "sanmar_webservice",
  "operation": "getProductInfoByStyleColorSize"
}
```

---

## 2. Live inventory check

**Prompt:** "Is PC55 in Black, size L, in stock right now?"

```bash
echo '{"style": "PC55", "color": "Black", "size": "L"}' \
  | python3 scripts/sanmar.py check-inventory
```

**Output:**

```json
{
  "style": "PC55",
  "color": "Black",
  "size": "L",
  "warehouse_quantities": [120, 88, 0, 240, 60],
  "total_available": 240,
  "surface": "sanmar_webservice",
  "operation": "getInventoryQtyForStyleColorSize"
}
```

`total_available` is the maximum single-warehouse quantity, matching SanMar
shipping semantics: an order ships from one warehouse, so ability-to-ship is
bounded by the largest warehouse quantity, not the sum.

---

## 3. Pricing for a planned order

**Prompt:** "What's our myPrice on PC55 Black size L and PC55 Navy size XL?"

```bash
echo '{"lines": [
  {"style": "PC55", "color": "Black", "size": "L"},
  {"style": "PC55", "color": "Navy", "size": "XL"}
]}' | python3 scripts/sanmar.py get-pricing
```

**Output:**

```json
{
  "items": [
    {"style": "PC55", "color": "Black", "size": "L",
     "inventory_key": "12345", "size_index": "3",
     "piece_price": 7.52, "dozen_price": 7.02, "case_price": 6.52,
     "my_price": 6.75, "sale_piece_price": null,
     "sale_dozen_price": null, "sale_case_price": null},
    {"style": "PC55", "color": "Navy", "size": "XL",
     "inventory_key": "12346", "size_index": "4",
     "piece_price": 7.52, "dozen_price": 7.02, "case_price": 6.52,
     "my_price": 6.75, "sale_piece_price": null,
     "sale_dozen_price": null, "sale_case_price": null}
  ],
  "surface": "sanmar_webservice",
  "operation": "getPricing"
}
```

Keep `inventory_key` and `size_index` per line — they are required when calling
`create-purchase-order`.

---

## 4. Pre-submit cart validation

**Prompt:** "Validate this draft PO before I send it."

```bash
echo '{"purchase_order": {
  "po_number": "PO-1042",
  "ship_to": {
    "name": "BaconCo Receiving",
    "address1": "123 Print Way",
    "city": "Memphis", "state": "TN", "zip": "38103",
    "ship_method": "UPS", "email": "purchasing@example.com"
  },
  "lines": [
    {"style": "PC55", "color": "Black", "size": "L", "quantity": 24},
    {"style": "PC55", "color": "Navy", "size": "XL", "quantity": 12}
  ]
}}' | python3 scripts/sanmar.py validate-cart
```

**Output (happy path):**

```json
{"ok": true, "errored_lines": [], "warnings": [],
 "surface": "sanmar_webservice", "operation": "getPreSubmitInfo"}
```

**Output (inventory shortfall):**

```json
{
  "ok": false,
  "errored_lines": [
    {"style": "PC55", "color": "Navy", "size": "XL",
     "message": "Insufficient inventory in any warehouse"}
  ],
  "warnings": [],
  "surface": "sanmar_webservice",
  "operation": "getPreSubmitInfo"
}
```

Do not call `create-purchase-order` until `ok` is true.

---

## 5. Submit a purchase order (high risk)

**Prompt:** "Send PO-1042 to SanMar."

First: pull `inventory_key` / `size_index` per line via `get-pricing` and merge
them onto each line, call `validate-cart` and confirm `ok: true`, then confirm
with the operator that a live submit is intended.

**Dry-run preview (default, `confirm` omitted or false):**

```bash
echo '{"purchase_order": { ...draft... }, "confirm": false}' \
  | python3 scripts/sanmar.py create-purchase-order
```

```json
{
  "status": "dry_run",
  "po_number": "PO-1042",
  "sanmar_reference": null,
  "raw_payload": "<?xml version='1.0' encoding='UTF-8'?>\n<soapenv:Envelope ...>",
  "raw_response": null,
  "surface": "sanmar_webservice",
  "operation": "submitPO"
}
```

**Live submit:**

```bash
echo '{"purchase_order": { ...draft... }, "confirm": true}' \
  | python3 scripts/sanmar.py create-purchase-order
```

```json
{
  "status": "submitted",
  "po_number": "PO-1042",
  "sanmar_reference": "PO-1042",
  "raw_payload": "...",
  "raw_response": "<soap:Envelope ...>",
  "surface": "sanmar_webservice",
  "operation": "submitPO"
}
```

If SanMar returns `errorOccurred=true`, the call exits non-zero with an
`api_error`:

```json
{"error": {"type": "api_error", "surface": "sanmar_webservice",
           "operation": "submitPO", "message": "<verbatim SanMar message>",
           "retryable": false}}
```

---

## 6. Order status / tracking after submission

**Prompt:** "What's the status of PO-1042?"

```bash
echo '{"po_number": "PO-1042"}' | python3 scripts/sanmar.py check-order-status
```

```json
{
  "po_number": "PO-1042",
  "sanmar_order_number": "9876543",
  "shipment_count": 2,
  "status": "shipped",
  "surface": "sanmar_promostandards",
  "operation": "GetOrderShipmentNotificationRequest"
}
```

**Prompt:** "Get tracking numbers for PO-1042."

```bash
echo '{"po_number": "PO-1042"}' | python3 scripts/sanmar.py get-tracking
```

```json
{
  "po_number": "PO-1042",
  "shipments": [
    {"tracking_number": "1Z999AA10123456784", "carrier": "ups"},
    {"tracking_number": "9622012345678901234567", "carrier": "fedex"}
  ],
  "surface": "sanmar_promostandards",
  "operation": "GetOrderShipmentNotificationRequest"
}
```

---

## 7. Cancellation request — currently unsupported

**Prompt:** "Cancel PO-1042."

```bash
echo '{"po_number": "PO-1042", "reason": "duplicate", "confirm": true}' \
  | python3 scripts/sanmar.py cancel-order
```

```json
{
  "status": "not_implemented",
  "po_number": "PO-1042",
  "message": "SanMar's published web services... Cancel via SanMar customer service.",
  "surface": "sanmar_webservice",
  "operation": "cancelPO"
}
```

Pass this back to the user verbatim and recommend opening a SanMar
customer-service ticket.

---

## 8. Parse a PDF purchase order uploaded by the user

**Prompt:** "Here's the PO PDF — can you place it for us?"

Parse the PDF, present the extracted values for approval, then submit. Never
auto-submit without user confirmation.

```bash
echo '{"pdf_path": "/uploads/po-1042.pdf"}' \
  | python3 scripts/sanmar.py parse-po-pdf
```

```json
{
  "po_number": "PO-1042",
  "order_date": "04/28/2026",
  "ship_method": "UPS Ground",
  "ship_to": {
    "name": "BaconCo Receiving",
    "address1": "123 Print Way",
    "address2": "",
    "city": "Memphis",
    "state": "TN",
    "zip": "38103",
    "email": "purchasing@example.com"
  },
  "lines": [
    {"style": "PC55", "color": "Black", "size": "L",
     "quantity": 24, "unit_price": 7.52, "description": "Port & Co Tee Black"},
    {"style": "PC55", "color": "Navy", "size": "XL",
     "quantity": 12, "unit_price": 7.52, "description": "Port & Co Tee Navy"}
  ],
  "warnings": [],
  "draft_for_submit": {
    "po_number": "PO-1042",
    "ship_to": {"name": "BaconCo Receiving", "address1": "123 Print Way",
                "city": "Memphis", "state": "TN", "zip": "38103",
                "email": "purchasing@example.com", "ship_method": "UPS Ground"},
    "lines": [
      {"style": "PC55", "color": "Black", "size": "L", "quantity": 24},
      {"style": "PC55", "color": "Navy", "size": "XL", "quantity": 12}
    ]
  },
  "surface": "sanmar_pdf_parser",
  "operation": "parse_po_pdf"
}
```

**Agent flow:**

1. Show the parsed PO back to the user (especially `warnings`).
2. After approval, feed `draft_for_submit`'s lines through `get-pricing` to
   enrich each with `inventory_key` / `size_index`.
3. Call `validate-cart` and confirm `ok: true`.
4. Call `create-purchase-order` with `purchase_order` set to the enriched draft
   and `confirm: true`.

If `warnings` flags missing fields, ask the user to fill them in rather than
guessing.

---

## 9. Resolve a marketing color to its SanMar mainframe color

**Prompt:** "Inventory check for PC55 in Athletic Heather size L."

Try the marketing name directly. If SanMar rejects it or returns nothing,
`check-inventory` automatically falls back to the SDL CSV on SanMar's SFTP
server and retries — no explicit lookup needed.

```bash
echo '{"style": "PC55", "color": "Athletic Heather", "size": "L"}' \
  | python3 scripts/sanmar.py check-inventory
```

**Behind the scenes:**

1. Initial SOAP call with `color="Athletic Heather"` errors out.
2. Tool downloads `SanMarPDD/SanMar_SDL_N.csv` from `ftp.sanmar.com:2200` (or
   uses the local 24h cache).
3. Finds the row with `STYLE#=PC55`, `COLOR_NAME=Athletic Heather`, `SIZE=L`
   and reads `SANMAR_MAINFRAME_COLOR=ATHHTHR`.
4. Retries the inventory call with `color="ATHHTHR"` and returns the normal
   `InventoryResult` with `color` set to the resolved code.

**Explicit lookup** (to get the code without an inventory/pricing call):

```bash
echo '{"style": "PC55", "color": "Athletic Heather", "size": "L"}' \
  | python3 scripts/sanmar.py lookup-mainframe-color
```

```json
{
  "status": "matched",
  "style": "PC55",
  "requested_color": "Athletic Heather",
  "size": "L",
  "matches": [
    {"style": "PC55", "requested_color": "Athletic Heather", "size": "L",
     "mainframe_color": "ATHHTHR", "color_name": "Athletic Heather",
     "inventory_key": "12345", "size_index": "3", "unique_key": "12345_3"}
  ],
  "source_file": "SanMarPDD/SanMar_SDL_N.csv",
  "as_of": "2026-04-30T06:02:11+00:00",
  "surface": "sanmar_ftp",
  "operation": "lookup_mainframe_color"
}
```

If `status` is `ambiguous`, ask the user to pick between the listed `matches`.
If `not_found`, surface that verbatim — do not guess.

---

## 10. Missing credentials → ask the user

When no credentials are configured, a tool exits with `config_error` (exit 2):

```bash
echo '{"style": "PC55", "color": "Black", "size": "L"}' \
  | python3 scripts/sanmar.py check-inventory
```

```json
{"error": {"type": "config_error",
           "message": "SanMar web-service credentials were not provided. Ask the user for customer_number, username, password and supply them either via the SANMAR_CUSTOMER_NUMBER / SANMAR_USERNAME / SANMAR_PASSWORD environment variables or as credential fields in the tool's stdin JSON."}}
```

Treat this as a signal to ask the user for the missing fields. Once you have
them, supply them one of two ways:

**Inline in each call's JSON:**

```bash
echo '{"style": "PC55", "color": "Athletic Heather", "size": "L",
       "customer_number": "123456", "username": "api@x.com", "password": "…",
       "ftp_password": "…"}' \
  | python3 scripts/sanmar.py check-inventory
```

**Or via the environment (set once for the session):**

```bash
export SANMAR_CUSTOMER_NUMBER=123456
export SANMAR_USERNAME=api@x.com
export SANMAR_PASSWORD=…
export SANMAR_FTP_PASSWORD=…          # only for mainframe-color resolution
echo '{"style": "PC55", "color": "Black", "size": "L"}' \
  | python3 scripts/sanmar.py check-inventory
```

The FTP password is **different** from the web-services password. Never guess
values, and never fall back to another vendor's credentials.

---

## 11. Per-warehouse inventory (PromoStandards v2)

**Prompt:** "Which warehouses have K420 Black small in stock?"

```bash
echo '{"style": "K420"}' | python3 scripts/sanmar.py get-inventory-levels
```

**Output (abridged):**

```json
{
  "style": "K420",
  "parts": [
    {"part_id": "92032", "color": "Black", "size": "S", "total_available": 1045,
     "warehouses": [
       {"warehouse_id": "1", "warehouse_name": "Seattle", "quantity": 0},
       {"warehouse_id": "2", "warehouse_name": "Cincinnati", "quantity": 167},
       {"warehouse_id": "3", "warehouse_name": "Dallas", "quantity": 179}
     ]}
  ],
  "surface": "sanmar_promostandards", "operation": "getInventoryLevels"
}
```

Pass `part_ids` (SanMar unique keys) to limit the response to specific variants.
For a bulk snapshot of a whole style across warehouses without a live call, use
`get-inventory-feed` with `{"style": "K420"}` (parses `sanmar_dip.txt`).

---

## 12. Retrieve invoices for a PO (accounts-payable)

**Prompt:** "Pull the SanMar invoice for PO P13189 so we can match and bill it."

```bash
echo '{"po_number": "P13189"}' | python3 scripts/sanmar.py get-invoices
```

**Output (abridged):**

```json
{
  "query_type": "purchase_order", "query_value": "P13189", "count": 1,
  "invoices": [
    {
      "invoice_number": "12345678", "po_number": "P13189",
      "sales_order_number": "163291890", "invoice_date": "2024-06-18",
      "due_date": "2024-07-18", "terms": "NET 30", "total_amount": 192.72,
      "sub_total": 192.72, "sales_tax": 0.0, "shipping_handling": 0.0,
      "lines": [{"style": "2000", "color": "Red", "size": "M", "quantity": 16,
                 "unit_price": 1.84, "amount": 29.44, "unique_key": "263633"}],
      "common": {
        "source": "sanmar", "po_number": "P13189", "invoice_number": "12345678",
        "invoice_date": "2024-06-18", "due_date": "2024-07-18",
        "is_credit": false, "has_lines": true, "total": 192.72,
        "charges": {"merchandise": 192.72, "freight": 0.0,
                    "freight_allowance": 0.0, "sales_tax": 0.0, "discount": null},
        "lines": [{"item": "2000", "size": "M", "color": "Red", "unit": "EA",
                   "qty_shipped": 16, "net_price": 1.84, "extension": 29.44}]
      }
    }
  ]
}
```

Hand `invoices[].common` to `drivethru-payable-matching` — it's the same
normalized shape `sportsinc-sportslink` emits, so the PO match runs unchanged.
Other queries: `{"invoice_number": "12345678"}`, `{"order_date": "2024-06-18"}`,
`{"start_date": "2024-06-01", "end_date": "2024-06-30"}`, `{"unpaid": true}`.
An empty `count` for a PO means it hasn't been invoiced yet (SanMar invoices
after 9 p.m. PT once an order ships — pull the day after).

---

## 13. Parse the FTP Daily Invoice file (batch payables)

**Prompt:** "Import yesterday's SanMar invoices from the FTP drop."

```bash
# Newest *Invoice_Details* file from the outbound folder over SFTP:
echo '{}' | python3 scripts/sanmar.py parse-invoice-file
# …or a specific local/remote file, or the EDI-810 variant:
echo '{"path": "/data/123456_Invoice_Details-06-18-24.txt"}' \
  | python3 scripts/sanmar.py parse-invoice-file
echo '{"remote_path": "/Outbound/338469-810.x12", "edi": true}' \
  | python3 scripts/sanmar.py parse-invoice-file
```

Output matches `get-invoices` exactly (native invoices + a `common` block each),
so the downstream payables flow is identical regardless of source.

---

## 14. Package tracking + shipment-status file

**Prompt:** "Where's PO P13137 — tracking and which boxes shipped?"

```bash
echo '{"po_number": "P13137"}' | python3 scripts/sanmar.py get-tracking
```

```json
{
  "po_number": "P13137", "complete": true,
  "shipments": [
    {"tracking_number": "1Z999...", "carrier": "ups", "shipment_method": "Ground",
     "ship_date": "2024-01-12T22:44:42-08:00", "sales_order_number": "163260908",
     "ship_from_city": "Irving", "ship_from_state": "TX",
     "ship_to_city": "Jacksonville", "ship_to_state": "FL",
     "items": [{"style": "PC55P", "part_id": "834732", "quantity": 1}]}
  ]
}
```

Query instead by `{"sales_order_number": "163260908"}` or, for a whole day,
`{"shipment_date": "2024-01-12T00:00:00Z"}` (7-day max). For tracking **plus
per-line costs** from the nightly ASN file, use `get-shipment-status`:

```bash
echo '{"po_number": "P13137"}' | python3 scripts/sanmar.py get-shipment-status
```
