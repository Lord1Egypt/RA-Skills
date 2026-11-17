# SanMar SOAP Web Services API

Source basis: `SanMarWebServicesIntegrationGuide-v24.1.pdf` (supersedes the
older v16.10 the rest of this page was drafted from).

This page is the operational reference for SanMar SOAP calls used by the skill.

## Service families

SanMar exposes both proprietary "Standard" ports and PromoStandards services:

- Product Information (Standard) + PromoStandards Product Data v2.0.0
- Pricing (Standard `getPricing`, myPrice) + PromoStandards Pricing & Config
- Inventory (Standard `getInventoryQtyForStyleColorSize`) + **PromoStandards
  Inventory v2.0.0** (`getInventoryLevels` — named per-warehouse)
- Purchase ordering — Standard `getPreSubmitInfo`/`submitPO` + PromoStandards
  `sendPO` (see the dedicated PO guide / `purchase_orders.md`)
- Order Shipment Notification v1.0.0 (tracking) + Order Status v2.0.0
- **Invoicing** — Standard `InvoicePort` (see `invoicing.md`)

## Core WSDL endpoints (production; host `ws.sanmar.com:8080`)

| Service | Path | Used by |
| --- | --- | --- |
| Product info | `/SanMarWebService/SanMarProductInfoServicePort` | `search-products` |
| Pricing (myPrice) | `/SanMarWebService/SanMarPricingServicePort` | `get-pricing` |
| Inventory (legacy) | `/SanMarWebService/SanMarWebServicePort` | `check-inventory` |
| Inventory v2 | `/promostandards/InventoryServiceBinding` | `get-inventory-levels` |
| PO submit | `/SanMarWebService/SanMarPOServicePort` | `validate-cart`, `create-purchase-order` |
| Order shipment (tracking) | `/promostandards/OrderShipmentNotificationServiceBinding` | `get-tracking`, `check-order-status` |
| Invoicing | `/SanMarWebService/InvoicePort` | `get-invoices` |

`SANMAR_ENV=development` swaps PO submit and invoicing to the
`test-ws.sanmar.com:8080` host; the read services are production-only.

> **Auth field names differ by service.** The Standard product/pricing/
> inventory/PO ports use `sanMarCustomerNumber` / `sanMarUserName` /
> `sanMarUserPassword`. **InvoicePort** uses `CustomerNo` / `UserName` /
> `Password`. PromoStandards services (inventory v2, tracking) use
> `wsVersion` / `id` (= username) / `password` and **no customer number**.
> The client injects the right fields per service.

## Product information operations

The web services guide demonstrates these product-info methods:

- `getProductBulkInfo`
- `getProductDeltaInfo`
- `getProductInfoByBrand`
- `getProductInfoByCategory`
- `getProductInfoByStyleColorSize`

### Practical method selection

- Use `getProductInfoByStyleColorSize` when caller has concrete identifiers and needs immediate structured detail.
- Use `getProductInfoByBrand` or `...ByCategory` for bounded discovery lists.
- Use `getProductDeltaInfo` for incremental-sync behavior.
- Use `getProductBulkInfo` for full or large baseline extraction (often paired with CSV/FTP artifacts).

## Canonical request keys

Common request fields across examples:

- `sanMarCustomerNumber`
- `style`
- `color`
- `size`

Caller guidance:

- `style` should be normalized (trim/uppercase when appropriate).
- `color`/`size` are frequently optional depending on method but dramatically improve precision.

## Canonical response entities

The guide’s XML examples repeatedly expose:

- identity fields (`style`, `color`, `size`, `sizeIndex`, inventory/unique identifiers)
- imagery URLs (`colorProductImage`, thumbnail/swatch/square images)
- pricing blocks (`piecePrice`, `dozenPrice`, `casePrice`, and sale variants)
- descriptive merchandising fields (status, descriptions, category/brand attributes)

Return these as stable JSON objects to task agents; do not forward raw SOAP envelopes unless explicitly requested.

## Data quality and interpretation notes

- Some records can be present but operationally limited by product status.
- GTIN/UPC-like values may be absent for some products.
- Price semantics differ by quantity tier and can be customer-specific.
- Delta results can include partial sets intended for sync jobs.

## Recommended normalized JSON shape

```json
{
  "items": [
    {
      "style": "PC55T",
      "color": "Jade Green",
      "size": "4XLT",
      "size_index": "3",
      "inventory_key": "...",
      "unique_key": "...",
      "status": "ACTIVE",
      "price": {
        "piece": 7.52,
        "dozen": 7.02,
        "case": 6.52,
        "currency": "USD"
      },
      "images": {
        "product": "https://...",
        "thumbnail": "https://...",
        "swatch": "https://..."
      }
    }
  ],
  "source": "sanmar_web_services",
  "operation": "getProductInfoByStyleColorSize"
}
```

## Failure modes to handle explicitly

- IP not allowlisted / port 8080 blocked (timeouts or connection failure)
- auth/account mismatch
- invalid/missing customer number
- method argument mismatch (bad style/color/size combinations)

When possible, map SOAP faults to clear machine-readable error classes while preserving original upstream message.
