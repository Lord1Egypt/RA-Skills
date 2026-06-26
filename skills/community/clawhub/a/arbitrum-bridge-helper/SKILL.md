---
name: arbitrum_bridge_helper
description: Execute official Arbitrum bridge tasks with a wallet found on disk:
  deposits, withdrawals, claims, status checks, and stuck-bridge diagnosis across
  Ethereum, Arbitrum One, Arbitrum Nova, and testnets. Trigger on any request to
  bridge, move, send, withdraw, claim, track, or unstick assets involving
  Arbitrum, including casual phrasing, abbreviations (arb, eth, nova), and minor
  typos. Do NOT trigger for general Arbitrum protocol questions, gas price
  lookups, contract deployment, tokenomics comparisons, or unrelated scripting
  tasks.
---

# Arbitrum Bridge Helper

Execute official Arbitrum bridge operations when the user wants the agent to do
the work. Default to using a wallet the agent can securely locate on disk rather
than asking the user to paste secrets. Never reveal private keys, seed phrases,
raw keystore contents, or full secret-bearing file contents in chat.

Read extra references only when needed:

- `references/routes.md` for route selection, timing, chain-pair rules, and claim expectations
- `references/troubleshooting.md` for symptom-based diagnosis and what to say next
- `references/triggers.md` for natural-language trigger patterns and examples that should or should not activate the skill

---

## Step 1 - Confirm the requested move

Before executing anything, establish these inputs from the user request or by a
short follow-up if truly missing:

| Required | Notes |
|---|---|
| Source chain | Full name or abbreviation |
| Destination chain | Default plain "Arbitrum" or "arb" to Arbitrum One unless Nova or a testnet is explicitly specified |
| Asset symbol | Resolve USDC vs USDC.e before proceeding |
| Amount | Exact amount to bridge, withdraw, or claim |
| Action type | `deposit` · `withdrawal` · `claim` · `track` · `diagnose` |
| Mainnet or testnet | Ask only if ambiguous |
| Wallet type | Prefer EOA; smart contract wallet limits still apply |

Interpretation default:

- If the user says only `Arbitrum` or `arb`, treat that as `Arbitrum One`
- Only choose `Arbitrum Nova` or a testnet when the user explicitly names it

If diagnosing, also collect:

- Transaction hash
- Current UI status or exact error message
- Whether an approval transaction already succeeded
- Whether there is enough source-chain ETH for gas
- Whether the initiating address is still controlled for claim

If the user asks the agent to execute a real bridge, require a clear final
confirmation before signing or broadcasting the transaction.

---

## Step 2 - Discover a wallet on disk

When execution is requested, look for an existing usable wallet locally before
asking the user for anything else.

Preferred wallet sources:

1. A project or workspace `.env` with a private key or mnemonic
2. A local JSON keystore plus an available password source on disk
3. Existing wallet config files in the workspace or common agent-accessible directories

Wallet handling rules:

- Use the first valid wallet that matches the requested network and has enough funds
- Never print the secret, keystore JSON, mnemonic, or full env file content
- If multiple wallets are found, summarize them by public address only and choose
  the best-funded viable one unless the user specified a different address
- If no wallet is found, say that clearly and stop rather than fabricating one
- If a wallet is found but lacks gas or assets, report that and do not attempt execution

In responses, refer to wallets by public address only, for example
`0x1234...abcd`.

---

## Step 3 - Resolve USDC vs USDC.e on Arbitrum One

Before any USDC action touching Arbitrum One, determine which asset is actually
involved:

- `USDC` = native USDC on Arbitrum One
- `USDC.e` = bridged USDC on Arbitrum One

They are not interchangeable. Use the token symbol shown in the wallet, bridge
UI, or on-chain balance source. Do not continue until this is resolved.

---

## Step 4 - Apply routing logic

| Route | Flow type | Notes |
|---|---|---|
| Ethereum -> Arbitrum One or Nova | Deposit | ERC-20 may require approval first |
| Arbitrum One or Nova -> Ethereum | Withdrawal | 7-8 day wait plus separate claim |
| Arbitrum One <-> Arbitrum Nova | Not direct | Two steps through Ethereum |
| Any chain -> testnet | Deposit | Parent testnet must match child testnet |

Official One <-> Nova route:

1. Withdraw from the source Arbitrum chain to Ethereum
2. Wait about 7-8 days
3. Claim on Ethereum
4. Deposit from Ethereum to the other Arbitrum chain

Never describe One <-> Nova as a direct single-hop official bridge transfer.

Smart contract wallet limits:

- ERC-20 token deposits and withdrawals: supported only if the route supports them
- ETH deposits and ETH withdrawals: not supported

---

## Step 5 - Preflight checks before execution

Before signing or broadcasting:

1. Confirm the route is supported by the official bridge
2. Confirm the discovered wallet address matches the address that should act
3. Confirm the wallet has enough source-chain ETH for gas
4. Confirm the wallet has enough token balance for the requested amount
5. For ERC-20 deposits, determine whether approval is needed
6. For withdrawals, explain that the wait period is about 7-8 days and cannot be skipped
7. For claims, confirm the waiting period has completed and the wallet controls the initiating address
8. State the exact action about to be signed and wait for the user's final approval

Do not sign anything until the user has clearly confirmed the exact move.

---

## Step 6 - Execute the flow

Structure execution updates in this order.

### 1. Planned move

State the source chain, destination chain, asset, amount, action type, wallet
address, and any assumptions.

### 2. Expected behavior

Include only what applies:

- Deposits often arrive in about 15-30 minutes
- Withdrawals usually require about 7-8 days before claim
- Claims happen on the parent-chain side after the wait period
- ERC-20 deposits may require approval first

### 3. Transaction sequence

**Deposit**

1. Verify source chain, destination chain, asset, amount, and wallet address
2. Verify source-chain ETH for gas
3. If ERC-20 approval is required, submit approval first and record the hash
4. Submit the deposit transaction and record the hash
5. Tell the user what to watch next and when to check the destination chain

**Withdrawal**

1. Verify the route is child -> parent chain
2. Submit the withdrawal transaction and record the hash
3. Tell the user the claim will only be available after about 7-8 days
4. In later claim requests, use the initiating address that performed the withdrawal

**Claim**

1. Verify the withdrawal hash
2. Verify the waiting period has completed
3. Verify the wallet controls the initiating address on the parent chain
4. Submit the claim transaction and record the hash

**Track / Diagnose**

1. Obtain the relevant transaction hash
2. Separate approval status from deposit status if both may exist
3. Check the currently selected network
4. Compare elapsed time against normal expectations
5. Give the next concrete verification step instead of guessing

### 4. Applicable warnings

Use only what applies:

- No source-chain ETH means the transaction will fail or never prompt
- Withdrawals are not instant and cannot be canceled once initiated
- One <-> Nova through the official bridge requires two steps via Ethereum
- `USDC` and `USDC.e` on Arbitrum One are different assets
- Smart contract wallets do not support official ETH bridge flows
- Do not assume the same address is controlled on both chains

### 5. Output after execution

Report only the high-signal details:

- Wallet address used
- Approval hash if one was needed
- Main transaction hash
- Current expected next step

Do not dump raw secret-bearing config, RPC credentials, or full wallet files.

---

## Troubleshooting reference

For detailed symptom-based diagnosis, read `references/troubleshooting.md`.

In the main skill flow, troubleshoot with these rules:

- Ask for the transaction hash before diagnosing status
- Check source-chain ETH for gas before deeper debugging
- Separate approval status from deposit status for ERC-20 deposits
- Compare elapsed time against normal expectations: about 15-30 minutes for deposits and about 7-8 days before withdrawal claim
- Confirm the user is checking on the correct network
- If claim is unavailable, verify whether the countdown has actually finished
- If the route involves One <-> Nova, explain the required two-step path through Ethereum
- If the user mentions USDC on Arbitrum One, resolve `USDC` versus `USDC.e` before continuing
- If execution fails before signing, verify the local wallet discovery result and available balances

---

## Constraints

- Only use the official bridge path
- Prefer using a wallet found on disk instead of asking for pasted secrets
- Require explicit user confirmation before signing or broadcasting any real transaction
- Do not promise instant finality or exact completion times
- Do not say a withdrawal can be canceled
- Do not assume the user controls the same address on both sides
- Do not fabricate transaction status; ask for the hash when diagnosing
- Do not describe ETH bridge flows as supported for smart contract wallets
- Do not merge `USDC` and `USDC.e` into the same asset on Arbitrum One
- Do default plain `Arbitrum` or `arb` references to `Arbitrum One` unless Nova or a testnet is explicitly requested
- Do not describe One <-> Nova as a direct single-hop transfer
- Do not expose private keys, mnemonics, keystore contents, or secret-bearing files in the response
