# x402-Agent-Pay.com Reference

## Registration
- Web: https://x402-agent-pay.com/register (manual form)
- API: POST https://x402-agent-pay.com/api/agentpay/register
- Body: {"name": "...", "email": "..."}
- Returns: {partner_id, api_key, api_token, success, message}

## Authentication
- Header: X-Partner-Token: <api_key>
- All requests require this header

## Endpoints
| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/agentpay/register | No | Register agent |
| GET | /api/partner/balance?partner_id=X | Yes | Balance + stats |
| POST | /x402/settle | Yes | Settle payment |
| POST | /x402/verify | Yes | Verify payment |
| GET | /x402/info | No | Facilitator info |
| GET | /x402/stats | Yes | Platform stats |

## Supported Chains
- Base L2 (chain 8453) — $0.02 flat fee
- Ethereum, Optimism, Arbitrum, Polygon — free (gas only)

## Treasury
0x367F1b3D8Ca90D1e087481a9A40d585Bf3451a03

## Partner Dashboard
https://x402-agent-pay.com/dashboard (login with API key)

## Marketplace
https://x402-agent-pay.com/marketplace (search for partner_id)

## Registration Response Example
```json
{
  "success": true,
  "partner_id": "maliotsol",
  "api_key": "102b6e1b287bb3c5087a99411616ffcea4743ee0715e16154ed12f004eb7fad6",
  "message": "Registration complete."
}
```

## Balance Response Example
```json
{
  "partner_id": "maliotsol",
  "claimable_usdc": 0.0,
  "lifetime_count": 0,
  "lifetime_fees": 0.0,
  "share_percentage": 0.0,
  "payout_verified": false,
  "payout_address": null
}
```
