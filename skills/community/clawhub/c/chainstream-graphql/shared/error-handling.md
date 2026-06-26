# Error Handling

## HTTP Status Codes

| Code | Meaning | Retryable | Recovery |
|------|---------|-----------|----------|
| 400 | Bad request (invalid params) | No | Fix parameters |
| 401 | Auth invalid/expired | No | First `config auth` → if not logged in, `login` (auto-grants nano trial 50K CU) → retry. If still failing, check API key: `config set --key apiKey --value <key>`. See [authentication.md](authentication.md#agent-bootstrap-checklist) |
| 402 | No quota / payment required | No | First `config auth` → `login` if needed (trial may suffice) → `plan status` → if trial exhausted, `wallet pricing` then `plan purchase`. See [x402-payment.md](x402-payment.md) |
| 404 | Resource not found | No | Verify chain/address |
| 429 | Rate limit exceeded | Yes | Exponential backoff: 1s → 2s → 4s → 8s (max 3 retries) |
| 500 | Server error | Yes | Retry once after 2s |
| 502/503 | Service unavailable | Yes | Retry after 5s |

## SDK Auto-Retry

`@chainstream-io/sdk` has built-in retry via `axios-retry`:
- Retries on 429 and 5xx
- Exponential backoff
- Max 3 retries

## DeFi-Specific Errors

| Error | Meaning | Recovery |
|-------|---------|----------|
| Transaction reverted | On-chain execution failed | Do NOT auto-retry; show error to user |
| Slippage exceeded | Price moved beyond tolerance | Re-quote with higher slippage, get fresh confirmation |
| Insufficient balance | Wallet doesn't have enough tokens | Show current balance, suggest lower amount |
| Job timeout | No on-chain confirmation within 60s | Show job ID and tx hash for manual verification |
| Invalid signature | Wallet signing failed | Check wallet config: `chainstream wallet address` or re-login: `chainstream login` |

## Rate Limits

| Plan | Requests/second |
|------|----------------|
| Free | 10 |
| Starter | 50 |
| Pro | 200 |
| Enterprise | 1000 |
