---
name: pay-for-service
description: >
  Make paid requests to x402-enabled APIs using USDC on Base.
  Use when the user explicitly asks to call a paid API, make an x402 payment,
  pay for a request, or fetch from a paid endpoint.
  Covers "call this API", "pay for", "use this service", "make a paid call".
user-invocable: true
disable-model-invocation: true
context: fork
allowed-tools:
  - "Bash(npx agnic@latest status*)"
  - "Bash(npx agnic@latest x402 pay *)"
  - "Bash(npx agnic@latest x402 details *)"
  - "Bash(npx agnic@latest balance*)"
---

# Paying for x402 Services

Use `npx agnic@latest x402 pay` to call x402-enabled API endpoints with automatic USDC payment on Base.

## Authentication

Run `npx agnic@latest status --json` to verify. If not authenticated:
- **Headless (CI/server/agent)**: Set `AGNIC_TOKEN` env var or pass `--token <token>`
- **Interactive (has browser)**: Run `npx agnic@latest auth login`

See the `authenticate-wallet` skill for details.

## Command Syntax

```bash
npx agnic@latest x402 pay <url> [-X <method>] [-d <json>] [-q <params>] [-h <json>] [--max-amount <n>] [--json]
```

See `reference/x402-protocol.md` for full options, USDC amounts, and input validation rules.

## Workflow

1. **Check requirements** (optional but recommended):
   ```bash
   npx agnic@latest x402 details <url>
   ```
   Shows price, method, and schema without making a payment.

2. **Verify balance**:
   ```bash
   npx agnic@latest balance --network base
   ```

3. **Make the paid request**:
   ```bash
   npx agnic@latest x402 pay <url> --json
   ```

## Examples

```bash
# GET request (auto-pays)
npx agnic@latest x402 pay https://example.com/api/weather --json

# POST request with body
npx agnic@latest x402 pay https://example.com/api/sentiment -X POST -d '{"text": "I love this product"}' --json

# Limit max payment to $0.10
npx agnic@latest x402 pay https://example.com/api/data --max-amount 100000 --json
```

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)
- Wallet must have sufficient USDC balance on Base

## Error Handling

Common errors:

- "Not authenticated" -- Run `npx agnic@latest auth login` or set `AGNIC_TOKEN`
- "Insufficient balance" -- Fund wallet with USDC (`npx agnic@latest balance` to check)
- "No X402 payment requirements found" -- URL may not be an x402 endpoint
- Invalid JSON in `--data` -- Ensure the body is valid JSON before passing
- HTTP 4xx/5xx from the API -- Show the status code and response body to the user
