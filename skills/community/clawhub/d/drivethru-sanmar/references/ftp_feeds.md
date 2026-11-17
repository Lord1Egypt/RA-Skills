# SanMar FTP Integration and File Feeds

Source basis:

- `SanMar-FTP-Integration-Guide-v23.1.pdf`
- `SanMar-FTP-Integration-Guide-v18 (4).pdf`

This page covers SanMar file-based integration patterns, folder behavior, and major feed categories.

## Integration model

SanMar FTP integration is used for:

- bulk and incremental product data distribution
- inventory and pricing feed delivery
- invoice and order-related integration files

SanMar onboarding notes indicate FTP credentials are provisioned separately from web-service credentials.

## Major feed categories

## 1) Product library / catalog exports

The guide references SanMar data library naming and active product export files (including variants such as active/closeout data). Fields include style/color/size identities, descriptions, imagery references, and multi-tier pricing.

Common key fields seen repeatedly:

- `inventory_key`
- `size_index`
- `unique_key`
- `style` / mill style
- catalog/display color fields
- `piece`, `dozen`, `case` pricing fields

## 2) Daily inventory and sales pricing

Daily files provide quantity/availability and pricing deltas. The guide also references customer-specific pricing (`my_price`) feed behavior and smaller daily delta files.

SME behavior:

- expose feed date/time in output
- prefer unique-key joins to merge with product master
- keep staleness messaging explicit (daily batch timing)

**Parsed by `get-inventory-feed`** — `sanmar_dip.txt` (pipe-delimited,
inventory **by warehouse**, refreshed hourly, under `/SanMarPDD/`). Columns:

| # | Column | # | Column |
| --- | --- | --- | --- |
| 1 | Inventory_Key | 10 | Dozens_Price (=piece) |
| 2 | Size_Index | 11 | Case_Price |
| 3 | Catalog_No (style) | 12 | Case_Size |
| 4 | Catalog_Color | 13–15 | sale prices |
| 5 | Size | 16–17 | sale start/end |
| 6 | Whse_No (1=Sea,2=Cin,3=Dal,4=Reno,5=Robb,6=Jax,7=Minn,12=Phx,31=Rich) | 18 | Unique_key |
| 7 | Quantity (≤1500/whse) | 19 | Discontinued_code (S/M) |
| 8 | Piece_Weight | | |
| 9 | Piece_Price | | |

Always pass `style` to filter — the full feed is very large. For real-time
per-warehouse levels prefer the SOAP `get-inventory-levels` (PromoStandards v2).
`SanMar_EPDD.csv` (comma-delimited) is the bulk-inventory companion (QTY = all
warehouses combined) and shares the SDL columns plus `QTY`.

## 3) Invoicing & shipment outputs

By-request outbound files (exported to the account's FTP outbound folder):

- **Daily Invoice** — fixed-width `.txt`, Excel, and EDI-810 variants. Parsed by
  `parse-invoice-file`. Full layout in [`invoicing.md`](invoicing.md).
- **Daily Shipment Status (ASN)** — tab-delimited `*Status.txt` with tracking +
  per-line costs. Parsed by `get-shipment-status`. Layout in
  [`shipment_status.md`](shipment_status.md).
- **Special/Incentive pricing** — `sanmar_dp.csv` (lowest `my_price`, full
  catalog), `sanmar_dpc.csv` (daily delta: `unique_key` + `my_price` only),
  `sanmar_dpIncentive.csv` (program pricing). The `common` join key is
  `unique_key` (= `inventory_key` + `size_index`).

The invoice/status/pricing files are account-specific in name and folder — pass
an exact `remote_path`, or let the tool fetch the newest match from
`SANMAR_FTP_OUTBOUND_DIR`. Never invent filenames when a caller expects a
deterministic PO association.

## File and folder handling behaviors

The guides describe strict file naming and folder conventions for order-related integration flows, including resubmission handling when duplicate names are detected.

Operational guardrails for this SME:

- never invent filenames when caller expects deterministic PO associations
- preserve exact upstream filename, drop-folder, and timestamp metadata
- signal duplicate-file/replay risks explicitly

## Feed cadence and releases

SanMar documents regular daily drops plus broader seasonal/annual product release cycles. Treat feed completeness as batch-based, not transactional real-time.

## Join strategy across feeds

Recommended deterministic join precedence:

1. `unique_key`
2. (`inventory_key`, `size_index`)
3. (`style`, `color`, `size`) as fallback

When keys disagree between sources, prefer the most recent dated feed and include a warning.

## Suggested normalized output envelope

```json
{
  "feed": "daily_inventory_pricing",
  "as_of": "2026-04-28T12:00:00Z",
  "items": [
    {
      "unique_key": "123456_03",
      "style": "PC55",
      "color": "BLACK",
      "size": "L",
      "inventory": 120,
      "price": {
        "piece": 7.52,
        "dozen": 7.02,
        "case": 6.52,
        "my_price": 6.75
      }
    }
  ],
  "source": "sanmar_ftp"
}
```

## Common pitfalls to detect

- using stale full extract instead of latest daily delta
- missing/incorrect key join between product and inventory files
- misunderstanding tier prices as a single universal price
- assuming all products have GTINs or all images are populated
