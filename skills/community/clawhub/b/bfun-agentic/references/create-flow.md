# Create Flow

This reference documents the current `bfun create` command implemented by the repo. It is a guide for agents and operators, not a separate launcher. Always execute through `bfun create`, not through ad hoc scripts.

## Required inputs

The command requires:

- `--name <name>`
- `--symbol <symbol>`
- `--image <path>`

The image path is resolved relative to the current working directory. If the file does not exist, the command fails with `Image not found: ...`.

## Standard launch

The minimal launch path is:

```bash
bfun create \
  --name "My Token" \
  --symbol "MTK" \
  --image ./logo.png
```

Useful non-required metadata fields:

- `--description <text>`
- `--website <url>`
- `--twitter <handle>`
- `--telegram <handle>`
- `--pair <type>` with supported values `ETH`, `CAKE`, `USDT`, `USD1`, `ASTER`, `U`, `USDC`

Default pair is `ETH`.

## Advanced market configuration

The create flow builds a `CreateParams` struct and sends either:

- `createBFunToken`
- `createBFunTokenAndBuy`

The second route is used only when `--buy-amount` is provided and is greater than zero.

### Bonding curve and vesting rules

The command enforces these constraints:

- `--bonding-curve-pct` must be between `50` and `80`
- `--vesting-pct` must be between `0` and `30`
- `bonding-curve-pct + vesting-pct + 20 = 100`

That fixed `20` is the migration allocation used by the current helper logic.

Optional vesting fields:

- `--vesting-duration <value>`
- `--cliff-duration <value>`
- `--vesting-recipient <address>`

Duration parsing rules:

- `6m` means 6 months
- `90d` means 90 days
- `1y` means 1 year
- plain numbers are interpreted as days

## Target raise and collateral templates

If `--target-raise` is omitted, the repo uses the collateral template defaults. If the user provides it, the command validates it against the selected pair template:

- minimum: `DEFAULT_TARGET_RAISE / 2`
- maximum: `DEFAULT_TARGET_RAISE * 100`

Current pair defaults come from `src/lib/chain-configs.js`.

### Pair templates (BSC Mainnet)

| Pair | Collateral token | Decimals | Default target raise |
|------|------------------|----------|----------------------|
| `ETH` | native (`0x000...000`) | 18 | `12` |
| `CAKE` | `0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82` | 18 | `6250` |
| `USDT` | `0x55d398326f99059fF775485246999027B3197955` | 18 | `8000` |
| `USD1` | `0x8d0D000Ee44948FC98c9B98A4FA4921476f08B0d` | 18 | `8000` |
| `ASTER` | `0x000Ae314E2A2172a039B26378814C252734f556A` | 18 | `12000` |
| `U` | `0xcE24439F2D9C6a2289F741120FE202248B666666` | 18 | `8000` |
| `USDC` | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` | 18 | `8000` |

## Tax token configuration

Tax is disabled unless `--tax-rate` is set to a non-zero supported value.

Supported tax rates:

- `1`
- `2`
- `3`
- `5`

When tax is enabled, the allocation fields must sum to `100`:

- `--funds-pct`
- `--burn-pct`
- `--dividend-pct`
- `--liquidity-pct`

Additional rules:

- If `--funds-pct > 0`, the user must provide `--funds-recipient` or `--vault-type`
- `--dividend-min-balance` must be at least `10000` when dividend allocation is non-zero
- If tax is disabled, market payout must remain zero-address internally

## Vault modes

Supported vaults are derived from `src/lib/create-helpers.js`:

| Vault type | Behavior | Extra requirement |
|------------|----------|-------------------|
| `split` | Encodes recipient list into vault data | `--split-recipients <json>` |
| `snowball` | Uses the chain `VAULT_KEEPER` address | none |
| `burn_dividend` | Uses the chain `VAULT_KEEPER` address | none |
| `gift` | Encodes an X handle into vault data | `--gift-x-handle <handle>` |

### Split recipients format

Example:

```json
[
  { "address": "0x1111111111111111111111111111111111111111", "pct": 60 },
  { "address": "0x2222222222222222222222222222222222222222", "pct": 40 }
]
```

Validation rules:

- every `address` must be a valid EVM address
- percentages must sum to `100`

### Gift vault handle rules

`--gift-x-handle` must be 1 to 15 characters and match alphanumeric or underscore characters only.

## Optional first buy

`--buy-amount <amount>` performs a first buy during token creation.

Behavior:

- if the pair is native `ETH`, the create transaction sends that amount as `value`
- if the pair is ERC20 collateral, the CLI checks allowance and may reset it to `0` before approving the new amount for USDT-like tokens
- if approval fails or reverts, the CLI aborts

## Execution sequence

The current implementation does the following:

1. Validates input locally
2. Uploads token metadata and image to the B.Fun backend
3. Fetches a salt for the token implementation
4. Builds the `CreateParams` struct from current chain config and CLI options
5. Optionally approves collateral if the selected pair is not native and `--buy-amount` is used
6. Sends the factory transaction
7. Waits for receipt
8. Parses `NewBFunToken` from logs
9. Notifies the backend with the transaction ID

## Operator checklist

Before running `bfun create`, confirm:

- correct chain (BSC mainnet, chain 56)
- correct pair
- image exists on disk
- tax allocations sum correctly
- vesting math sums correctly
- recipient addresses are valid
- write-operation approval has been explicitly granted by the user
