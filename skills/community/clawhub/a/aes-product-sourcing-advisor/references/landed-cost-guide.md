# Landed Cost Calculator Guide

## What Is Landed Cost?

Landed cost is the total cost of a product delivered to your warehouse or fulfillment center. It includes every expense from the factory floor to your shelf: unit price, packaging, freight, insurance, duties, taxes, and handling fees. Comparing suppliers on FOB price alone is the most common sourcing mistake — two suppliers with a $0.50 FOB price difference can end up with nearly identical landed costs after duties and freight.

## Landed Cost Formula

```
Landed Cost = Unit Price (FOB/FCA)
            + Packaging & Labeling
            + Inland Freight (factory to port)
            + Port/Terminal Handling
            + International Freight (ocean or air)
            + Cargo Insurance
            + Customs Duties & Tariffs
            + Customs Brokerage Fees
            + Last-Mile Delivery (port to warehouse)
            + Defect/Return Allowance
```

## Component-by-Component Breakdown

### 1. Unit Price (FOB/FCA)
The price quoted by the supplier for the product delivered to the port of origin (FOB) or their facility (FCA). Always confirm what is included: Does the quote include packaging? Inner boxes? Master carton?

**Tip:** Request quotes at 3+ volume tiers (MOQ, 2x MOQ, 5x MOQ). Price drops of 5-15% are common at higher volumes.

### 2. Packaging & Labeling
Costs for individual product packaging (poly bags, boxes, inserts), master carton packaging, and any required labeling (FBA labels, CE marks, country of origin stickers). Some suppliers include basic packaging in their FOB price; custom packaging is always extra.

**Typical costs:**
- Poly bag: $0.02-0.05/unit
- Custom printed box: $0.15-0.80/unit
- Insert cards: $0.03-0.10/unit
- Master carton: $0.30-1.00/carton (divide by units per carton)

### 3. Inland Freight
Transportation from the factory to the port of export. In China, this ranges from negligible (factory near port) to significant (inland provinces like Sichuan to Shenzhen).

**Typical costs:**
- Same province as port: $0.01-0.05/unit
- Cross-province (e.g., Zhejiang to Shanghai): $0.05-0.15/unit
- Inland to coast (e.g., Chengdu to Shenzhen): $0.15-0.40/unit

### 4. Port/Terminal Handling
Charges at the origin port for container handling, documentation, and loading. Usually quoted per container or per CBM.

**Typical costs:** $0.02-0.10/unit (varies by shipment size)

### 5. International Freight

#### Ocean Freight (most common for ecommerce)
Charged per CBM (cubic meter) for LCL (Less than Container Load) or per container for FCL (Full Container Load).

**Typical rates (2024-2025 ranges):**
- LCL China to US West Coast: $40-80/CBM
- LCL China to US East Coast: $60-100/CBM
- LCL China to EU (Hamburg): $50-90/CBM
- 20ft FCL China to US West Coast: $2,000-4,500
- 40ft FCL China to US West Coast: $3,500-7,000

**Transit times:**
- China to US West Coast: 14-20 days
- China to US East Coast: 25-35 days
- China to EU: 28-38 days
- Vietnam to US West Coast: 18-25 days

#### Air Freight (for urgent/high-value/lightweight items)
Charged per kg with a volumetric weight calculation (L x W x H / 6000).

**Typical rates:**
- China to US: $4-8/kg
- China to EU: $3-7/kg

**When to use air:** Product value > $15/unit, time-sensitive launch, lightweight items where per-unit air cost < 10% of product value.

### 6. Cargo Insurance
Covers loss or damage during international transit. Standard marine cargo insurance costs 0.3-0.5% of the declared shipment value (CIF).

**Formula:** Insurance = CIF Value × 0.003 to 0.005

### 7. Customs Duties & Tariffs

#### United States
- Find your product's HTS code at hts.usitc.gov
- Standard duty rates range from 0% to 25%+
- Section 301 tariffs add 7.5-25% on many Chinese goods
- De minimis threshold: $800 (shipments under this value are duty-free)

#### European Union
- Find your product's CN code
- Standard duty rates vary by product category
- Anti-dumping duties may apply to specific product categories
- VAT (19-27% depending on country) is due at import

**Formula:** Duty = (FOB Price + Freight + Insurance) × Duty Rate

### 8. Customs Brokerage
Fee paid to a licensed customs broker to handle import documentation and clearance.

**Typical costs:**
- US: $100-250 per entry (divide by units in shipment)
- EU: €75-200 per entry
- Per-unit impact depends on shipment size

### 9. Last-Mile Delivery
Transportation from the destination port to your warehouse or fulfillment center.

**Typical costs:**
- Port to local warehouse (within 50 miles): $0.05-0.15/unit
- Port to Amazon FBA warehouse: $0.10-0.30/unit (includes drayage + delivery appointment)
- Cross-country delivery (e.g., LA port to East Coast warehouse): $0.20-0.60/unit

### 10. Defect/Return Allowance
Build in expected cost of defective units based on the supplier's defect rate history or industry averages.

**Formula:** Defect Cost = Unit Landed Cost × Expected Defect Rate

**Typical defect rates:**
- Excellent supplier (established relationship): 0.5-1.5%
- Good supplier (verified factory): 1.5-3%
- New/unverified supplier: 3-8%

## Worked Example

**Product:** Silicone phone case, sourced from Shenzhen, China → US (Amazon FBA, California warehouse)

| Component | Calculation | Cost/Unit |
|---|---|---|
| FOB Price | Quoted | $1.20 |
| Packaging | Custom box $0.25 + poly bag $0.03 | $0.28 |
| Inland Freight | Factory in Shenzhen, near port | $0.02 |
| Ocean Freight (LCL) | $55/CBM ÷ 800 units/CBM | $0.07 |
| Insurance | ($1.20 + $0.07) × 0.004 | $0.01 |
| Customs Duty | HTS 3926.90 at 3.4% of ($1.20 + $0.07 + $0.01) | $0.04 |
| Section 301 Tariff | 25% of ($1.20 + $0.07 + $0.01) | $0.32 |
| Customs Brokerage | $150 ÷ 5,000 units | $0.03 |
| Last-Mile (FBA) | $0.15/unit average | $0.15 |
| Defect Allowance | $2.12 × 2% | $0.04 |
| **Total Landed Cost** | | **$2.16** |

The FOB price is $1.20, but the landed cost is $2.16 — an 80% increase. Without the Section 301 tariff, landed cost would be $1.84, making tariff analysis critical for China-sourced products.

## Quick Estimation Multipliers

When you need a rough landed cost estimate before detailed calculation:

| Route | No Extra Tariffs | With Section 301 (25%) |
|---|---|---|
| China → US West Coast | FOB × 1.45-1.55 | FOB × 1.70-1.85 |
| China → US East Coast | FOB × 1.50-1.65 | FOB × 1.75-1.95 |
| China → EU | FOB × 1.40-1.55 | N/A (different tariff structure) |
| Vietnam → US | FOB × 1.40-1.50 | N/A (no Section 301) |
| India → US | FOB × 1.45-1.60 | N/A (no Section 301) |
| Turkey → EU | FOB × 1.20-1.35 | N/A (customs union) |

These multipliers include average freight, duties, and handling but exclude special tariffs or unusually heavy/bulky products.
