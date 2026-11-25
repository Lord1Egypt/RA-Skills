# EIP-1559 Gas Market on Base L2

## How Base Gas Works

Base uses EIP-1559 fee market:
- **Base Fee:** Adjusted per block based on congestion (target: 50% gas limit)
- **Priority Fee:** Tip to miners/sequencer (usually very low on L2)
- **Total Fee:** base + priority

## Base L2 Specifics

| Parameter | Value |
|-----------|-------|
| Block time | ~2 seconds |
| Gas limit | 30M per block |
| Target gas | 15M per block |
| Base fee minimum | Very low (~0.001 gwei typical) |
| Priority fee typical | 0.0001 - 0.001 gwei |

## Congestion Patterns

Base gas spikes during:
- Major NFT mints
- Airdrop claims
- Popular DeFi protocol launches
- US market hours (14:00-22:00 UTC)

## Prediction Model

Our predictor uses:
1. Simple moving average (20, 50, 200 block)
2. Ratio to historical average
3. Time-of-day weighting (future enhancement)

## RPC Endpoints

The script defaults to the public no-key endpoint `https://mainnet.base.org`.
To use a keyed provider instead, set the full endpoint URL in the
`BASE_RPC_URL` environment variable (or pass `--rpc-url`). Never hardcode
an API key into the skill — keys live only in the operator's environment.

- Public (default, no key): `https://mainnet.base.org`
- Alchemy: `https://base-mainnet.g.alchemy.com/v2/<key>` (key from your environment only)
- QuickNode: `https://<subdomain>.base-mainnet.quiknode.pro/` (key from your environment only)

## References

- Base docs: https://docs.base.org
- EIP-1559: https://eips.ethereum.org/EIPS/eip-1559
