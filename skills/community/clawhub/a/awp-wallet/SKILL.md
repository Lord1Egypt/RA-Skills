---
name: awp-wallet
description: >
  Use when the user says "send ETH/USDC to 0x...", "check my balance",
  "how much do I have", "approve token spending", "sign this message",
  "estimate gas", "what's my wallet address", or needs any crypto
  transfer, balance check, token approval, or on-chain signing.
  400+ EVM chains, auto-gasless.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - git
        - openssl
      anyBins:
        - npm
    emoji: "\U0001F4B0"
    homepage: https://github.com/awp-core/awp-wallet
    install:
      - kind: node
        package: awp-wallet
        bins: [awp-wallet]
---

# AWP Wallet

EVM wallet for AI agents. All commands output JSON. No password needed — encryption is auto-managed.

## Step 1 — Ensure Installed

```bash
awp-wallet --version 2>/dev/null || {
  git clone https://github.com/awp-core/awp-wallet.git /tmp/awp-wallet &&
  cd /tmp/awp-wallet && bash install.sh
}
```

If `awp-wallet: command not found` persists after install, run:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Step 2 — Ensure Wallet Exists

```bash
awp-wallet receive 2>/dev/null || awp-wallet init
```

When creating a new wallet, tell the user: `[WALLET] created new wallet: 0x...`

## Step 3 — Unlock Session

Every operation that reads or writes on-chain needs a session token.

```bash
TOKEN=$(awp-wallet unlock --duration 3600 | jq -r '.sessionToken')
```

If you get `Invalid or expired session`, re-run this step.

## Step 4 — Execute the User's Request

Pick the right command based on what the user asked. `$T` = the session token from Step 3.

### "Check my balance" / "How much do I have"
```bash
awp-wallet balance --token $T --chain ethereum
awp-wallet balance --token $T --chain base --asset usdc
awp-wallet portfolio --token $T                          # all chains overview
```

### "Send X to 0x..."
Before sending, confirm with the user:
```
[TX] about to send:
     to:      0xBob...1234
     amount:  50 USDC
     chain:   Base
     proceed? (y/n)
```
Then:
```bash
awp-wallet send --token $T --to 0xAddr --amount 0.1 --chain ethereum
awp-wallet send --token $T --to 0xAddr --amount 100 --asset usdc --chain base
```

### "What's my address" / "Where do I receive"
```bash
awp-wallet receive
```
No session token needed.

### "Approve spending" / "Revoke approval"
```bash
awp-wallet approve --token $T --asset usdc --spender 0xRouter --amount 1000 --chain base
awp-wallet revoke  --token $T --asset usdc --spender 0xRouter --chain base
```

### "Sign this message"
```bash
awp-wallet sign-message --token $T --message "Hello World"
awp-wallet sign-typed-data --token $T --data '{"types":{...},"primaryType":"...","domain":{...},"message":{...}}'
```

### "Estimate gas"
```bash
awp-wallet estimate --to 0xAddr --amount 0.1 --chain ethereum
```

### "Check transaction status"
```bash
awp-wallet tx-status --hash 0xHash --chain ethereum
```

### "Show history"
```bash
awp-wallet history --token $T --chain ethereum --limit 20
```

### "Send to multiple addresses"
```bash
awp-wallet batch --token $T --chain base \
  --ops '[{"to":"0xA","amount":"10","asset":"usdc"},{"to":"0xB","amount":"20","asset":"usdc"}]'
```

## Step 5 — Lock When Done

```bash
awp-wallet lock
```

## Choosing a Chain

`--chain` accepts a name or numeric ID. Default: `ethereum`.

Preconfigured: `ethereum` `base` `bsc` `arbitrum` `optimism` `polygon` `avalanche` `fantom` `zksync` `linea` `scroll` `mantle` `blast` `celo` `sepolia` `base-sepolia`

Any EVM chain: `--chain 99999 --rpc-url https://custom.rpc.com`

If the user says "on Base" → `--chain base`. If they say "on BSC" or "BNB Chain" → `--chain bsc`. If no chain is mentioned, use `ethereum`.

## Choosing an Asset

`--asset` accepts a symbol or contract address. Omit for native currency (ETH, BNB, etc.).

Built-in: `usdc` `usdt` `awp` `weth` `wbnb` `dai`

Any token: `--asset 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

## Output Tags

Use these tags when presenting results to the user:

| Tag | When | Example |
|-----|------|---------|
| `[QUERY]` | Balance, gas estimates | `[QUERY] ETH balance: 1.5 ETH ($3,750)` |
| `[TX]` | After a transaction | `[TX] sent 50 USDC → 0xBob (hash: 0x...)` + explorer link |
| `[SIGN]` | After signing | `[SIGN] message signed: 0x...` |
| `[WALLET]` | Wallet info | `[WALLET] address: 0x...` |

## Error Recovery

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found` | Not installed | Step 1 |
| `No wallet found` | No wallet yet | `awp-wallet init` |
| `Invalid or expired session` | Token expired | Re-run Step 3 |
| `Insufficient balance` | Not enough funds | Tell user; suggest `--mode gasless` if no native gas |
| `Daily limit exceeded` | Safety limit hit | Tell user to try again in 24h |

## Advanced (rarely needed)

```bash
awp-wallet chains                                       # list all chains
awp-wallet chain-info --chain zksync                    # chain details
awp-wallet wallets                                      # list wallet profiles
awp-wallet wallet-id                                    # current profile ID
awp-wallet status --token $T                            # session info
awp-wallet allowances --token $T --asset usdc --spender 0xRouter --chain base
awp-wallet verify-log                                   # audit log integrity
awp-wallet upgrade-7702 --token $T --chain ethereum     # EIP-7702 upgrade
awp-wallet revoke-7702 --token $T --chain ethereum      # revoke EIP-7702
awp-wallet deploy-4337 --token $T --chain ethereum      # smart account status
```

## Environment Variables (all optional)

| Variable | Purpose |
|----------|---------|
| `WALLET_PASSWORD` | Explicit password (default: auto-managed). Required for `export` and `change-password`. |
| `PIMLICO_API_KEY` | Enable gasless ERC-4337 transactions |
| `AWP_AGENT_ID` | Multi-agent wallet isolation |
| `AWP_SESSION_ID` | Per-session wallet isolation |

Gasless mode auto-activates when the wallet has no native gas and `PIMLICO_API_KEY` is set. Force with `--mode gasless`.
