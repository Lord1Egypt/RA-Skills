# Currency Resolution

When users specify currency names (SOL, ETH, BNB, USDC) instead of addresses, the CLI auto-resolves to the correct on-chain address.

## Resolution Table

| Chain | Name | Address |
|-------|------|---------|
| sol | SOL | `So11111111111111111111111111111111111111112` |
| sol | USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| bsc | BNB | `0x0000000000000000000000000000000000000000` |
| bsc | USDC | `0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d` |
| eth | ETH | `0x0000000000000000000000000000000000000000` |
| eth | USDC | `0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eB48` |

## Examples

```bash
# These are equivalent:
npx @chainstream-io/cli dex route --chain sol --from <wallet> --input-token SOL --output-token <addr> --amount 1000000
npx @chainstream-io/cli dex route --chain sol --from <wallet> --input-token So11111111111111111111111111111111111111112 --output-token <addr> --amount 1000000
```

Currency resolution is case-insensitive (sol, Sol, SOL all work).
