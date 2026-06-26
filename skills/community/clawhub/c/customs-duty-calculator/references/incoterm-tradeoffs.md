# DDP vs DDU Tradeoffs

The Incoterm choice changes who pays the duty, when, and what happens if anything goes wrong.

## DDP (Delivered Duty Paid)

Seller is responsible for getting the goods to the buyer's door including all duties and import taxes.

**Pros:**
- Clean buyer experience; no surprise bills.
- Single quoted price; lower checkout abandonment.
- Returns are simpler (the seller is the importer of record).
- Better marketplace performance — many platforms favor or require DDP for prime-style experiences.

**Cons:**
- Seller carries cash flow for duty and VAT upfront.
- Margin model must include true landed cost. Underestimate = direct margin loss.
- VAT registrations may be required in the destination country once volume crosses thresholds (EU OSS / IOSS, UK).
- Refunding duty on returns is complex; carriers offer reclaim services but with fees.
- Rate changes are absorbed by the seller until rebill.

**Use when:** Per-shipment duty is small (<USD 50 typically), buyer experience matters, you sell on marketplaces that expect DDP, or you're building a brand.

## DDU / DAP (Delivered Duty Unpaid / Delivered At Place)

Buyer pays duty and VAT at delivery (collected by the carrier).

**Pros:**
- Cleaner seller P&L; duty is the buyer's problem.
- Lower cash-flow exposure.
- Useful for B2B where the buyer is a registered importer.

**Cons:**
- Surprise bills lead to refusals, returns, and reputational damage.
- Higher abandonment if duty estimate is shown at checkout.
- Carrier brokerage can stack significantly on small parcels.
- Complicates returns; the buyer may abandon when faced with the duty bill.
- Wrecks NPS in consumer markets unfamiliar with cross-border purchases.

**Use when:** Duty is large and uncertain, the buyer is B2B and accustomed to importing, or operating in a market with mature cross-border consumer expectations.

## Hybrid: prepaid DDU

Some carriers (DHL, FedEx, UPS) offer "duty prepay" at checkout — duty is collected from the buyer but paid at the border by the carrier on the seller's account. Cleaner UX than pure DDU; lower cash-flow load than full DDP. Available where supported.

## Decision matrix

| Factor | Lean DDP | Lean DDU |
|---|---|---|
| Per-shipment duty < USD 50 | ✓ | |
| Per-shipment duty > USD 200 | | ✓ |
| Brand-direct consumer | ✓ | |
| B2B buyer | | ✓ |
| Marketplace listing | ✓ | |
| Volatile duty rates | | ✓ |
| Strong cash position | ✓ | |
| Returns volume > 10% | | ✓ |

## Always do

- Quote landed cost transparently in marketing material and PDP.
- Refresh the rate quarterly.
- Reconcile actual customs invoices monthly against quoted rate; investigate variance > 10%.
- Keep documentation for the legal retention period.
