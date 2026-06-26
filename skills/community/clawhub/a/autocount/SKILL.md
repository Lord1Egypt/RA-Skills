---
name: AutoCount
description: Create and validate AutoCount business documents through AutoCount Web API. Use when the user wants to create or test sales invoices, purchase invoices, goods received notes, inspect purchase orders, map debtor/creditor/item master data into document payloads, or build AutoCount document automation against a Windows-hosted AutoCount Web API.
---

# AutoCount

Use this skill to create or test AutoCount documents through the AutoCount Web API.

Supported document work in this skill:
- sales invoice
- sales order / delivery order / credit note
- purchase invoice
- goods received note
- purchase order inspection/listing
- master-data lookup for debtors, creditors, items, locations, and currencies

## Workflow

1. Confirm the base URL, API name, and API key.
2. Use the headers:
   - `X-API-NAME: 9999`
   - `X-API-KEY: 9999`
   - `Content-Type: application/json`
3. Prefer `SaveAsDraft: true` unless the user explicitly wants final posting.
4. For transfer chains, the source document must be final (`SaveAsDraft: false`). Draft purchase documents cannot be used as transfer sources.
5. Prefer AutoCount defaults (`<<<Default>>>`) over guessed business values.
6. Do not hardcode tax codes. Use defaults or system-derived values only.
7. After each create call, fetch the created record and report the actual document number.

## Known API pattern

Base URL example:
- `http://your-autocount-host:9999`

Headers example:
```http
X-API-NAME: <your-api-name>
X-API-KEY: <your-api-key>
Content-Type: application/json
```

## Endpoints verified

### Sales
- `POST {{localURL}}/api/SalesOrder/CreateRecord`
- `GET {{localURL}}/api/SalesOrder/GetRecord?docKey=...`
- `POST {{localURL}}/api/DeliveryOrder/CreateRecord`
- `GET {{localURL}}/api/DeliveryOrder/GetRecord?docKey=...`
- `POST {{localURL}}/api/Invoice/CreateRecord`
- `GET {{localURL}}/api/Invoice/GetRecord?docKey=...`
- `POST {{localURL}}/api/CreditNote/CreateRecord`
- `GET {{localURL}}/api/CreditNote/GetRecord?docKey=...`
- `POST {{localURL}}/api/CreditNote/UpdateRecord?docKey=...`
- `POST {{localURL}}/api/CreditNote/CancelRecord?docKey=...`
- `POST {{localURL}}/api/CreditNote/DeleteRecord?docKey=...`

### Purchase
- `POST {{localURL}}/api/PurchaseOrder/CreateRecord`
- `POST {{localURL}}/api/PurchaseOrder/UpdateRecord?docKey=...`
- `POST {{localURL}}/api/PurchaseInvoice/CreateRecord`
- `POST {{localURL}}/api/GoodsReceivedNote/CreateRecord`
- `GET {{localURL}}/api/PurchaseOrder/GetRecord?docKey=...`
- `POST {{localURL}}/api/PurchaseOrder/GetRecordList`
- `GET {{localURL}}/api/GoodsReceivedNote/GetRecord?docKey=...`
- `POST {{localURL}}/api/GoodsReceivedNote/GetRecordList`
- `GET {{localURL}}/api/PurchaseInvoice/GetRecord?docKey=...`

### Master data
- `GET {{localURL}}/api/Debtor/GetRecordList`
- `GET {{localURL}}/api/Creditor/GetRecordList`
- `GET {{localURL}}/api/Item/GetRecordList`
- `GET {{localURL}}/api/Location/GetRecordList`
- `GET {{localURL}}/api/Currency/GetRecordList`

## Core rules

### Defaults

Use AutoCount defaults where supported:
- `DocNo: "<<<Default>>>"`
- `DocNoFormatName: "<<<Default>>>"`
- `DebtorName: "<<<Default>>>"` when not enriching from master data
- `DisplayTerm: "<<<Default>>>"`
- `CurrencyCode: "<<<Default>>>"`
- address/phone/attention fields may also accept `<<<Default>>>`
- `TaxCode: "<<<Default>>>"` is preferred over manually forcing a tax code

### Draft option

```json
"Options": {
  "DocNoFormatName": "<<<Default>>>",
  "SaveAsDraft": true
}
```

### Reporting rule

After a successful create:
1. capture the returned `docKey`
2. call the matching `GetRecord` endpoint
3. report back at least:
   - `DocNo`
   - `DocKey`
   - party code/name
   - total/final total

## Sales invoice pattern

### Minimal stable sales invoice template

```json
{
  "Master": {
    "DocNo": "<<<Default>>>",
    "DocDate": "2026-03-27",
    "DebtorCode": "SS29",
    "DebtorName": "<<<Default>>>",
    "SalesLocation": "HQ",
    "DisplayTerm": "<<<Default>>>",
    "CurrencyCode": "<<<Default>>>"
  },
  "Details": [
    {
      "ItemCode": "00001",
      "UOM": "METER",
      "UserUOM": "<<<Default>>>",
      "Location": "HQ",
      "Description": "<<<Default>>>",
      "Qty": 2,
      "UnitPrice": 22.22,
      "TaxCode": "<<<Default>>>",
      "Classification": "010",
      "OriginCountryCode": "MYS"
    }
  ],
  "Options": {
    "DocNoFormatName": "<<<Default>>>",
    "SaveAsDraft": true
  }
}
```

## Purchase-side pattern

Purchase documents use a similar body shape to sales invoices, but with purchase-side party/location fields.

### Purchase invoice template

```json
{
  "Master": {
    "DocNo": "<<<Default>>>",
    "CreditorCode": "400-S001",
    "CreditorName": "SUPPLIER",
    "PurchaseLocation": "HQ",
    "DocDate": "2026-03-27",
    "Description": "PURCHASE INVOICE",
    "DisplayTerm": "C.O.D.",
    "CurrencyCode": "MYR",
    "CurrencyRate": 1
  },
  "Details": [
    {
      "DeliveryDate": "2026-03-27",
      "ItemCode": "00002",
      "UOM": "SET",
      "UserUOM": "SET",
      "Location": "HQ",
      "Description": "SOFA 沙发",
      "Qty": 10,
      "FOCQty": 0,
      "UnitPrice": 1000,
      "Discount": "",
      "TaxCode": "<<<Default>>>"
    }
  ],
  "Options": {
    "DocNoFormatName": "<<<Default>>>",
    "SaveAsDraft": true
  }
}
```

### Goods received note template

```json
{
  "Master": {
    "DocNo": "<<<Default>>>",
    "SupplierDONo": "AUTO-GRN-20260327-01",
    "CreditorCode": "400-S001",
    "CreditorName": "SUPPLIER",
    "PurchaseLocation": "HQ",
    "DocDate": "2026-03-27",
    "Description": "GOODS RECEIVED NOTE",
    "DisplayTerm": "C.O.D.",
    "CurrencyCode": "MYR",
    "CurrencyRate": 1
  },
  "Details": [
    {
      "DeliveryDate": "2026-03-27",
      "ItemCode": "00002",
      "UOM": "SET",
      "UserUOM": "SET",
      "Location": "HQ",
      "Description": "SOFA 沙发",
      "Qty": 10,
      "FOCQty": 0,
      "UnitPrice": 1000,
      "Discount": "",
      "TaxCode": "<<<Default>>>"
    }
  ],
  "Options": {
    "DocNoFormatName": "<<<Default>>>",
    "SaveAsDraft": true
  }
}
```

## SO → DO → Invoice guidance

Use this when the user wants sales document progression.

1. Create or inspect a final Sales Order first.
2. For transfer source documents, ensure the source is final, not draft.
3. For transfer creates, use transfer-only payloads:
   - set `Details: []`
   - populate `TransferDetails[]`
   - do not include a matching manual detail row
4. SO → DO transfer:
   - `POST /api/DeliveryOrder/CreateRecord`
   - `TransferDetails[].DocType = "SO"`
5. DO → Invoice transfer:
   - `POST /api/Invoice/CreateRecord`
   - `TransferDetails[].DocType = "DO"`
6. Use `SalesLocation` on invoice payloads and sales-side master payloads where appropriate.
7. Set `DocNo: "<<<Default>>>"` and `DocNoFormatName: "<<<Default>>>"`.
8. Use `TaxCode: "<<<Default>>>"` unless the system proves a specific value.
9. Fetch created records and report the final document numbers.

### Proven live sales chain

A full sales chain was live-tested successfully:
- Sales Order → Delivery Order using `DocType: "SO"`
- Delivery Order → Invoice using `DocType: "DO"`

## PO → GRN → PI guidance

Use this when the user wants purchase document progression.

1. List purchase orders with:
   - `POST /api/PurchaseOrder/GetRecordList` and body `{}`
2. Inspect a specific PO with:
   - `GET /api/PurchaseOrder/GetRecord?docKey=...`
3. For transfer source documents, ensure the source is final, not draft.
4. For transfer creates, use transfer-only payloads:
   - set `Details: []`
   - populate `TransferDetails[]`
   - do not include a matching manual detail row, or AutoCount may create an extra unlinked line
5. PO → GRN transfer:
   - `POST /api/GoodsReceivedNote/CreateRecord`
   - `TransferDetails[].DocType = "PO"`
6. GRN → PI transfer:
   - `POST /api/PurchaseInvoice/CreateRecord`
   - `TransferDetails[].DocType = "GR"`
7. Direct PO → PI transfer is also supported on a fresh final PO:
   - `TransferDetails[].DocType = "PO"`
8. Add GRN-specific `SupplierDONo` when creating GRNs.
9. Set `DocNo: "<<<Default>>>"` and `DocNoFormatName: "<<<Default>>>"`.
10. Use `TaxCode: "<<<Default>>>"` unless the system proves a specific value.
11. Fetch created records and report the final document numbers.

### Transfer payload rule

Use this pattern for transfer documents:

```json
{
  "Master": {
    "DocNo": "<<<Default>>>",
    "DocDate": "2026-04-09",
    "CreditorCode": "400-S001",
    "CreditorName": "<<<Default>>>",
    "PurchaseLocation": "HQ",
    "DisplayTerm": "<<<Default>>>",
    "CurrencyCode": "<<<Default>>>",
    "CurrencyRate": "<<<Default>>>"
  },
  "Details": [],
  "TransferDetails": [
    {
      "DocType": "PO",
      "DocNo": "PO-000038",
      "ItemCode": "00002",
      "UOM": "SET",
      "TransferQty": 5,
      "TransferFOCQty": 0
    }
  ],
  "Options": {
    "DocNoFormatName": "<<<Default>>>",
    "SaveAsDraft": false
  }
}
```

Swap `DocType` as follows:
- `PO` for PO → GRN
- `PO` for PO → PI
- `GR` for GRN → PI
- `SO` for SO → DO
- `DO` for DO → Invoice

### Proven live chain

A full purchase chain was live-tested successfully:
- Purchase Order → GRN using `DocType: "PO"`
- GRN → Purchase Invoice using `DocType: "GR"`

### Balance and over-transfer notes

AutoCount tracks transfer quantity at table level even when the normal PO API does not expose it.
Observed relevant DB fields include:
- `PODTL.Qty`
- `PODTL.TransferedQty`
- `PODTL.Transferable`
- `PIDTL.FromDocType`
- `PIDTL.FromDocNo`

Working balance formula:
- remaining transferable qty = `Qty - TransferedQty`

Important: the standard `PurchaseOrder/GetRecord` API response did not expose `TransferedQty`, so automation should not assume the API will prevent over-transfer. Validate quantities before transfer when possible.

## Update / cancel / delete safety

Treat these as real mutations.

1. Prefer testing update/cancel/delete only on fresh test documents unless the user clearly requests mutation on a real document.
2. `UpdateRecord` expects a clean create-style payload more often than a raw `GetRecord` echo.
3. `CancelRecord` and `DeleteRecord` are destructive.
4. After cancel/delete, a later `GetRecord` may return record-not-found.
5. Always report the exact affected `DocNo` and `DocKey` back to the user.

### Confirmed live mutation routes

For Credit Note, the following worked in live testing:
- `POST /api/CreditNote/UpdateRecord?docKey=...`
- `POST /api/CreditNote/CancelRecord?docKey=...`
- `POST /api/CreditNote/DeleteRecord?docKey=...`

Observed behavior:
- update changed quantity and total successfully
- cancel returned `true`
- after cancel/delete testing, `GetRecord` returned record-not-found for the test document

## Enrichment guidance

Before document creation, optionally fetch master data and copy display fields into the payload.

### Sales enrichment
- `DebtorName`
- `InvAddr1..4`
- `Phone1`
- `Attention`
- `DisplayTerm`
- `CurrencyCode`

### Purchase enrichment
- `CreditorName`
- supplier-related address/contact fields if available
- `DisplayTerm`
- `CurrencyCode`

### Item enrichment
- `Description`
- valid `UOM`
- location-aware stock hints

This makes the final document more complete in the AutoCount UI.

## Known findings from testing

- AutoCount Web API was reachable on port `9999` over HTTP in the tested environment.
- Root URL returned `404`, which is normal for the service.
- Authentication uses headers, not curl basic auth:
  - `X-API-NAME`
  - `X-API-KEY`
- Sales order create/get worked.
- Delivery order create/get worked.
- Sales invoice create/get worked repeatedly.
- Credit note create/get worked.
- Credit note update worked.
- Credit note cancel worked.
- Credit note delete route worked and the test document became non-retrievable afterward.
- Purchase invoice create worked.
- GRN create worked.
- Purchase order create worked.
- Purchase order update worked when using a clean create-style payload against `UpdateRecord?docKey=...`.
- PO list requires `POST {}` instead of GET.
- PO get worked with valid doc keys.
- Updating a draft PO with `SaveAsDraft: false` did not reliably convert it into a final transferable PO in UI testing; creating a fresh final PO was reliable.
- Transfer source docs must be final, not draft.
- For transfer documents, `Details: []` plus `TransferDetails[]` worked; mixing `Details[]` with `TransferDetails[]` created an extra unlinked manual line.
- `TransferDetails[].DocType` values confirmed in live testing:
  - `PO` for PO → GRN
  - `PO` for PO → PI
  - `GR` for GRN → PI
- `GRN` as a purchase invoice transfer doc type failed with `Invalid transfer document.`
- A full live chain succeeded: PO → GRN → PI.
- A full live chain succeeded: SO → DO → Invoice.
- Lean payloads can create documents, but UI-visible debtor/item display fields may remain blank unless explicitly enriched.
- Item `00001` worked repeatedly in sales invoices with:
  - description: `FABRIC`
  - UOM: `METER`
  - origin country: `MYS`
- Item list response does not necessarily expose tax code fields.
- Do not manually force tax codes unless explicitly instructed or proven from system data.
- Using `TaxCode: "<<<Default>>>"` worked and is preferred.
- GRN create initially failed when `DocNo` was missing; adding `DocNo: "<<<Default>>>"` fixed it.
- Sales invoice route is `/api/Invoice/CreateRecord`, not `/api/SalesInvoice/CreateRecord`.
- Sales transfer doc types confirmed in live testing:
  - `SO` for SO → DO
  - `DO` for DO → Invoice

## References

Read `references/test-notes.md` for the observed behavior and payload patterns discovered during live testing.
