# SanMar Purchase Order Integration

Source basis: `SanMar-Purchase-Order-Integration-Guide-24.1.pdf`.

This page is the reference for PO submission, validation, and downstream fulfillment/invoice workflows.

## Scope

SanMar PO integration supports web-service and file-based submission patterns, with onboarding and production-readiness steps enforced by SanMar.

## Onboarding and activation flow

High-level flow described in guide:

1. Complete base FTP and/or web-service onboarding first.
2. Request PO integration enablement.
3. Execute required test order(s) in test environment.
4. Notify SanMar integration team with test PO identifiers for review.
5. Provide production processing details (user/shipping/payment configuration).
6. Receive production enablement confirmation.

## Authentication and account prerequisites

PO operations are tied to:

- valid SanMar customer/account setup
- approved credit/payment configuration
- valid ship-to and shipping method rules

SME should fail fast with `needs_clarification` when these are underspecified.

## PO-related service operations referenced

Guide references operations including:

- `submitPO`
- `GetSupportedOrderTypes`
- `SendPO` (PromoStandards-aligned naming also referenced as `sendPO`)
- `GetPreSubmitPO` for pre-check/inventory validations

## Recommended write workflow for this SME

1. Validate required identifiers and ship method.
2. Run pre-submit checks (inventory/order-type support) when requested or high-risk.
3. Submit order.
4. Return acknowledgement identifiers and status.
5. Include follow-on expectations (confirmation, shipping notice, invoice paths).

## Shipping and fulfillment considerations

Guide content highlights:

- ship-method constraints and account-specific options
- split-ship / closest-warehouse behaviors
- will-call processing requirements
- decorator/PSST-specific handling and cutoffs

SME response should always state which shipping assumptions were applied.

## File-based PO integration notes

The guide details order processing via multiple coordinated files and strict naming/folder conventions. Duplicate/reused names may trigger resubmission routing.

For any file-based workflow response, include:

- expected file set
- filename correlation key
- drop location
- processed/acknowledged status

## Downstream statuses and artifacts

After submission, callers may need:

- order acknowledgement / confirmation state
- shipment progress
- invoice readiness (including 810-style outputs)

Normalize these into compact status enums in SME responses.

## Example normalized PO submit response

```json
{
  "status": "submitted",
  "po_number": "PO-12345",
  "sanmar_reference": "SM-987654",
  "ship_method": "GROUND",
  "validation": {
    "pre_submit_checked": true,
    "warnings": []
  },
  "next_events": [
    "acknowledgement",
    "shipment_confirmation",
    "invoice"
  ],
  "source": "sanmar_po_integration"
}
```

## High-risk failure cases to guard

- duplicate PO submission / idempotency gaps
- invalid ship-to or unsupported order type
- inventory drift between quote/check and submit
- account not enabled for requested processing mode
- malformed multi-file payload relationships in FTP-based submission
