# Trade Flow

This reference describes how the current CLI quotes and executes trades. Always use the published commands:

- `bfun quote-buy`
- `bfun quote-sell`
- `bfun buy`
- `bfun sell`

## Core workflow

Recommended sequence:

1. `bfun token-info <token>`
2. `bfun token-get <token>` if extra API metadata is useful
3. `bfun quote-buy` or `bfun quote-sell`
4. confirm the operation with the user
5. `bfun buy` or `bfun sell`

Do not skip the quote step for agent-guided trading.

## Phase-aware routing

The CLI has two trading paths:

- bonding-curve helper path
- DEX helper path

`buy` and `sell` choose the function based on the quote result:

| Operation | Curve path | DEX path |
|-----------|------------|----------|
| Buy | `buyWithEth` | `dexBuyWithEth` |
| Sell | `sellForEth` | `dexSellForEth` |

These functions are called on the `BFunFactoryTradeHelper` contract for the active chain.

## Quote behavior

`quote-buy` and `quote-sell` return structured JSON including:

- `phase`
- `pairType`
- `collateralAddress`
- `expectedOut`
- `minOut`
- fee and refund details
- base-unit fields such as `expectedOutWei`, `minOutWei`, `feeWei`

### Slippage

The CLI accepts `--slippage <bps>`.

Rules from the current implementation:

- default is `500` bps
- minimum is `0`
- maximum is `10000`
- invalid or non-integer input causes an error

### Pair handling

The quote layer distinguishes:

- native pair: BNB or wrapped native collateral
- non-native collateral pair

Returned fields:

- `pairType: "eth"` means native BNB-style collateral
- `pairType: "collateral"` means a non-native collateral template
- `tradeWithEth` indicates whether the route converts through the helper for BNB-denominated entry/exit

The helper ABI includes:

- `quoteEthToCollateralForToken`
- `quoteCollateralToEthForToken`
- `quoteDexExactInput`

That allows the CLI to present BNB-denominated quotes even when the market is paired with a non-native collateral asset such as USDC or USDT.

## Buy flow

Command:

```bash
bfun buy <tokenAddress> <bnbAmount> [--slippage <bps>]
```

Behavior:

1. Validates that `bnbAmount > 0`
2. Calls `quoteBuy`
3. Rejects if quoted minimum output is `0`
4. Chooses `buyWithEth` for curve or `dexBuyWithEth` for DEX
5. Sends the transaction with `value = amountInWei`
6. Waits for the receipt and returns JSON

Returned transaction fields include:

- `txHash`
- `action: "buy"`
- `phase`
- `from`
- `token`
- `bnbAmount`
- `expectedTokenOut`
- `minTokenOut`
- `receipt.status`

## Sell flow

Command:

```bash
bfun sell <tokenAddress> <tokenAmount> [--slippage <bps>]
```

Behavior:

1. Validates that `tokenAmount > 0`
2. Calls `quoteSell`
3. Rejects if quoted minimum output is `0`
4. Approves the token first
5. Uses the approval spender based on phase:
   - curve: `BFunFactory`
   - dex: `BFunFactoryTradeHelper`
6. Chooses `sellForEth` for curve or `dexSellForEth` for DEX
7. Waits for the receipt and returns JSON

Returned transaction fields include:

- `txHash`
- `action: "sell"`
- `phase`
- `expectedBnbOut`
- `minBnbOut`
- receipt metadata

## Graduated markets

The agent should treat `graduated` as a stop state even though the quote layer primarily routes between `curve` and `dex`.

Best practice:

1. run `bfun token-info`
2. if phase is `graduated`, do not execute a trade
3. explain that bonding-curve trading has stopped and migration is not yet safely routed as DEX
4. re-check later with `token-info`

## Transfer utility

`bfun send` is not part of the primary trading flow. It sends:

- native BNB when `--token` is omitted
- ERC20 tokens when `--token <tokenAddress>` is provided

Use it only for explicit transfer requests, not as part of a normal market trade.
