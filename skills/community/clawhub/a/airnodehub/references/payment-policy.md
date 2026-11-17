# Payment policy

This skill is deliberately non-spending.

Before calling, inspect the live document. If x-airnode.payment.prices contains the operation, return needs-payment-authorisation with operation, published price, network and asset. Treat HTTP 402 and MCP payment refusals the same way; discovery does not grant payment authority.

Do not accept or read raw private keys, infer payment authority from wallet availability, sign an x402 authorization, silently substitute a free provider, or retry a paid operation as if it were free.

A separate authorized payer must enforce the user's maximum spend, timeout and fallback policy, reconcile uncertain settlement before retrying, and retain the settlement evidence returned by the actual x402 version. This helper never installs a payer or handles payment secrets.
