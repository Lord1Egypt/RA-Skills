# SanMar SOAP Web Services API

Source basis: `SanMarWebServicesIntegrationGuide-v16.10.pdf`.

This page is the operational reference for SanMar SOAP calls used by the SME.

## Service families

SanMar documentation lists these major SOAP surfaces:

- Product Information
- Pricing
- Inventory
- PromoStandards Inventory (v1.2.1)
- Order acknowledgement / confirmation
- Invoicing
- Purchase ordering (see dedicated PO guide)

## Core WSDL endpoints (production)

- `https://ws.sanmar.com:8080/SanMarWebService/SanMarProductInfoServicePort?wsdl`
- `https://ws.sanmar.com:8080/SanMarWebService/SanMarWebServicePort?wsdl`
- `https://ws.sanmar.com:8080/SanMarWebService/SanMarPricingServicePort?wsdl`
- `https://ws.sanmar.com:8080/SanMarWebService/SanMarNotificationServicePort?WSDL`
- `https://ws.sanmar.com:8080/SanMarWebService/InvoicePort?wsdl`
- `https://ws.sanmar.com:8080/promostandards/InventoryServiceBinding?wsdl`

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
