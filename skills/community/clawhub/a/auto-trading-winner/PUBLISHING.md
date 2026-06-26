# Publish Auto Trading Winner

## 1. Move into the skill folder

```bash
cd skills/auto-trading-winner
```

## 2. Local smoke test

Dry-run on `sim` before publishing:

```bash
source ../../.venv/bin/activate
export SIMMER_API_KEY="sk_live_..."
export TRADING_VENUE="sim"
export MARKET_QUERY="bitcoin"
export MAX_MARKETS="10"
export CANDIDATE_LIMIT="5"
export SELECT_CANDIDATE="1"
python trade_skill.py
```

## 3. Publish the first version

```bash
npx clawhub@latest publish . --slug auto-trading-winner --version 1.0.0
```

## 4. Verify installation

```bash
npx clawhub@latest install auto-trading-winner
```

## 5. Publish an update later

```bash
npx clawhub@latest publish . --slug auto-trading-winner --bump patch
```

## Notes

- Always pass `--slug auto-trading-winner` explicitly.
- `SIMMER_API_KEY` is the only strictly required credential.
- `SOLANA_PRIVATE_KEY` is only needed for live Kalshi self-custody trading.
- `WALLET_PRIVATE_KEY` is only needed for external-wallet Polymarket setups.
- The skill defaults to dry-run unless `--live` or `SIMMER_ENABLE_LIVE=true` is provided.