---
name: bifrost-slpx-stake
description: |
  Execute liquid staking operations on Bifrost SLPx protocol across Ethereum, Base, Optimism,
  and Arbitrum. Mint vETH by staking ETH/WETH, redeem vETH back to ETH, and claim after
  redemption completes. Supports manual signing and agent-side signing via ERC-4626 vault.
  Use when users want to stake, unstake, mint, redeem, or claim ETH on Bifrost DeFi.
metadata:
  author: bifrost.io
  version: "1.0.0"
---

# Bifrost SLPx Stake

Execute Bifrost vETH liquid staking operations: mint, redeem, and claim.

## Contract & Network

vETH is deployed on Ethereum and three L2 networks. The same contract address is used across all chains.

| Chain | ChainId | VETH Contract | WETH (underlying) | Default RPC | Fallback RPC |
|-------|---------|---------------|--------------------|----|------|
| Ethereum | 1 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` | `https://ethereum.publicnode.com` | `https://1rpc.io/eth` |
| Base | 8453 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x4200000000000000000000000000000000000006` | `https://base.publicnode.com` | `https://1rpc.io/base` |
| Optimism | 10 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x4200000000000000000000000000000000000006` | `https://optimism.publicnode.com` | `https://1rpc.io/op` |
| Arbitrum | 42161 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` | `https://arbitrum-one.publicnode.com` | `https://1rpc.io/arb` |

## Configuration

On first run, ask the user whether they want to configure custom settings. If not, use the defaults above.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BIFROST_CHAIN` | Target chain name (`ethereum`, `base`, `optimism`, `arbitrum`) | `ethereum` |
| `BIFROST_RPC_URL` | Custom RPC endpoint | Per-chain default from table above |
| `BIFROST_VETH_ADDRESS` | VETH contract address (override) | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` |
| `BIFROST_PRIVATE_KEY` | Private key for agent-side signing (hex, with or without 0x prefix) | Not set (manual signing mode) |

### Wallet Setup

Two signing modes. Default is manual signing (no setup needed).

**Default: Manual Signing**

Output complete transaction details (to, value, data, gas, chainId). User signs with their own wallet (MetaMask, Ledger, CLI, etc.).

**Option: Agent-Side Signing**

Set `BIFROST_PRIVATE_KEY` as an environment variable, or import via Foundry keystore:

```bash
cast wallet import bifrost-agent --interactive
```

When `BIFROST_PRIVATE_KEY` is set, the agent can sign and broadcast transactions directly using `cast send`.

## Quick Reference

### Write Operations

| Operation | Function | Selector | Description |
|-----------|----------|----------|-------------|
| Mint vETH (via ETH) | `depositWithETH()` | `0x1166dab6` | Stake native ETH to mint vETH. ETH is sent as `msg.value`. The contract wraps ETH → WETH internally — no ERC-20 approval needed. Reverts `EthNotSent()` if `msg.value == 0` |
| Mint vETH (via WETH) | `deposit(uint256,address)` | `0x6e553f65` | Deposit WETH directly to mint vETH for `receiver`. Requires prior WETH approval to the VETH contract |
| Redeem vETH | `redeem(uint256,address,address)` | `0xba087652` | Burn `shares` of vETH to initiate ETH withdrawal for `receiver`. ETH enters a redemption queue and is NOT returned instantly. Requires `owner == msg.sender` or sufficient allowance |
| Claim as ETH | `withdrawCompleteToETH()` | `0x3ec549e9` | Claim ALL completed withdrawals as native ETH. Internally calls `withdrawCompleteTo(this)` then unwraps WETH → ETH. Reverts `EthTransferFailed()` if ETH transfer fails |
| Claim as WETH | `withdrawComplete()` | `0x266a3bce` | Claim ALL completed withdrawals as WETH to `msg.sender`. Use this if `withdrawCompleteToETH()` fails |
| Claim to address | `withdrawCompleteTo(address)` | `0xf29ee493` | Claim ALL completed withdrawals as WETH to a specified `receiver` address |

### Pre-Execution Query Functions

| Query | Function | Selector | Description |
|-------|----------|----------|-------------|
| Preview deposit | `previewDeposit(uint256)` | `0xef8b30f7` | Simulate deposit and return exact vETH shares to be minted |
| Preview redeem | `previewRedeem(uint256)` | `0x4cdad506` | Simulate redemption and return exact ETH to be returned |
| Fallback: shares calc | `convertToShares(uint256)` | `0xc6e6f592` | Convert ETH amount to vETH shares using current Oracle exchange rate |
| Fallback: assets calc | `convertToAssets(uint256)` | `0x07a2d13a` | Convert vETH shares to ETH value using current Oracle exchange rate |
| vETH balance | `balanceOf(address)` | `0x70a08231` | Get vETH token balance of a specific address |
| Max redeemable | `maxRedeem(address)` | `0xd905777e` | Maximum vETH shares the owner can redeem in a single tx |
| Claimable ETH | `canWithdrawalAmount(address)` | `0x52a630b9` | Returns `(totalAvailableAmount, pendingDeleteIndex, pendingDeleteAmount)`. First value = ETH ready to claim |

## How to Call

**Read queries** — use `eth_call` (no gas):

```bash
# Method A: cast (preferred)
cast call <VETH_CONTRACT> \
  "<FUNCTION_SIGNATURE>(<ARG_TYPES>)(<RETURN_TYPES>)" <ARGS> \
  --rpc-url <RPC_URL>

# Method B: curl (if cast unavailable)
curl -s -X POST <RPC_URL> \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"<VETH_CONTRACT>","data":"<SELECTOR><ENCODED_ARGS>"},"latest"]}'
```

If `previewDeposit` or `previewRedeem` fails, fall back to `convertToShares` / `convertToAssets` (same encoding).

**Write transactions** — use `cast send` (requires wallet):

```bash
# Mint vETH (stake native ETH)
cast send <VETH_CONTRACT> \
  "depositWithETH()" --value <AMOUNT_IN_WEI> \
  --rpc-url <RPC_URL> --private-key <PRIVATE_KEY>

# Redeem vETH (unstake)
cast send <VETH_CONTRACT> \
  "redeem(uint256,address,address)" <SHARES_IN_WEI> <USER_ADDR> <USER_ADDR> \
  --rpc-url <RPC_URL> --private-key <PRIVATE_KEY>

# Claim ETH (withdraw completed redemptions)
cast send <VETH_CONTRACT> \
  "withdrawCompleteToETH()" \
  --rpc-url <RPC_URL> --private-key <PRIVATE_KEY>
```

### Calldata Encoding (for manual signing output)

- **uint256**: convert wei to hex, left-pad to 64 chars
- **address**: remove 0x prefix, left-pad to 64 chars
- `canWithdrawalAmount` returns 3 × uint256 (192 hex chars): `(totalAvailableAmount, pendingDeleteIndex, pendingDeleteAmount)`. First 64 chars = claimable ETH amount

## API 1: Mint vETH (Stake ETH)

### Pre-Execution

1. Query rate: `previewDeposit(amount)` → expected vETH
2. Check wallet: `BIFROST_PRIVATE_KEY` env var or Foundry keystore `bifrost-agent`
3. Display preview and wait for CONFIRM

### Transaction

| Field | Value |
|-------|-------|
| To | `<VETH_CONTRACT>` |
| Value | User's ETH amount in wei |
| Data | `0x1166dab6` |
| ChainId | Per selected chain |

### Manual Signing Output

```
To:       <VETH_CONTRACT>
Value:    {wei} ({amount} ETH)
Data:     0x1166dab6
ChainId:  {chainId}
```

## API 2: Redeem vETH (Unstake)

### Pre-Execution

1. Check `balanceOf(user)` ≥ redeem amount
2. Query `previewRedeem(shares)` → expected ETH
3. Check `maxRedeem(user)`
4. Display preview (warn: ETH enters queue, NOT instant) and wait for CONFIRM

### Transaction

| Field | Value |
|-------|-------|
| To | `<VETH_CONTRACT>` |
| Value | `0` |
| Data | ABI-encoded `redeem(shares, userAddr, userAddr)` |
| ChainId | Per selected chain |

Encode calldata: `cast calldata "redeem(uint256,address,address)" <SHARES> <ADDR> <ADDR>`

## API 3: Claim Redeemed ETH

### Pre-Execution

1. Check `canWithdrawalAmount(user)` — first return value = claimable amount
2. If 0: inform user redemption may still be processing
3. If > 0: display claimable amount and wait for CONFIRM

### Transaction

| Field | Value |
|-------|-------|
| To | `<VETH_CONTRACT>` |
| Value | `0` |
| Data | `0x3ec549e9` |
| ChainId | Per selected chain |

## Agent Behavior

1. **Environment check**: on first interaction, ask user if they want to configure `BIFROST_CHAIN`, `BIFROST_RPC_URL`, or `BIFROST_PRIVATE_KEY`. If not, use Ethereum Mainnet defaults with manual signing mode
2. **RPC selection**: use `BIFROST_RPC_URL` if set; otherwise use per-chain default RPC. Fall back to per-chain fallback RPC on failure
3. **Multi-chain awareness**: when user specifies a chain (e.g. "on Base", "on Arbitrum"), switch to that chain's RPC, WETH address, and chainId accordingly
4. **Wallet detection**: check `BIFROST_PRIVATE_KEY` env var or Foundry keystore `bifrost-agent`. If found, ask user whether to use it. If not, output tx data for manual signing
5. **CONFIRM required**: display transaction preview (amount, rate, expected output, chain) and require user to type **CONFIRM** before any write
6. **Private key import requires CONFIRM**: show security warning first, require CONFIRM before accepting key
7. **Key retention is user-controlled**: after tx, ask user whether to keep or delete the key
8. **Balance pre-check**: verify sufficient ETH/vETH before building tx
9. **Prefer cast, fall back to curl**: use pre-computed calldata from selector table if cast fails
10. **No credential display**: never echo private keys; truncate addresses (first 6 + last 4)
11. **Post-completion tip**: if no wallet configured, suggest "set up wallet" after operation
12. After successful tx, provide block explorer link: `https://etherscan.io/tx/{hash}` (Ethereum), `https://basescan.org/tx/{hash}` (Base), `https://optimistic.etherscan.io/tx/{hash}` (Optimism), `https://arbiscan.io/tx/{hash}` (Arbitrum)
13. **Useful links**: direct users to [Bifrost vETH page](https://www.bifrost.io/vtoken/veth) or [Bifrost App](https://app.bifrost.io/vstaking/vETH) when relevant

## Security

1. Private keys are opt-in only — default outputs unsigned tx data
2. Explicit CONFIRM for every write operation
3. Validate amounts against balance and protocol limits
4. Recommend dedicated wallet with limited funds for agent-side signing

## Error Handling

| Error | User Message |
|-------|-------------|
| `EthNotSent()` (0x8689d991) | "No ETH included. Please specify the amount." |
| `EthTransferFailed()` | "ETH transfer failed. Try claiming as WETH with withdrawComplete()." |
| `ZeroWithdrawAmount()` (0xd6d9e665) | "No claimable ETH. Your redemption may still be processing." |
| `ERC4626ExceededMaxRedeem` (0xb94abeec) | "Redeem exceeds your maximum. Check balance." |
| `Pausable: paused` | "VETH contract is paused. Try again later." |
| Insufficient ETH | "Insufficient ETH. Balance: {bal}, Needed: {amount + gas}." |
| Insufficient vETH | "Insufficient vETH. Balance: {bal}, Requested: {amount}." |
| Max withdraw count exceeded | "Too many pending redemptions. Claim existing ones first." |
| RPC failure | "Unable to connect. Retrying with backup endpoint..." |

## Notes

1. `depositWithETH()` wraps ETH → WETH internally via `WETH.deposit()`. No ERC-20 approval needed. For direct WETH deposits, use `deposit(uint256,address)` instead (requires WETH approval)
2. `withdrawCompleteToETH()` internally calls `withdrawCompleteTo(address(this))` to receive WETH, then unwraps to ETH via `WETH.withdraw()`, then sends ETH to caller. If ETH transfer fails, use `withdrawComplete()` to receive WETH instead
3. Redemption is NOT instant — `redeem()` / `withdraw()` add entries to the withdrawal queue, processed in batches via Bifrost cross-chain mechanism
4. All write functions are protected by `whenNotPaused` and `nonReentrant` (ReentrancyGuardUpgradeable)
5. Gas estimates are approximate; use `cast estimate` for accuracy
