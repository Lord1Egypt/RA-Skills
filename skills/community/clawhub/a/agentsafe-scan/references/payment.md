# Free → paid flow (API host)

ClawHub installs this skill for free. **Charges happen only on our API after free/pack quota.**

## Free tier

- Default: **20** scans per UTC day per `agent_id`
- **Free watch:** 3 URLs, daily drift check

## Overage micropay (single scan)

1. Hit free/pack daily ceiling → HTTP **402**
2. Read `payment.receive_wallet` + `next_action`
3. Send **≥ 0.05 USDC on Base** to receive wallet
4. Retry `POST /v1/scan` with `payment_tx` = Base tx hash
5. One verified unlock = one overage scan (replay protected)

## Packs (recommended for frequent gates + watch)

| pack_id | USDC / 30d | Daily ceiling | Watch URLs |
|---------|-----------:|---------------|-----------:|
| watch_starter | 9 | 100 | 10 (6h) |
| operator | **29** | **500** | **25 (hourly)** |
| fleet | 99 | 2000 | 100 (30min) |

## Watch / rescan (NEW in v0.1.8)

```bash
curl -sS -X POST https://agentsafe.up.railway.app/v1/watch/add \
  -H 'Content-Type: application/json' \
  -d '{"agent_id":"YourAgent","url":"https://example.com/SKILL.md"}'

curl -sS -X POST https://agentsafe.up.railway.app/v1/watch/check \
  -H 'Content-Type: application/json' \
  -d '{"agent_id":"YourAgent","watch_id":"<id>"}'
```

Drift = content fingerprint changed. Re-scan before allowing.
