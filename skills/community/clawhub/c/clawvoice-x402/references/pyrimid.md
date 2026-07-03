# Pyrimid

Pyrimid is an affiliate attribution layer already used elsewhere in the ForgeMesh/x402 stack.

Current package stance:

- Pyrimid-aware in config/catalog.
- Direct x402 remains the default payment path.
- Do not route normal voice payments through Pyrimid by default.
- Do not use `x402HTTPClient` for Pyrimid payment responses.

Known local rule from ForgeMesh production notes:

> Never route Pyrimid 402 responses through `x402HTTPClient`. Use raw viem calls.

Why not default:

- This package's core value is voice setup + wallet bootstrap.
- Pyrimid is useful for affiliate attribution on supported downstream products.
- Adding it to default speech would complicate the install and payment story before the basic ClawHub package is proven.

Future implementation:

1. Add optional `--affiliate-id` and `PYRIMID_AFFILIATE_ID`.
2. Only use Pyrimid for products with `affiliate.pyrimidEligible: true`.
3. Fall back to direct x402 if affiliate validation fails.
4. Record affiliate id and route type in the receipt ledger.
