# CHAMPRO API reference

Source: [CHAMPRO Development Tools](https://devtools.champrosports.com/#devtools).
Where observed behaviour differs from the published document, both are recorded
and the observation wins.

## Hosts and authentication

| Host | Purpose | Credential |
| --- | --- | --- |
| `https://api.champrosports.com` | REST API | `APICustomerKey` (GUID) |
| `https://cb.champrosports.com` | Custom Builder API | `CustomerKey` (embed key) for reads, `APICustomerKey` for ordering |

Both keys are generated on
[Account & Contact Info](https://champrosports.com/AccountAndContactInfo), and
they are not interchangeable.

`PlaceOrder` — on either host — additionally requires the calling IP to be on
the account's **API Allowed IP Addresses** list (error 15). Reads do not.

### Everything returns HTTP 200

Captured live 2026-08-21 with an invalid key. Every one of these is a 200:

| Endpoint | Failure body |
| --- | --- |
| `ProductInfo` | `{"ProductMaster":"JSBJ8","MOQ":0,"MOQCustom":0,"ProductSKUs":null,"AvailableLeadTimes":null,"Error":"Customer validation error…"}` |
| `OrderStatus` | `{"OrderNumber":0,"PO":null,…,"Error":"Customer validation error…"}` |
| `Inventory` | `{"SessionID":null,"Inventory":null,"ResponseMessage":"Customer validation error…","ErrorMessages":null}` |
| `PlaceOrder` | `{"SessionID":null,…,"RequestErrors":[{"Response":"E4.1: Customer validation error…"}],"Orders":null}` |
| CB `GetOrderInfo` | `[]` — no error channel whatsoever |

`ProductInfo` returning `MOQ: 0, MOQCustom: 0` on an auth failure is the
nastiest of these: those are legal values, so a client reading them without
checking `Error` concludes the product has no minimum.

Real HTTP errors do occur, and mean something different: CB `GetFile` 404s on
an unknown session, and any GET under `/api/OrderSandBox/` 405s.

## Sandbox

| | URL |
| --- | --- |
| Production | `POST /api/Order/PlaceOrder` |
| Sandbox | `POST /api/OrderSandBox/PlaceOrder` |

There is **no `IsSandBox` field on the REST API** — that flag exists only on
the Custom Builder's own PlaceOrder. Sandbox orders older than 30 days are
purged.

Observed: `/api/OrderSandBox/<anything>` is a catch-all routing every path to
the sandbox place-order (`/api/OrderSandBox/Inventory` places an order), while
`/api/Order/<bogus>` returns a proper 404. Only `PlaceOrder` has a sandbox;
`ProductInfo`, `Inventory` and `OrderStatus` do not.

Both hosts accept `application/json` and `application/x-www-form-urlencoded`.
This skill sends JSON throughout.

---

## `GET /api/Order/ProductInfo`

Query: `ProductMaster`, `APICustomerKey`.

| Field | Type | Notes |
| --- | --- | --- |
| `ProductMaster` | String | echoed |
| `MOQ` | Integer | minimum order quantity for **STOCK**; 0 = no minimum |
| `MOQCustom` | Integer | minimum for **CUSTOM**; 0 = no minimum |
| `ProductSKUs[].SKU` | String | the orderable SKU |
| `ProductSKUs[].Configuration` | String | e.g. `GIRLS`, `YOUTH`, `WOMENS` |
| `ProductSKUs[].Fabric` | String | e.g. `ACTIVE CLOTH`, `TEK-KNIT WPK395` |
| `ProductSKUs[].Color` | String | usually `""` — colour lives in the SKU suffix |
| `ProductSKUs[].Size` | String | |
| `AvailableLeadTimes[].LeadTimeName` | String | the exact value a CUSTOM order's `LeadTime` must match |
| `AvailableLeadTimes[].LeadTime` | String | days, as a string |
| `AvailableLeadTimes[].LeadTimeCharge` | String | surcharge, as a string |
| `Error` | String | **check this before anything else** |

**MOQ is an increment, not a floor.** The document is explicit: "the product
must be ordered in quantity increments of the MOQ". With `MOQCustom: 12`, 18
is rejected (error 25) though it exceeds 12. The increment applies to the
product-master total across the order's lines.

A SKU's product master cannot be derived by slicing — `JSBJ8` yields both
`JSBJ8GACL` and `JSBJ8WWP14XL`. Callers name the master.

## `POST /api/Order/Inventory`

```json
{"APICustomerKey": "…", "Orders": [{"OrderItems": [{"SKU": "BBS44ABS"}]}]}
```

The nesting is real: a list of orders, each with a list of items. It reads as
inventory for a *set of SKUs* regardless of how they are grouped.

| Field | Type | Notes |
| --- | --- | --- |
| `SessionID` | String | opaque request id |
| `Inventory[].ItemID` | String | base product id |
| `Inventory[].SKU` | String | |
| `Inventory[].MORE_EXPECTED_ON` | String | US-format restock date, or `""` |
| `Inventory[].Warehouses[].WarehouseLocation` | String | `IL`, `CA`, `DR` |
| `Inventory[].Warehouses[].Quantity` | Integer | |
| `ResponseMessage` | String | doubles as a status line — only an error when it reads like one |
| `ErrorMessages[]` | List of String | per-SKU, e.g. `E3.1: <SKU> - SKU does not Exist.` |

A SKU that fails appears in `ErrorMessages` and is simply **absent** from
`Inventory` — indistinguishable from one with no stock unless you diff against
what you asked for. `check-inventory` returns `missing` for exactly this.

## `POST /api/Order/PlaceOrder`

Shared envelope:

```json
{"APICustomerKey": "…", "Autowarehouse": "YES", "Orders": [ … ]}
```

`Autowarehouse` is `"YES"` or absent, and applies to STOCK orders.

### Order fields

| Field | STOCK | CUSTOM | Notes |
| --- | --- | --- | --- |
| `PO` | required | required | your order number; must be unique |
| `OrderType` | `STOCK` | `CUSTOM` | one order is entirely one type (error 07) |
| `ShipToFirstName` / `ShipToLastName` | required | required | |
| `Address` / `Address2` | required / optional | required / optional | |
| `City` / `StateCode` / `ZIPCode` / `CountryCode` | required | required | `USA`; the doc notes `US`/`USA`/`United States` are accepted, any case |
| `Phone` | required | required | |
| `IsResidential` | required | required | documented Boolean; examples send `1`/`0`, responses echo `true`/`false` |
| `ShippingMethod` | **required** | — | from the published list |
| `ShippingCustomerAccount` | required for Collect / BillThirdParty | — | the payer's carrier account |
| `LeadTime` | — | **required** | a `LeadTimeName` from ProductInfo |
| `ProofFileURL` | — | **required** | public PDF/JPG/JPEG/PNG, fetched server-side |
| `TeamColor` | — | optional | |
| `OrderItems[].SKU` | required | required | |
| `OrderItems[].Quantity` | required | required | MOQ / MOQCustom increments apply |
| `OrderItems[].Warehouse` | required unless Autowarehouse | — | `IL`, `CA`, `DR` |
| `OrderItems[].TeamName` / `PlayerName` / `PlayerNumber` | — | optional | per-garment roster |

### Response

| Field | Notes |
| --- | --- |
| `SessionID` | CHAMPRO's id for the request |
| `RequestType` | `ORDER` / `SUBMIT`, or `PRESUBMIT` for sandbox |
| `Autowarehouse` | echoed |
| `RequestErrors[].Response` | request-level failure — nothing was created |
| `Orders[]` | the submitted orders, echoed, plus: |
| `Orders[].CostTotal` | total for the processed products |
| `Orders[].OrderErrors[].Response` | order-level, e.g. `E2.8.3: <SKU> - Not enough Inventory.` |
| `Orders[].SubOrders[].SubOrderID` | **the order number in CHAMPRO's system** — the only proof an order exists |
| `Orders[].SubOrders[].Warehouse` | the fulfilling warehouse |
| `Orders[].SubOrders[].SubOrderItems[]` | with per-item `Cost` |
| `Orders[].SubOrders[].SubOrderErrors[]` | suborder-level |

**Partial success is normal.** The published example returns two
`OrderErrors` for insufficient inventory *and* two suborders that were created.
Errors present does not mean nothing happened; only `SubOrders` tells you what
exists. There is no cancel endpoint and no idempotency key.

## `GET /api/Order/OrderStatus`

Query: `OrderNumber` (a **SubOrderID**, not a PO), `APICustomerKey`.

| Field | Notes |
| --- | --- |
| `OrderNumber` | echoed; `0` on failure |
| `PO` | your order number |
| `SalesID` | CHAMPRO's sales order, e.g. `SO-2000712`. The field table spells it `SALESID`; the example spells it `SalesID`. Accept both. |
| `Lines[].TrackingNumber` | carrier tracking number |
| `Lines[].ShippingCarrier` | e.g. `FedEx` |
| `Lines[].ShippingService` | e.g. `FedEx, Ground` |
| `Lines[].SKUs[]` | `{SKU, Quantity}` — what is inside that package |
| `Status` | e.g. `Invoiced` |
| `Error` | |

A `Lines` entry is a *package*, so a split shipment produces several. Since one
order can produce several suborders, following an order means querying every
`SubOrderID` it returned.

---

## Error codes

Two numbering schemes, and they are not the same table.

**Custom Builder `MessageCode`** — two digits, returned as a field. Full table
with per-code remedies: `echo '{"code":"25"}' | python3 scripts/champro.py explain-error`.

The account-level ones, where no change to the order payload will help: 04, 05,
09, 10, 15, 16, 20, 23.

**REST dotted codes** — prefixes embedded in the message text, not a field:

| Family | Meaning |
| --- | --- |
| `E2.x` | order processing — a line or order was rejected during placement |
| `E3.x` | catalog/SKU lookup — `E3.1: <SKU> - SKU does not Exist.` |
| `E4.x` | authentication — `E4.1: Customer validation error.` |

## Shipping methods

Forty published values, twenty of which carry a billing type. Any method ending
`COLLECT` or `THIRD PARTY` bills someone other than your CHAMPRO account and
requires `ShippingCustomerAccount`.

The list mixes two spellings — `UPS GROUND` and `FEDEX_2_DAY` — so send the
catalog's exact value. `list-shipping-methods` returns it;
`validate-order` rewrites a near-miss to the canonical spelling and says so.

`FEDEX_FREIGHT_ECONOMY`, `FEDEX_FREIGHT_PRIORITY` and `CUSTOM CO` are LTL
(freight) loads. The published table renders them with a trailing footnote
marker (`FEDEX_FREIGHT_ECONOMY3`); the digit is the footnote, not part of the
name.

## Warehouses

| Code | Location |
| --- | --- |
| `IL` | Illinois |
| `CA` | California |
| `DR` | Dominican Republic |
