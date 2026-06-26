# Payment Tokens

Use this file when the user wants to specify or identify a supported `paymentToken`.

This skill does **not** treat ERC20 payment tokens as broadly supported. Only the chain-token combinations in the table below should be used as supported non-default ERC20 payment tokens. Everything else should be treated as unsupported unless it is the chain's native token or wrapped native token.

## Token Decimals

Use token decimals when converting a user-facing amount into `paymentTokenAmount`.

Formula:

`amountInBaseUnits = amountInToken * (10 ^ decimals)`

Quick rules:

- Native tokens such as `ETH` use `18` decimals
- `bsc` `USDT` and `USD1` in this table use `18` decimals
- `base` `USDC` in this table uses `6` decimals
- `polygon` `ETH` in this table uses `18` decimals

Examples:

- `0.5 ETH` -> `500000000000000000`
- `100 USDC` with `6` decimals -> `100000000`
- `0.01 BSC USDT` with `18` decimals -> `10000000000000000`

## Supported Non-default Payment Tokens

| Chain | Token | Address | Decimals | Support Rule | Notes |
|-------|-------|---------|----------|--------------|-------|
| `bsc` | `USD1` | `0x8d0D000Ee44948FC98c9B98A4FA4921476f08B0d` | `18` | Supported | Supported on BSC as a custom ERC20 payment token |
| `bsc` | `USDT` | `0x55d398326f99059fF775485246999027B3197955` | `18` | Supported | Supported on BSC as a custom ERC20 payment token |
| `base` | `USDC` | `0x833589fCD6EDB6E08f4c7C32D4f71b54bdA02913` | `6` | Supported | Supported on Base as a custom ERC20 payment token |
| `polygon` | `ETH` | `0x7ceb23fd6bc0add59e62ac25578270cff1b9f619` | `18` | Supported | Use Polygon WETH for `ETH` pricing requests on Polygon |

## Chain Support Rules

- `bsc`: supports `USDT`, `USD1`, native token, and wrapped native token
- `base`: supports `USDC`, native token, and wrapped native token
- `polygon`: supports `ETH`, native token, and wrapped native token
- Other chains: support only native token and wrapped native token
- Any other ERC20 should be treated as unsupported


## Usage Pattern

When the user says:

- "Sell for USDT"
- "Create an offer in USDC"
- "Use USDC on Base"
- "Use USD1 on BSC"

First check whether that `chain + token` pair is explicitly supported by this file.

- If supported, map the token symbol to the payment token address for the requested chain, then pass that address as `paymentToken`
- If not supported, do not guess another ERC20 address; tell the user that this skill currently supports only the documented payment tokens for that chain, or fall back to native / wrapped native token flow

For `buy`, if the token's decimals are known from this table, also pass them as `paymentTokenDecimals` to avoid runtime guessing.

For `sell` and `offer`, use the same decimals when converting the human price into `paymentTokenAmount`.

When responding to the user:

- Resolve token names by exact `chain + address` match only
- Do not infer a token symbol from decimals, chain, or price alone
- If the payment token address is not in this table, show the raw token address or `unknown ERC20` instead of guessing a symbol
- If the requested ERC20 is outside the supported set above, say it is not supported by this skill on that chain

## Important Notes

- `offer` should use ERC20 payment tokens only
- For `offer`, wrapped native tokens such as `WETH` or `WBNB` remain the default when `paymentToken` is omitted
- Stablecoin contract addresses vary by chain; never reuse an address across chains
- Do not expand support beyond the table in this file without an explicit code or skill update
