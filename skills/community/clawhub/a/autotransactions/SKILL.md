Sure — here is the English version with the small change included:

````markdown
---
name: polymarket-minimal-buy-python
description: Use Python to run a minimal authenticated Polymarket trading client with private key loaded from private.env. Supports initialize/signing auth, market buy/sell, limit buy/sell, open orders, single-order lookup, and order cancellation.
---

# Polymarket Minimal Trading Python

Provide a minimal runnable Python trading client for Polymarket. The private key is loaded from `private.env` and used for authenticated signing.

## Features

- initialize with private key
- market buy / sell
- limit order buy / sell
- auto allowance authorization (USDC for BUY, conditional token for SELL)
- get open orders / get single order
- cancel single / cancel all
- auto create `private.env` if missing, then prompt the user to fill in a MetaMask or other decentralized wallet private key

## Setup

```bash
pip install py-clob-client eth-account

# Auto-create private.env if it does not exist
test -f private.env || cat > private.env <<'EOF'
POLYMARKET_PRIVATE_KEY=
EOF

echo "Created private.env if it was missing. Please open it and paste in the private key from your MetaMask or other decentralized wallet."
````

## Env

Prefer reading `private.env` from the skill directory, and also support system environment variables.

* `POLYMARKET_PRIVATE_KEY` (required)

Example:

```env
POLYMARKET_PRIVATE_KEY=your_wallet_private_key
```

Please write the private key from your **MetaMask** or another **decentralized wallet** into the `private.env` file.

## Usage

```bash
# Market buy
python3 scripts/min_buy.py market-buy --token-id <TOKEN_ID> --amount 10

# Market sell
python3 scripts/min_buy.py market-sell --token-id <TOKEN_ID> --amount 10

# Limit buy
python3 scripts/min_buy.py limit-buy --token-id <TOKEN_ID> --price 0.45 --size 20

# Limit sell
python3 scripts/min_buy.py limit-sell --token-id <TOKEN_ID> --price 0.55 --size 20

# Query orders
python3 scripts/min_buy.py open-orders
python3 scripts/min_buy.py get-order --order-id <ORDER_ID>

# Cancel orders
python3 scripts/min_buy.py cancel-order --order-id <ORDER_ID>
python3 scripts/min_buy.py cancel-all
```



A slightly cleaner prompt line for the setup section would be:

```bash
echo "Please edit private.env and fill in POLYMARKET_PRIVATE_KEY with the private key from your MetaMask or other EVM-compatible decentralized wallet."
````
