# Error codes

All errors return structured JSON with `error`, `code`, and `message` fields.

Signing key env name and setup: **`references/private-key-env.md`** only.

| Code | Meaning |
|------|---------|
| `INVALID_TOKEN` | Unknown vToken name |
| `UNSUPPORTED_TOKEN` | Token not available for on-chain operations |
| `INVALID_ADDRESS` | Bad Ethereum address format |
| `INVALID_AMOUNT` | Amount must be a positive number |
| `INVALID_CHAIN` | Unknown EVM chain name |
| `INSUFFICIENT_BALANCE` | Not enough vETH |
| `CONTRACT_PAUSED` | vETH contract is paused |
| `NOTHING_TO_CLAIM` | No completed redemptions to claim |
| `NO_PRIVATE_KEY` | Signing key not configured or invalid — required to broadcast `mint` / `redeem` / `claim` |
| `NO_PRIVATE_KEY_OR_ADDRESS` | Unsigned transaction build for those commands requires a configured signing key or `--address` (see CLI) |
| `NO_ADDRESS_OR_PRIVATE_KEY` | `balance` or `status` with **no address argument** requires a valid signing key (CLI derives the queried address from it) |
| `RPC_ERROR` | RPC connection failed |
| `API_ERROR` | Bifrost API unavailable or timed out |
| `TX_ERROR` | Transaction execution failed |
| `CLI_ERROR` | Missing argument or invalid option |
