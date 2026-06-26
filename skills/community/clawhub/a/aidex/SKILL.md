---
name: aidex
description: Swap tokens on Ethereum via the AIDEX aggregator. Search tokens, check exchange rates, view balances, and execute swaps. Client-side transaction signing keeps your private key on your machine.
version: 1.0.7
homepage: https://ai-dex.io/
user-invocable: true
emoji: "\U0001F504"
metadata: {
  "openclaw": {
    "requires": {
      "bins": ["node"]
    },
    "primaryEnv": "AIDEX_PRIVATE_KEY"
  }
}
---

## Overview

AIDEX is a high-performance DEX aggregator on Ethereum. This skill gives your OpenClaw agent the ability to swap tokens, check exchange rates, monitor balances, and verify transaction results.

AIDEX provides tools, not decisions. You decide when and what to trade. AIDEX is your hands — fast, transparent, reliable. Every operation is a visible on-chain Ethereum transaction that you can verify on Etherscan. Nothing is hidden, nothing is obscured.

AIDEX doesn't pretend to be smarter than you. It doesn't make decisions on your behalf. It does exactly what you ask — honestly, quickly, and verifiably. If you want to experiment with automated trading, AIDEX gives you the simplest, most transparent foundation to build on.

Your funds stay in your wallet at all times. Unlike centralized exchange integrations where your money sits on someone else's platform, AIDEX works with decentralized liquidity pools. You remain in full control.

## Source code

Open source on GitHub: [AIDEX-DeFi/skills](https://github.com/AIDEX-DeFi/skills). Issues and pull requests welcome.

## Why AIDEX

- **Simplicity** — Simple, clear scripts. Clear inputs, clear outputs. The agent calls them, you see the results. That's it.
- **Transparency** — Every swap is a standard Ethereum transaction. You get a transaction hash. You can check it on Etherscan. What you asked for is what gets executed.
- **Security** — Your private key never leaves your machine. The API only receives already-signed transactions. Even if our servers were compromised, no one could alter your transaction — it's cryptographically signed by you. See the [Security Model](#security-model) section below.
- **Speed** — Lightning-fast execution layer with minimal latency. Transactions are built and sent in milliseconds.
- **Best rates** — Wide liquidity pool coverage finds exchange routes that competitors miss, giving you better rates.

## Dependencies

This skill requires Node.js packages listed in `package.json` in the skill's root folder:

- **ethers** — Ethereum library for client-side transaction signing. This is what keeps your private key safe — transactions are signed locally, never sent to the API.
- **@napi-rs/keyring** *(optional)* — Native access to the operating system's credential manager (Windows Credential Manager, macOS Keychain, Linux Secret Service). Allows storing the private key securely instead of an environment variable.

**Run `npm install` in the skill's root folder after the initial install and after each skill update.** Skill updates may pin new dependency versions. The packages are installed locally into the skill's own `node_modules/` folder — this is NOT a modification to the user's system environment. It is a standard, reversible operation (the folder can be deleted at any time).

If your operational constraints prevent you from running `npm install` automatically, ask the user for permission and let them decide.

**Do not report the skill as broken if dependencies are missing — install them.**

## Security Model

### Client-side transaction signing

All transaction signing happens locally on your machine using ethers.js. The AIDEX API **never receives, requests, or has access to your private key**.

Here's what happens during a swap:

1. Your agent calls the AIDEX API with swap parameters (which tokens, how much)
2. The API returns a **complete unsigned transaction** (destination address, call data, gas parameters)
3. The `swap.js` script signs this transaction using your private key via `ethers.Wallet.signTransaction()`
4. Finally, the signed transaction is sent back to the API for fast broadcasting to the Ethereum network

### What the API cannot do

Your funds are protected because every transaction must be reviewed and signed directly by your wallet. AIDEX cannot modify transaction amounts, tokens, or recipients, and cannot initiate unauthorized transactions.

### What AIDEX API does NOT do

- Does not store private keys
- Does not manage or custody your funds
- Does not deduct fees from your wallet
- Does not have any access to your assets beyond what you explicitly sign

### Private key storage — a reasonable trade-off

Your private key can be stored in the `AIDEX_PRIVATE_KEY` environment variable or in the operating system's credential manager (system keyring). Both approaches keep the key local to your machine. See the [Setup](#setup) section for configuration details.

This is a deliberate and reasonable trade-off between autonomy and security: if the agent cannot sign transactions, it cannot trade autonomously.

## Setup

The AIDEX skill works out of the box for read-only operations: searching tokens, checking exchange rates, and viewing balances. No configuration needed.

To execute swaps, configure your private key using one of the options below.

### What is a Private Key?

A private key is 64 hexadecimal characters (`0-9`, `a-f`), optionally prefixed with `0x` — 64 or 66 characters total. It is the sole credential that authorizes transactions from your Ethereum wallet. Unlike a password, a private key cannot be reset or recovered — if it is lost or compromised, access to the wallet's funds is permanently lost or stolen.

If you don't have a wallet yet, the easiest way to get started is with [MetaMask](https://metamask.io/):

1. Install the MetaMask browser extension and create a new wallet
2. Open MetaMask, click the account selector at the top of the screen
3. Tap the account menu (⋮) next to the account name, then select **Account details**
4. Select **Private keys**, enter your MetaMask password, and copy the revealed key

Use this key in one of the configuration options below.

### Option A: Environment variable (via OpenClaw)

**Simple — for testing only.** The private key is passed as a command-line argument and may end up in shell history, process list, and audit logs:

```bash
openclaw config set skills.entries.aidex.env.AIDEX_PRIVATE_KEY "0xYourPrivateKeyHere"
```

**Secure — requires bash (on Windows use WSL).** The key is read interactively into a shell variable and piped via stdin, never appearing in argv:

```bash
read -rsp "AIDEX private key: " k; echo; printf '{"skills":{"entries":{"aidex":{"env":{"AIDEX_PRIVATE_KEY":"%s"}}}}}' "$k" | openclaw config patch --stdin; unset k
```

After changing the config, restart the gateway so the new value takes effect:

```bash
openclaw gateway restart
```

### Option B: System keyring (desktop only)

> **Not available in Docker, WSL, CI, or headless Linux.** The system keyring requires a desktop session. If you are running in a containerized or headless environment, use Option A above.

Store your private key in the operating system's credential manager. The key is encrypted at rest and protected by your OS user account, keeping it out of configuration files and environment variable logs.

**Windows** (Credential Manager):

```cmd
cmdkey /generic:AIDEX_PRIVATE_KEY.aidex /user:AIDEX_PRIVATE_KEY
```

**macOS** (Keychain):

```bash
security add-generic-password -s aidex -a AIDEX_PRIVATE_KEY -U -w
```

**Linux** (Secret Service — GNOME Keyring, KWallet):

```bash
secret-tool store --label="AIDEX Private Key" service aidex username AIDEX_PRIVATE_KEY target default
```

In all three commands above, you will be prompted to enter the private key interactively.

**Headless and containerized environments (Docker, WSL, CI):**

The system keyring is not accessible from containers or headless environments — it requires a desktop session with D-Bus. In these environments, use Option A (environment variable). For production server deployments, proper firewall configuration is essential to restrict access to the machine running the agent.

If both an environment variable and a keyring entry are present, the environment variable takes priority.

## Token identification

In all scripts that accept token parameters (`--token-in`, `--token-out`, `--tokens`), you can specify tokens by **address** or by **symbol**:

- By address: `--token-in 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- By symbol: `--token-in USDC`

If a symbol is ambiguous (matches multiple tokens), the API will return an error listing all matches so you can specify the address instead.

## Scripts

> **Note:** You don't need to read this section to use AIDEX for trading. Your OpenClaw agent handles the scripts automatically. This section is for developers or anyone who wants to understand how the system works under the hood.

All scripts output JSON to stdout. Every response contains a `success` field (`true` or `false`). On failure, an `error` field explains what went wrong.

### account.js — Get wallet address *(requires private key)*

Derives your wallet address from the private key. Does not call the API.

```bash
node {baseDir}/scripts/account.js
```

Output: `{"success": true, "address": "0x..."}`

### tokens.js — Search tokens

Search for tokens by symbol, name, or address.

```bash
node {baseDir}/scripts/tokens.js --term USDC
```

Without `--term`, returns the full token list.

Output: `{"success": true, "tokens": [{"address": "0x...", "symbol": "USDC", "decimals": 6, "name": "USD Coin", "imageUrl": "..."}]}`

### rate.js — Check exchange rate

Get the current exchange rate for a token pair. Read-only, does not execute anything. Tokens can be specified by address or symbol.

```bash
node {baseDir}/scripts/rate.js --token-in ETH --token-out USDC --amount-in 0.5
```

Output: `{"success": true, "rate": "3125.50", "amountOut": "1562.75", "estimatedGasPriceUsd": 2.34}`

### balance.js — Check token balances

Get balances for up to 9 tokens at once. Use `ETH` or the zero address (`0x0000000000000000000000000000000000000000`) for native ETH balance. Tokens can be specified by address or symbol.

> **Note:** `--address` is required, but you often don't need to ask the user for it. Run `account.js` first — if the private key is configured, it returns the wallet address. Only ask the user for their address if `account.js` returns an error (private key not configured).

```bash
node {baseDir}/scripts/balance.js --address 0xYourWallet --tokens ETH,USDC
```

Output: `{"success": true, "balances": [{"address": "0x000...0", "symbol": "ETH", "balance": "1.5", "allowance": null}, {"address": "0xA0b...eB48", "symbol": "USDC", "balance": "3250.00", "allowance": "1000.0"}]}`

The `allowance` field shows how much the AIDEX router is approved to spend on behalf of the wallet (relevant for ERC-20 tokens). For native ETH, `allowance` is `null`.

### swap.js — Execute a swap *(requires private key)*

Builds a chain of transactions (approve if needed + swap) via API, signs them locally on your machine, and broadcasts them. Full cycle in one call. The API handles approve automatically — the script doesn't need to know about it. Tokens can be specified by address or symbol.

```bash
node {baseDir}/scripts/swap.js --token-in ETH --token-out USDC --amount-in 0.5 --slippage 0.5 --deadline-minutes 20
```

- `--slippage` — Maximum acceptable slippage in percent (default: 0.5)
- `--deadline-minutes` — Transaction deadline in minutes from now (default: 20)

Output: `{"success": true, "transactionHashes": ["0x..."], "fromAddress": "0x...", "amountOut": "1562.75", "estimatedGasPriceUsd": 2.34}`

Note: `transactionHashes` is an array — it may contain 1-3 hashes (approve transactions + swap). Pass all of them to swap-status.js.

### swap-status.js — Check swap operation status

Verify the result of a swap operation (including approve steps). Accepts 1-3 transaction hashes.

```bash
node {baseDir}/scripts/swap-status.js --hashes 0xApproveHash,0xSwapHash
```

Output:
```json
{
  "success": true,
  "status": "completed",
  "steps": [
    {"type": "approve", "status": "confirmed", "transactionHash": "0x..."},
    {"type": "swap", "status": "confirmed", "transactionHash": "0x...", "amountIn": "0.5", "tokenIn": "ETH", "amountOut": "1562.75", "tokenOut": "USDC"}
  ]
}
```

High-level status: `pending` (waiting for confirmation), `completed` (all steps confirmed), `failed` (a step reverted).

## Workflow Patterns

### Check exchange rate

```
1. rate.js --token-in ETH --token-out USDC --amount-in 1
```

### Execute a swap

```
1. account.js                                              → get wallet address
2. rate.js --token-in ETH --token-out USDC --amount-in 0.5 → show rate and gas cost to user
3. [Ask user for confirmation]
4. balance.js --address <wallet> --tokens ETH,USDC          → show balances and allowance
5. swap.js --token-in ETH --token-out USDC --amount-in 0.5  → execute (approve + swap if needed)
6. swap-status.js --hashes <hash1>,<hash2>                  → verify result
7. balance.js --address <wallet> --tokens ETH,USDC          → show balances after
```

### Price monitoring with auto-swap (via OpenClaw cron/heartbeat)

```
1. rate.js --token-in ETH --token-out USDC --amount-in 0.5  → check current rate
2. If target rate reached:
   a. swap.js --token-in ETH --token-out USDC --amount-in 0.5  → execute swap
   b. swap-status.js --hashes <hashes>                          → verify result
   c. balance.js ...                                            → show final balances
3. If not reached: wait for next cron tick
```

When using cron-based monitoring and the API returns a temporary error ("AIDEX is temporarily unavailable" or network error), simply skip this iteration and retry on the next tick. Do not treat temporary errors as final failures.

## Agent Rules

1. **Always show rate and gas cost** before executing a swap. The user must see what they're getting.
2. **Ask for explicit confirmation** before executing a swap — unless the user explicitly set up automatic execution (e.g., "swap every time the price drops below 2800"). Confirmation can be one-time or for a series, but the agent never invents retries on its own.
3. **Display amounts in human-readable format** (e.g., "0.5 ETH", "1,562.75 USDC"), not raw BigInt values.
4. **Always show transaction hashes** after a swap so the user can track them on Etherscan.
5. **Handle error responses gracefully**:
   - `Route not found` — Let the user know AIDEX could not find a route for this pair, and suggest trying a different pair or amount.
   - `AIDEX is temporarily unavailable` — Let the user know AIDEX is not available right now and suggest trying again in a few minutes.
   - The error says the skill is outdated (e.g., `Skill ... is outdated` or `Outdated skill version`) — Ask the user to run `openclaw skills update aidex` in their terminal.
   - `Request rejected` — Most likely the request was formed incorrectly — re-check the arguments. If they look correct, ask the user to update the skill: `openclaw skills update aidex`.
   - Network errors — Same as above, suggest retrying later.
   - Invalid token — Suggest searching for the token by name or symbol.
6. **After a swap, always call swap-status.js** to verify the actual result and show it to the user.
7. **Private key not configured?** If no private key is available, present **all** configuration options: environment variable (via `openclaw config set`) **and** system keyring. Do not default to a single option — let the user choose.
8. **NEVER loop or auto-retry on errors.** If any transaction reverts or the API returns an error, stop the current operation and report to the user. Do not automatically retry. If the user wants to try again, they will say so.
9. **NEVER access the private key directly.** Do not read openclaw.json, .env files, or any other configuration files to extract the private key. Do not pass the private key as a command-line argument — command-line arguments are visible to all processes on the system. Passing the key this way is equivalent to leaking it to an attacker. The key is resolved from the AIDEX_PRIVATE_KEY environment variable or the system keyring. If neither source provides a valid key, inform the user and stop. No workarounds.
10. **While a transaction is mining**, you can show the user a link to track it: `https://etherscan.io/tx/{transactionHash}`. This applies to all transactions (swap, approve).
11. **Detect the user's environment.** When helping with private key setup, adapt your suggestions to the user's environment. If the user is running in a containerized or headless Linux environment (Docker, WSL, CI), lead with the environment variable approach (Option A) — do not mention the system keyring unless the user explicitly asks about alternatives. If asked, explain that the system keyring is available for desktop operating systems (Windows, macOS, Linux with a graphical session) but is not accessible from containers or headless environments. For desktop users, present all keyring options but highlight the one matching their OS first.
12. **Never ask the user about private key configuration proactively.** Do not ask "is your private key configured?" or offer to help with setup when the user first interacts with the skill. The user may not even know what a private key is. Simply run the requested operation — if the key is needed and not configured, the script will return a clear error, and only then should you explain what happened and how to set it up. For read-only operations (rate, tokens, balances), the key is not needed at all — do not mention it.
13. **Do not assume the private key is missing — check by running the script.** When the user asks for their balance, wallet address, or any operation that may require a private key, do not refuse preemptively. Run `account.js` — if the key is configured, you'll get the wallet address. If not, the script will return a clear error explaining what to set up. This is a read-only operation with no cost and no risk. Never tell the user "I can't do this" without actually trying first.
14. **When asking for a wallet address, warn the user not to confuse it with a private key.** Both start with `0x`, but an address is 42 characters and is safe to share, while a private key is 66 characters and must be kept secret. If the user provides a 66-character string where an address is expected, **do not use it** — warn them immediately that this looks like a private key and should never be shared. Example: "Your wallet address (42 characters, starts with 0x — this is **not** your private key, which is longer and must be kept secret)."
15. **Never modify the skill's source code.** The scripts in `{baseDir}/scripts/` and `package.json` are canonical — do not edit, patch, or "fix" them under any circumstances, even temporarily. If a script returns an unexpected error and you suspect a bug in the skill, you are almost certainly wrong: re-check your own inputs and call sequence carefully, read the script specifications in this SKILL.md word-for-word, and use the exact command names and argument names documented there — never invent your own syntax.

## Key Constants

- Native ETH address: `0x0000000000000000000000000000000000000000`
- WETH address: `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`
- Network: Ethereum mainnet (chainId: 1)
- Common tokens: ETH (18 decimals), USDC (6), USDT (6), DAI (18), WBTC (8)
