# Troubleshooting

## HTTP Error Codes

| Code | Meaning | Action |
|---|---|---|
| 401 | Invalid or missing API key | Check key format and auth header/param |
| 403 | Plan restriction (e.g. gRPC on Free tier) | Upgrade at [rpc.carbium.io](https://rpc.carbium.io) |
| 429 | Rate limit exceeded | Back off immediately; review request volume |
| 400 | Bad request (no route, invalid params) | Check mint addresses, slippage, required params |
| 500 | Server error | Retry after 1 second |
| 503 | Temporary unavailability | Retry with exponential backoff |

## WebSocket Error Codes

| Code | Message | Cause |
|---|---|---|
| `-32700` | Parse error | Malformed JSON or missing required params |
| `-32601` | Method not found | Method name typo or unsupported method |
| `-32602` | Invalid params | Wrong param types or missing fields |
| `-32603` | Internal error | Server-side — retry |

## Common Issues

### "No pool found" (400)

- The token pair has no liquidity on the specified provider
- Try a different provider or use `/quote` (which auto-routes)
- For pump.fun tokens before graduation: use direct bonding curve transactions, not the Swap API

### "API Key not found" (401)

- RPC and Swap API use **separate keys** from separate dashboards
- RPC key: `?apiKey=KEY` or `X-API-KEY` header
- Swap API key: `X-API-KEY` header only
- Check that you're using the correct key for the correct endpoint

### Rate Limited (429)

429 is an architecture signal, not just a retry cue:

- Separate keys for dev/staging/prod
- Do NOT hammer retries — use exponential backoff with jitter
- Isolate retry paths from decision logic
- Check your tier's RPS and monthly credit limits

### Transaction Not Confirmed

1. Check `getSignatureStatus` first — the tx may have already landed
2. If blockhash expired (~60s), get a new blockhash and rebuild
3. Poll with timeout (30-60s) rather than waiting indefinitely
4. Prefer HTTP polling over WebSocket for confirmation (more reliable)

### "sendTransaction" Fails

- Do NOT blindly retry — check `getSignatureStatus` first
- Duplicate transactions waste credits and may cause double-spends
- If simulation failed, inspect the error and do NOT submit
- Check that the blockhash is still fresh

### gRPC "Invalid params" Error

- At least one of `accountInclude` or `accountRequired` must contain values
- Empty arrays for both will return an error
- Check that account addresses are valid base58 strings

### WebSocket Silent Disconnect

- Send ping every 30 seconds to keep the connection alive
- Implement automatic reconnection with exponential backoff
- Re-subscribe to all streams after reconnect
- Cap backoff at 30 seconds

### Gasless Swap Fails

- Output token **must** be SOL for gasless swaps
- The `gasless` flag is ignored if output is not SOL
- Ensure sufficient input token balance (even though no SOL is needed for fees)

### Pump.fun Sniping Issues

| Error | Cause | Fix |
|---|---|---|
| Blockhash expired | Transaction took too long | Get fresher blockhash; reduce latency |
| Insufficient funds | Not enough SOL | Balance must cover amount + fees (~0.005 SOL) |
| Account not found | Token was just created | Retry with 50-100ms delay |
| Slippage exceeded | Price moved during execution | Increase `maxSolCost` or reduce position size |
| Token already graduated | Bonding curve `complete` flag is true | Check `complete` field before buying |

## Timeout Recommendations

| Operation | Recommended Timeout |
|---|---|
| RPC read calls | 5-10 seconds |
| Swap quote requests | 3-5 seconds |
| Transaction confirmation | 30-60 seconds (with polling) |
| gRPC reconnection backoff | 1-30 seconds (exponential) |
| WebSocket reconnection backoff | 1-30 seconds (exponential) |
