---
name: elytro-defi
description: Coordinate Elytro ERC-4337 smart accounts with DeFi planners (e.g., Uniswap AI) to quote, build, simulate, and execute calldata or UserOperations safely.
user-invocable: true
disable-model-invocation: false
required-skills: ["elytro"]
allowed-tools:
  - "Bash(elytro account*)"
  - "Bash(elytro query*)"
  - "Bash(elytro tx build*)"
  - "Bash(elytro tx simulate*)"
  - "Bash(elytro tx send*)"
related-skills: ["defi", "defi/uniswap", "elytro"]
---

# Coordinate Elytro With DeFi Planners

Use this skill when a protocol-specific planner (e.g., `defi/uniswap`) provides swap/liquidity/lending instructions that must be executed from an Elytro smart account. Elytro signs and submits the tx/UserOp; the planner supplies calldata, route, and slippage details.

## Prerequisites

1. **Wallet ready** – Follow the `elytro` skill to run `elytro init`, create/activate the target account, and fund it with required assets plus gas if sponsorship is disabled.
2. **Planner context** – Load the protocol-specific skill (Uniswap AI or similar). Share balances, chain, and account alias so it can craft calldata/UserOps against the correct router and chain ID.
3. **Environment** – Export Elytro env vars (`ELYTRO_ENV`, Pimlico key, RPC overrides) in the same shell session that runs the commands below.
4. **Secure temp files** – Store planner output in temporary files or shell variables (`CALLDATA`, `USEROP_JSON`). Never commit Elytro vault data or planner secrets.

## Workflow

### 1. Gather context for the planner

```bash
elytro account list
elytro query balance <alias> [--token <erc20>]
elytro query tokens <alias>
```

Share the alias/address, chain ID, native/token balances, and any gas sponsorship preferences with the planner so it can size the trade and pick pools.

### 2. Obtain calldata or UserOp from the planner

Ask the planner for one of two artifacts:

| Artifact | When to Request | Contents |
| --- | --- | --- |
| **Calldata bundle** | Most swaps, liquidity adds/removes, lending interactions | Router/contract address, calldata hex, ETH value (if payable), recommended chain ID |
| **UserOperation JSON** | When the planner already built an ERC‑4337 UserOp (paymasters, batching logic, etc.) | Complete `userOperation` structure ready for signing |

Always confirm the planner output references your Elytro account address and target chain.

### 3. Simulate before sending

#### Calldata path

```bash
ACCOUNT=demo-arb
CHAIN=42161
ROUTER=0xE592427A0AEce92De3Edee1F18E0157C05861564
CALLDATA=0x472b43f3...
VALUE_ETH=0

elytro tx simulate "$ACCOUNT" \
  --chain "$CHAIN" \
  --tx "to:$ROUTER,value:$VALUE_ETH,data:$CALLDATA"
```

Review the output for:

- `Type`, selector, and calldata size (should match planner summary)
- Sponsorship status (`Sponsored: Yes/No`)
- Balance warnings (insufficient ERC-20 or native ETH)
- Gas limits and estimated max cost

#### UserOperation path

```bash
USEROP_JSON=$(cat userop.json)
elytro tx simulate "$ACCOUNT" --userop "$USEROP_JSON"
```

Simulation ensures gas limits and paymaster fields are valid before signing.

### 4. Execute the action

- **Calldata** – Repeat the same spec with `tx send`. Add `--no-sponsor` if you must force self-paid gas.

  ```bash
  elytro tx send "$ACCOUNT" \
    --chain "$CHAIN" \
    --tx "to:$ROUTER,value:$VALUE_ETH,data:$CALLDATA"
  ```

- **UserOperation** – Sign and relay the planner’s JSON verbatim (Elytro will not overwrite paymaster data).

  ```bash
  elytro tx send "$ACCOUNT" --userop "$USEROP_JSON"
  ```

Record the printed bundler hash and eventual transaction hash for auditing.

### 5. Verify results

After inclusion, confirm balances or positions changed as expected:

```bash
elytro query balance "$ACCOUNT" --token <erc20>
elytro query tokens "$ACCOUNT"
```

Share proofs back with the planner or user if required.

## Input Validation & Safety

- **Addresses** – Must match `^0x[0-9a-fA-F]{40}$`. Reject any value with shell metacharacters.
- **Chain IDs** – Accept numeric IDs only (e.g., `42161`). Never pass unchecked strings into `--chain`.
- **Calldata** – Enforce `^0x[0-9a-fA-F]+$` and even length. Reject planner output that does not include `0x`.
- **Value** – Must be numeric (`^\d+(\.\d+)?$`). Convert planner-supplied wei using `--tx "value:<ETH>"`.
- **UserOp JSON** – Keep in a single-quoted shell string or file to avoid interpolation. Optionally validate with `jq`.

Do not execute planner instructions that involve unknown contracts, self-modifying code, or unreviewed paymasters without human approval.

## Examples

```bash
# Swap 100 USDC -> ETH on Arbitrum with calldata from Uniswap AI
CALLDATA=0x3593564c...
elytro tx simulate demo-arb \
  --chain 42161 \
  --tx "to:0xE592427A0AEce92De3Edee1F18E0157C05861564,value:0,data:$CALLDATA"
elytro tx send demo-arb \
  --chain 42161 \
  --tx "to:0xE592427A0AEce92De3Edee1F18E0157C05861564,value:0,data:$CALLDATA"

# Execute a planner-supplied UserOp (already sponsored)
elytro tx simulate demo-mainnet --userop "$(cat swap-userop.json)"
elytro tx send demo-mainnet --userop "$(cat swap-userop.json)"
```

If anything fails, rerun `elytro tx simulate` to inspect the error, then coordinate with the planner to adjust calldata, slippage, or paymaster settings.
