# Pump.fun Token Data Sources

## Problem
pump.fun API (frontend-api.pump.fun, api.pump.fun, etc.) blocks server IPs with Cloudflare challenge.
Returns "Redirecting to blocked" HTML instead of JSON.

## Working Alternative: DexScreener API
No auth required. Returns pump.fun tokens on Solana.

### Search for tokens
```bash
curl -s "https://api.dexscreener.com/latest/dex/search?q=pumpswap" | python3 -c "import sys,json; [print(p['baseToken']['name'], p['marketCap']) for p in json.load(sys.stdin).get('pairs',[])]"
```

### Get token by address
```bash
curl -s "https://api.dexscreener.com/tokens/<TOKEN_ADDRESS>"
```

### Response fields
- baseToken.name, baseToken.symbol, baseToken.address
- marketCap, fdv, priceUsd
- volume.h24, volume.h1, volume.m5
- priceChange.h24, priceChange.h1, priceChange.m5
- txns.h1.buys, txns.h1.sells, txns.m5.buys, txns.m5.sells
- liquidity.usd
- dexId (pumpswap, pumpfun, meteora, etc.)
- pairCreatedAt (timestamp)

### Filter for pump.fun tokens
```python
pairs = [p for p in data['pairs'] if p.get('chainId') == 'solana']
# dexId will be 'pumpswap' or 'pumpfun' for pump.fun tokens
```

## On-Chain: SLV RPC
Use our SLV RPC to monitor pump.fun program transactions:
```bash
curl -s https://edge.erpc.global?api-key=YOUR_KEY \
  --header 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"getSignaturesForAddress","params":["6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",{"limit":10}]}'
```

## PumpFun Sniper (local scoring)
At /tmp/pumpfun-sniper/scripts/scorer.py
```bash
python3 /tmp/pumpfun-sniper/scripts/scorer.py <TOKEN_CA>
```
Scores tokens 0-100 based on dev wallet, socials, liquidity, holder concentration.
