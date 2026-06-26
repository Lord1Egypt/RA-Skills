# Invoices

Use this reference when the user wants to accept USDT, create a hosted invoice, or inspect invoice lifecycle.

## Create Invoices

Use `POST /api/invoices` with amount, currency, description, reference, and expiry.

The response includes:
- invoice id
- deposit address
- deposit network
- payment URL
- expiry time

## Default Guidance

- Use invoice creation only when the user explicitly wants to collect payment.
- Show the hosted payment URL when the user wants to send a link.
- Use `GET /api/invoices` to inspect the current invoice list.
- Use the public invoice endpoint only for checkout surfaces, not for account management.
