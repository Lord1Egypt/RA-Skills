# SanMar invoicing

Two grounded sources of the **same** invoice data — pick by need:

| Tool | Source | When |
| --- | --- | --- |
| `get-invoices` | SanMar Standard **InvoicePort** SOAP | On-demand: one PO / invoice / date, or all unpaid. |
| `parse-invoice-file` | FTP **Daily Invoice** file (fixed-width or EDI-810) | Batch: everything invoiced the prior day. |

SanMar: *"The Daily Invoice File … will share the same data as our invoicing
calls."* Both tools emit the identical output shape (native header/lines + a
normalized `common` block), so a payables workflow treats them interchangeably.

## Timing (both sources)

SanMar invoices **once per day after 9 p.m. Pacific**, and only after an order
**ships**. Pull invoice data the day *after* the order date. If you pull by PO
and the order isn't invoiced yet, `get-invoices` returns an empty result (not an
error). One-to-two calls per PO per day is plenty; do not poll.

---

## `get-invoices` — Standard InvoicePort

- PRODUCTION: `https://ws.sanmar.com:8080/SanMarWebService/InvoicePort?wsdl`
- TEST (`SANMAR_ENV=development`): `https://test-ws.sanmar.com:8080/SanMarWebService/InvoicePort?wsdl`
- Namespace: `http://webservice.integration.sanmar.com/` (prefix `web`).
- **Auth (the "invoice exception"):** the credential element names are
  `<web:CustomerNo>`, `<web:UserName>`, `<web:Password>` — NOT the
  `sanMarCustomerNumber` / `sanMarUserName` / `sanMarUserPassword` used by the
  other standard ports. Same values, different element names. The skill builds
  the right envelope from the standard credentials.

### Query → operation mapping (what the tool sends)

| stdin field | Operation | Selector element(s) |
| --- | --- | --- |
| `po_number` | `GetInvoicesByPurchaseOrderNo` | `<web:PurchaseOrderNo>` |
| `invoice_number` | `GetInvoiceByInvoiceNo` | `<web:InvoiceNo>` |
| `order_date` | `GetInvoicesByOrderDate` | `<web:Date>` (yyyy-mm-dd) |
| `start_date`+`end_date` | `GetInvoicesByInvoiceDateRange` | `<web:StartDate>`,`<web:EndDate>` (≤ 3 months) |
| `unpaid: true` | `GetUnpaidInvoices` | — |

`headers_only: true` swaps to the `…Header…` variant
(`GetInvoicesHeaderByPurchaseOrderNo` / `…ByInvoiceDateRange` / `…ByOrderDate` /
`GetUnpaidInvoicesHeader`) for `purchase_order`, `invoice_date_range`,
`order_date`, and `unpaid`. `invoice_number` has no header-only form.

### Request (example — by PO)

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:web="http://webservice.integration.sanmar.com/">
  <soapenv:Header/>
  <soapenv:Body>
    <web:GetInvoicesByPurchaseOrderNo>
      <web:CustomerNo>123456</web:CustomerNo>
      <web:UserName>you@example.com</web:UserName>
      <web:Password>********</web:Password>
      <web:PurchaseOrderNo>4520838A</web:PurchaseOrderNo>
    </web:GetInvoicesByPurchaseOrderNo>
  </soapenv:Body>
</soapenv:Envelope>
```

### Response shape

`<Invoices>` wraps one or more `<Invoice>` (a single `<Invoice>` root for
`GetInvoiceByInvoiceNo`). Each has a `<Header>` and repeating `<LineItem>`:

- **Header:** `InvoiceNo`, `SalesOrderNumber`, `InvoiceDate`, `InvoiceStatus`
  (`Unpaid`/`Paid`), `CustomerNo`, `SoldTo`/`ShipTo`/`RemitTo` (`Name` +
  `Address`), `PurchaseOrderNo`, `OrderDate`, `DueDate`, `ShipVia`, `FOB`,
  `Terms`, `TotalCases`, `TotalWeight`, `SubTotal`, `SalesTax`,
  `ShippingHandlingCharges`, `TotalAmount`, `Miscellaneous` (`FreightSavings`,
  `TrackingIDs`).
- **LineItem:** `StyleNo`, `StyleColor`, `StyleDescription`, `StyleSize`,
  `Quantity`, `UnitPrice`, `Amount`, `UniqueKey`.

Error messages (returned in a fault): `Invalid request` (missing param),
`Data not found` (unknown/uninvoiced PO or invoice — surfaced as an **empty**
result), and date-range/length validation messages. Auth failures raise.

---

## Normalized `common` shape (both tools)

Every invoice in the tool output carries a `common` block — the cross-vendor
invoice shape consumed by `drivethru-payable-matching` (identical to what
`sportsinc-sportslink` emits):

```json
{
  "source": "sanmar",
  "po_number": "4520838A",          // ← PurchaseOrderNo (the PO match key)
  "invoice_number": "12345678",     // ← InvoiceNo
  "invoice_date": "2014-08-01",
  "due_date": "2014-08-31",
  "supplier": "SANMAR CORP",        // ← RemitTo/Name
  "sales_order_number": "123456789",
  "is_credit": false,               // ← TotalAmount < 0 → credit memo
  "has_lines": true,
  "total": 192.72,                  // ← TotalAmount
  "charges": {
    "merchandise": 192.72,          // ← SubTotal
    "freight": 0.0,                 // ← ShippingHandlingCharges
    "freight_allowance": 0.0,       // ← Miscellaneous/FreightSavings
    "sales_tax": 0.0,               // ← SalesTax
    "discount": null
  },
  "lines": [
    { "item": "2000", "description": "100% ULTRA CTN T RED", "size": "M",
      "color": "Red", "unit": "EA", "qty_shipped": 16,
      "net_price": 1.84, "extension": 29.44, "unique_key": "263633" }
  ]
}
```

A negative `total` → `is_credit: true`. Route credit memos to a human / vendor
credit; never create them as a payable.

---

## `parse-invoice-file` — FTP files

### Daily Invoice — fixed-width `.txt` (default)

`123456_Invoice_Details-MM-DD-YY.txt`, one **line item per row**, grouped into
invoices by invoice number. Exported nightly after 12 p.m. PT. Character
positions (1-indexed, from the FTP Integration Guide v23.1):

| Cols | Field | Cols | Field |
| --- | --- | --- | --- |
| 1–10 | Account Number | 180–189 | Style No |
| 11–38 | Account Name | 190–203 | Color |
| 39–47 | Invoice number | 204–253 | Description |
| 48–57 | Invoice Date | 254–257 | Size |
| 58–72 | Customer PO Number | 258–263 | Pieces |
| 73–82 | Order Date | 264–273 | Price |
| 83–92 | Due Date | 274–283 | Amount |
| 93–132 | Ship To Name | 284–293 | Sales Tax |
| 133–135 | Ship To State | 294–303 | Shipping Handling |
| 136–145 | Ship Date | 304–313 | Total |
| 146–157 | Freight Method | 314–323 | Invoice Total |
| 158–169 | Terms | 324–332 | Sales Order # |
| 170–179 | Unique Key | | |

The parser groups rows by invoice number, sums line `Amount`s into `sub_total`,
and takes the header totals (tax, shipping, `Invoice Total`) from the row.

> The guide's *example values* are wider than several documented field widths;
> the parser follows the **character ranges** above (which are internally
> self-consistent). If a real file ever misaligns, adjust `_INVOICE_FIELDS` in
> `scripts/feed_parsers.py` — or just use `get-invoices` / EDI-810, which are
> position-independent.

### EDI-810 — `edi: true`

X12 004010 invoice file. Best-effort: each `ST…SE` transaction becomes one
invoice. Extracted: invoice number/date (`BIG`), line items (`IT1` → qty, unit
price, unique key, description → style/color/size), grand total (`TDS`, implied
2 decimals), tax (`TXI`), shipping (`SAC` with a "Shipping" description). The
customer PO comes from `REF*PO`/`REF*CO` or `BIG04` when present. Negative
quantities/totals are credit lines/memos.

A Daily Invoice **Excel** file also exists (emailed, not on SFTP); it carries
the same columns as the fixed-width file. If you have one, extract its rows and
feed them as `text` or use `get-invoices` instead.
