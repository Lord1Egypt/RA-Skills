# Synthetic hand-computed example

[capture.json](capture.json) is generated synthetic data with an illustrative account. It is not a real wallet's activity and does not prove live API behavior.

| Default-perp fill | Notional | Closed PnL USDC | Signed fee USDC | Liquidity |
| --- | --- | --- | --- | --- |
| ETH buy 10 at 100 | 1000 | 0 | 1 | taker |
| ETH sell 5 at 110 | 550 | 50 | -0.25 | maker |
| BTC buy 1 at 200 to close a short | 200 | -10 | 2 | taker |

The ETH close appears twice with the same trade ID and identical content; it counts once. The ETH opening fee includes `builderFee: 0.2`, already part of the total `fee: 1`.

- Closed PnL: `0 + 50 - 10 = 40` USDC.
- Signed fees: `1 - 0.25 + 2 = 2.75` USDC. Positive charges are 3, rebates 0.25.
- Funding: `-3 ETH + 0.5 BTC = -2.5` USDC.
- Observed net: `40 - 2.75 - 2.5 = 34.75` USDC.
- Notional: `1000 + 550 + 200 = 1750` USDC. Maker share: `550 / 1750 = 31.4285%`; taker share: `1200 / 1750 = 68.5714%`.
- Positive fee concentration: BTC `2 / 3 = 66.6666%`, ETH `1 / 3 = 33.3333%`.
- Current exposure: long ETH notional 550, short BTC notional 400. Gross 950, signed net 150. ETH represents `550 / 950 = 57.8947%` of gross notional.

Spot and HIP-3 fills and HIP-3 funding are captured but excluded from the default-perp calculations. The BTC first observed fill starts with a short of 3; its earlier costs are unknown. Current state is captured one day after the activity window ends. A trigger order is observed but protection is not assessed. Available history ends below the page limit; complete-window coverage remains unverified.
