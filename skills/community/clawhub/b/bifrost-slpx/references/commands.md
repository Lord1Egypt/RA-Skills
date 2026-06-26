# Command reference

Always pass `--json` when invoking from an agent unless you intentionally need human-readable text.

Prefix: `npx -y @bifrostio/slpx-cli`

## Query commands (all vTokens)

### `rate [amount]`

Exchange rate. Default: 1 unit of base asset.

```bash
npx -y @bifrostio/slpx-cli rate --json
npx -y @bifrostio/slpx-cli rate 10 --json
npx -y @bifrostio/slpx-cli rate --token vDOT --json
npx -y @bifrostio/slpx-cli rate 100 --token vKSM --json
```

Output fields: `inputAmount`, `outputAmount`, `inputToken`, `outputToken`, `rate` (`tokenToBase`: `inputToken` per 1 `outputToken`), `source` (on-chain fallback also: `chain`)

**`rate` semantics (agents):** snapshot only—how many units of `inputToken` one `outputToken` commands **at request time**. The JSON has **no** inception date, **no** history, and **no** “cumulative return” label. Do **not** equate `(rate − 1)` with “appreciation since inception” or any other period; that is inferential, not in the data.

### `apy`

Staking APY (base + reward). Add `--lp` for LP pool yields from DeFiLlama.

```bash
npx -y @bifrostio/slpx-cli apy --json
npx -y @bifrostio/slpx-cli apy --token vDOT --json
npx -y @bifrostio/slpx-cli apy --token vMANTA --json
npx -y @bifrostio/slpx-cli apy --token vDOT --lp --json
```

Output fields: `token`, `totalApy`, `baseApy`, `rewardApy`, `rewardApyIncentiveAsset`

- `baseApy` — native staking yield on the underlying chain (Bifrost API: `apyBase`)
- `rewardApy` — Bifrost farming incentive component (Bifrost API: `apyReward`)
- `rewardApyIncentiveAsset` — **vDOT** for **vETH** only; **BNC** for every other vToken
- `totalApy` — `baseApy` + `rewardApy`

With `--lp`: adds `lpPools` — each entry: `symbol`, `project`, `chain`, `lpApy`, `tvl`

### `info`

Protocol overview: rate, APY, TVL, holders. vETH also: contract, chains, paused.

```bash
npx -y @bifrostio/slpx-cli info --json
npx -y @bifrostio/slpx-cli info --token vDOT --json
npx -y @bifrostio/slpx-cli info --token vASTR --json
```

Output fields: `protocol`, `inputAmount`, `outputAmount`, `inputToken`, `outputToken`, `rate` (`tokenToBase`), `totalApy`, `baseApy`, `rewardApy`, `tvl`, `totalStaked` (amount in `inputToken`), `totalSupply` (amount in `outputToken`), `holders`  
`rate` here matches **`rate` command** semantics: **spot** `tokenToBase`, **no** time dimension in the JSON.  
vETH extra: `contract`, `chains`, `paused`

## On-chain commands (vETH only)

### `balance [address]`

vETH balance and ETH equivalent. **Omit `address`** to query the CLI **default signing wallet**. Comma-separated addresses for batch.

```bash
npx -y @bifrostio/slpx-cli balance --json
npx -y @bifrostio/slpx-cli balance 0x742d...bD18 --json
npx -y @bifrostio/slpx-cli balance 0x742d...bD18 --chain base --json
npx -y @bifrostio/slpx-cli balance 0xAddr1,0xAddr2,0xAddr3 --json
```

Single: `address`, `vethBalance` (vETH, amount only), `ethValue` (ETH, amount only), `chain`  
Batch: `results` (`{address, vethBalance, ethValue}`), `chain`

### `status [address]`

Redemption queue status. Omit address to query the **default signing wallet** (same as `balance`).

```bash
npx -y @bifrostio/slpx-cli status --json
npx -y @bifrostio/slpx-cli status 0x742d...bD18 --json
```

Output: `address`, `claimableEth` (ETH, amount only), `pendingEthAmount` (ETH, amount only), `chain`, `hint` (time estimate when pending; may include units in prose)

### `mint <amount>`

Stake ETH → vETH. `--weth` uses WETH instead of native ETH.

```bash
npx -y @bifrostio/slpx-cli mint 0.1 --json
npx -y @bifrostio/slpx-cli mint 0.5 --chain base --json
npx -y @bifrostio/slpx-cli mint 0.1 --weth --json
npx -y @bifrostio/slpx-cli mint 0.5 --weth --chain arbitrum --json
```

Native ETH (unsigned preview): `action`, `inputAmount`, `inputToken` (`ETH`), `expectedAmount`, `expectedToken` (`vETH`), `mode`, `from` (signer/receiver when applicable), `unsigned.to`, `unsigned.value`, `unsigned.data`, `unsigned.chainId`  
WETH (unsigned preview): `action:mint-weth`, `inputAmount`, `inputToken` (`WETH`), `expectedAmount`, `expectedToken` (`vETH`), `mode`, `from`, `wethAddress`, `steps` (Approve, Deposit; deposit `receiver` aligns with `from` when using address-only flows)  
Signed: same amount/token fields plus `from`, `txHash`, `explorer`

WETH contract addresses: see `tokens-and-chains.md`.

### `redeem <amount>`

Redeem vETH — **not instant** (queue, often 1–3 days).

> Before broadcasting `redeem`, confirm with the user: amount, chain, and that redemption is queued (not instant).

```bash
npx -y @bifrostio/slpx-cli redeem 0.1 --json
```

### `claim`

Claim completed ETH after redemption.

```bash
npx -y @bifrostio/slpx-cli claim --json
```

## Global options

| Option | Description | Default |
|--------|-------------|---------|
| `--token <name>` | `vETH`, `vDOT`, `vKSM`, `vBNC`, `vGLMR`, `vMOVR`, `vFIL`, `vASTR`, `vMANTA`, `vPHA` | `vETH` |
| `--chain <name>` | `ethereum`, `base`, `optimism`, `arbitrum` (vETH on-chain only) | `ethereum` |
| `--rpc <url>` | Custom RPC | auto per chain |
| `--json` | JSON output | false |

## Transaction-related options

| Option | Description |
|--------|-------------|
| `--weth` | Mint from WETH (not native ETH) |
| `--lp` | LP yields on `apy` only |
| `--address <addr>` | **`balance` / `status`:** use the positional `[address]` (comma-separated batch for `balance`); omit to use the default signing wallet. **`mint` / `redeem` / `claim`:** optional when broadcasting (CLI uses the signing wallet); see CLI `--help` for edge cases. |

## Workflow examples

### Compare APYs (with LP)

```bash
npx -y @bifrostio/slpx-cli apy --token vDOT --lp --json
npx -y @bifrostio/slpx-cli apy --token vETH --lp --json
npx -y @bifrostio/slpx-cli apy --token vKSM --json
```

### Batch balances

```bash
npx -y @bifrostio/slpx-cli balance 0xAddr1,0xAddr2,0xAddr3 --json
```

### Research → stake (vETH)

```bash
npx -y @bifrostio/slpx-cli info --json
npx -y @bifrostio/slpx-cli rate 1 --json
npx -y @bifrostio/slpx-cli apy --json
npx -y @bifrostio/slpx-cli mint 0.5 --json
# Broadcast after pre-tx checklist + explicit user approval.
```

### Redeem → claim (vETH)

```bash
npx -y @bifrostio/slpx-cli balance 0x... --json
npx -y @bifrostio/slpx-cli redeem 1.0 --json
npx -y @bifrostio/slpx-cli status --json
npx -y @bifrostio/slpx-cli claim --json
```

## Operational notes

1. Query commands use the Bifrost API for all 10 vTokens.
2. On-chain commands are vETH-only on the listed EVM chains.
3. Redemption goes through Bifrost’s cross-chain queue — not immediate settlement.
4. **`mint` / `redeem` / `claim`:** broadcasting requires a configured signing key (default for this skill). See `references/errors.md` (`NO_PRIVATE_KEY`, `NO_PRIVATE_KEY_OR_ADDRESS`) and `references/private-key-env.md` if setup is missing.
5. **`balance` / `status`:** omitting the address uses the default signing wallet; otherwise pass an address. See `NO_ADDRESS_OR_PRIVATE_KEY` in `references/errors.md`.
6. RPC: CLI may fall back to backup endpoints if primary RPC fails.
7. `--weth` unsigned flow emits Approve + Deposit steps.
8. `--lp` on `apy` pulls DeFiLlama pool data for the selected vToken.
