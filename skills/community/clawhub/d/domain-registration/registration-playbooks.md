# Registration Playbooks

Use these patterns for first-time purchases and portfolio expansion.

## Universal Preflight

1. Confirm desired domain list and TLD strategy.
2. Validate availability directly on the target registrar.
3. Confirm premium status, renewal pricing, and transfer constraints.
4. Confirm legal and trademark risk for high-value brand domains.
5. Confirm contact profile and billing approval before writes.

## API-First Registration Pattern

Use when provider exposes registration endpoints and credentials are ready.

```bash
# Generic pattern (provider-specific endpoint and fields required)
curl -sS -X POST "${PROVIDER_API}" \
  -H "Authorization: Bearer ${PROVIDER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"domain":"example.com","years":1,"privacy":true}'
```

Required follow-up:
- validate API success code and order reference
- verify domain appears in account inventory
- enforce lock and renewal settings

## Dashboard-Driven Registration Pattern

Use when no public API is available or billing flow requires UI confirmation.

1. Open registrar dashboard and confirm correct account.
2. Add domains to cart and validate final yearly cost.
3. Enable WHOIS privacy when available.
4. Enable auto-renew only when billing owner confirms.
5. Capture order reference and final renewal date.

## Multi-Domain Batch Rule

- Register one pilot domain first.
- Validate ownership, billing, and DNS control success.
- Proceed in batches only after pilot passes all checks.

## Post-Registration Verification

- Confirm registration status in registrar account.
- Verify WHOIS status and registrant metadata as required.
- Validate nameserver defaults before DNS cutovers.
- Log action details in `changes.md` and renewal window in `inventory.md`.
