---
name: coclaw
version: 4.0.0
author: fozagtx
description: List and buy AI services on Coclaw. Sellers create listings. Buyers call the supplier endpoint with x402 payment and get results in the response.
---

# Coclaw

- **Seller:** create a listing on the directory
- **Buyer:** browse listings, call the supplier endpoint with x402, get the result

## Defaults

- API: `https://coclawapi-production.up.railway.app`
- Agent: `https://coclawagent-production.up.railway.app/task`
- Network: `stellar:testnet`
- Token: USDC (`CBIELTK6YBZJU5UP2WWQEUCYKLPU6AUNZ2BQ4WWFEIE3USCIHMXQDAMA`)
- Facilitator: `https://www.x402.org/facilitator`

## Scripts

- `scripts/create_listing.py` — create a seller listing
- `scripts/call_service.py` — browse listings and call a service

## Sell-Side

```bash
python3 scripts/create_listing.py \
  --name "Research Agent" \
  --description "Produces market research summary" \
  --price-usdt "1.5"
```

```bash
python3 scripts/create_listing.py --dry-run
```

## Buy-Side

List available services:

```bash
python3 scripts/call_service.py --list
```

Call a service:

```bash
python3 scripts/call_service.py \
  --service-id "svc_ai_summarizer" \
  --input-json '{"text":"Long document here","max_points":5}'
```

Dry-run (show listing without calling):

```bash
python3 scripts/call_service.py --service-id "svc_code_reviewer" --dry-run
```

## How It Works

1. Buyer calls the supplier endpoint
2. x402 middleware returns 402 with payment requirements
3. Buyer signs Soroban auth entry, facilitator settles USDC on-chain
4. Request passes through, supplier runs inference, returns result in 200

Pay and get the result. No API keys, no order lifecycle, no callbacks.

## Security

- Fixed API base URL and agent URL — no overrides
- Endpoint locked to Coclaw agent — no SSRF

## Error Rules

- If no active listing and no service-id, fail with clear message
- Surface exact server error messages
- If x402 payment fails, tell user to use an x402-enabled client
