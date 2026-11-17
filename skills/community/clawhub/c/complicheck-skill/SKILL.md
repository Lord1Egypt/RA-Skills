---
name: "cosmetic-compliance-check"
description: "Deterministic legal compliance verification for cosmetic formulations against EU CosIng regulations. Resolves trade names to INCI standards."
version: "0.1.3"
protocol: "x402"
price_per_check: "0.10 USDC"
payment_address: "49F85wZ6j8bPvLod3jDn2vLouEedL7QFof1QP23wrGft"
endpoint: "https://engine.lumensentry.com/webhook/check-cosmetic"
metadata:
  tags: [cosmetics, regulatory-compliance, inci, cosing, x402]
  category: "compliance"
---

# Cosmetic Compliance Check Skill

## Operational Overview
Provides sub-10ms deterministic legal compliance checking for cosmetic formulations against the EU CosIng (Annexes II–VI) database. Resolves trade names, CAS numbers, and botanical synonyms to canonical INCI standards.

## When to Use
- Trigger when evaluating a cosmetic formula or ingredient list for EU market access.
- Trigger when determining maximum allowable concentration limits or product category restrictions.

## Data Coverage
CompliCheck indexes ingredients listed in EU CosIng Annexes II–VI — substances subject to restriction, prohibition, or labeling requirements in the EU cosmetics regulation. Common unrestricted ingredients such as Aqua (water), Glycerin, and most emollients are not indexed. Queries for these return `status: "not_found"` with a note explaining they are not subject to a specific EU restriction.

Single-word category terms (Water, Aqua, Oil, Acid, Extract, Fragrance, etc.) are rejected with `not_found` and an explanatory note. Query a specific INCI name or trade name instead.

## Request Specification
- **Method:** `POST`
- **Endpoint:** `https://engine.lumensentry.com/webhook/check-cosmetic`
- **Content-Type:** `application/json`
- **Authentication:** Provide the x402 transaction signature via one of three methods:
  - `Authorization: Bearer <tx_signature>` HTTP header
  - `X-Payment-Hash: <tx_signature>` HTTP header
  - `payment_hash` field in the JSON request body

### Body Schema
```json
{
  "ingredients": ["Methylparaben", "Vitamin C", "Salicylic Acid"],
  "markets": ["EU"],
  "payment_hash": "<solana_transaction_signature>"
}
```

## Response Specification

### Success (HTTP 200 OK)
```json
{
  "results": [
    {
      "query": "Methylparaben",
      "resolved_to": "Methylparaben",
      "cas_number": "99-76-3",
      "confidence": 0.95,
      "status": {
        "EU": {
          "status": "restricted",
          "restriction_type": "both",
          "max_concentration": 0.4,
          "concentration_unit": "percent",
          "allowed_product_types": ["rinse-off"],
          "notes": "Preservative, max 0.4% in rinse-off, prohibited in leave-on"
        }
      }
    }
  ]
}
```

### Not Found (HTTP 200 OK)
```json
{
  "results": [
    {
      "query": "Aqua",
      "resolved_to": null,
      "cas_number": null,
      "confidence": null,
      "status": {
        "EU": {
          "status": "not_found",
          "note": "\"Aqua\" is a category term, not a specific INCI ingredient. Query a specific ingredient name (e.g., \"Methylparaben\", \"Ascorbic Acid\"). If you intended a specific botanical or compound, use its full name."
        }
      }
    }
  ]
}
```

### Payment Error (HTTP 402 Payment Required)

The `details` field distinguishes the failure reason. Agents should inspect it to decide whether to retry, wait, or abandon.

**Replay attack — hash already consumed by a prior request:**
```json
{
  "error": "Payment Required",
  "details": "Transaction hash already consumed (Replay Attack)",
  "status": 402
}
```

**Insufficient payment — sender remitted less than 0.10 USDC:**
```json
{
  "error": "Payment Required",
  "details": "Insufficient payment. Requires 0.10 USDC.",
  "status": 402
}
```

**Transaction not found or failed on-chain — signature is invalid, not yet confirmed, or the transaction errored:**
```json
{
  "error": "Payment Required",
  "details": "Transaction failed or not found on-chain",
  "status": 402
}
```