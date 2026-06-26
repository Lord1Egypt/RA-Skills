# Elytro -- Agent cheat sheet

Fast lookup: what to run, what needs user consent, and how to phrase results.

CLI errors include `error.message`, `error.data.hint`, and `suggestion` fields. Follow those directly.

---

## Commands

### Account

| Run                                                                    | Tell the user                                                                                      |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `account create -c <chainId> [-a alias] [-e email] [-l dailyLimitUsd]` | `Done: smart account created.` Include alias and address; note it is not deployed until activated. |
| `account activate [alias\|address] [--no-sponsor]`                     | `Done: account deployed on-chain.`                                                                 |
| `account list [-c <chainId>]`                                          | `Found <n> item(s).` One line per account: alias, chain, deployed yes/no.                          |
| `account info [alias\|address]`                                        | `Status:` with balance, deployment state, and security state.                                      |
| `account rename ...`                                                   | `Done: account renamed to <new>.`                                                                  |
| `account switch <alias\|address>`                                      | `Done: active account is now <alias>.` Always pass alias/address (avoid interactive pick).         |

### Transaction

| Run                                                           | Tell the user                                                                          |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `tx simulate [account] --tx <spec>... [--no-sponsor]`         | Use `Preview:` template from SKILL.md.                                                 |
| `tx send [account] --tx <spec>... [--no-sponsor] [--no-hook]` | Use `Done:` or `Action needed:` template. Never send without prior simulate + user OK. |
| `tx build ...`                                                | `Done: unsigned operation prepared.`                                                   |

`--tx` shape: `to:0x...,value:0.1,data:0x...` (`to` + either `value` or `data`; repeat `--tx` for batch).

### Query

| Run                                        | Tell the user                               |
| ------------------------------------------ | ------------------------------------------- |
| `query balance [account] [--token 0xAddr]` | `Status:` with account, amount, and symbol. |
| `query tokens ...`                         | `Found <n> item(s).`                        |
| `query tx <hash>`                          | `Status:` confirmed, pending, or not found. |
| `query chain`                              | `Status: current chain is <name> (<id>).`   |
| `query address <0x...>`                    | `Status:` address type and balance.         |

### Security / OTP / config

| Run                                          | Tell the user                                             |
| -------------------------------------------- | --------------------------------------------------------- |
| `security status`                            | `Status:` hook state, email, spending limit.              |
| `security 2fa install ...` / `uninstall ...` | `Done:` with plain-language result.                       |
| `security email bind\|change <email>`        | Often returns OTP pending; use `Action needed:` template. |
| `security spending-limit [usd]`              | View: `Status:`. Set: may return OTP pending.             |
| `otp submit <id> <code>`                     | Agent runs this after user provides the code.             |
| `otp list` / `otp cancel`                    | `Found <n> item(s).` / `Done:`.                           |
| `config show\|set\|remove`                   | `Status:` for show, `Done:` for set/remove.               |
| `update check` / `update`                    | `Status:` / `Done:`. No auto-update without user OK.      |

### Recovery

| Run                                                                                   | Tell the user                                                                                |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `recovery contacts list`                                                              | `Status:` with guardian count, threshold, each address.                                      |
| `recovery contacts set <addrs> --threshold <n> [--label ...] [--privacy] [--sponsor]` | `Done: guardians updated.` Include tx hash, count, threshold.                                |
| `recovery contacts clear [--sponsor]`                                                 | `Done: all guardians cleared.` Include tx hash.                                              |
| `recovery backup export [--output <file>]`                                            | `Done: backup exported.`                                                                     |
| `recovery backup import <file>`                                                       | `Done: backup imported.`                                                                     |
| `recovery initiate <address> --chain <id> [--from-backup <file>]`                     | `Done: recovery initiated.` Show recoveryUrl prominently. Tell user to share with guardians. |
| `recovery status [--wallet <addr> --recovery-id <hex>]`                               | `Status:` with recovery phase, signature count, countdown if applicable.                     |

### Service Discovery

| Run             | Tell the user                                                                                                            |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `services`      | `Found <n> service(s).` One line per service: id, name, category. Mention `services <id>` for details.                   |
| `services <id>` | Service name, description, endpoint list with pricing. Include example `request` command for the most relevant endpoint. |

### x402 / Delegations

| Run                                                                                                             | Tell the user                                                                                     |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `delegation add --manager <addr> --token <addr> --payee <addr> --amount <atomic> --permission 0x... [--verify]` | `Done: delegation stored.` Include id, token, payee, amount. Note if `--verify` passed and valid. |
| `delegation list [--account alias]`                                                                             | `Found <n> delegation(s).` One line per delegation: id, token, payee, amount, expiry.             |
| `delegation show <id>`                                                                                          | Full delegation details including permissionContext.                                              |
| `delegation verify <id>`                                                                                        | `Status:` valid / expired / insufficient_balance / invalid_onchain. Include details if failed.    |
| `delegation sync [--prune]`                                                                                     | `Status:` summary of valid/expired/invalid counts. With `--prune`: note how many expired removed. |
| `delegation renew <id> --expires-at <iso> [--permission 0x...] [--amount n] [--remove-old]`                     | `Done: delegation renewed.` Include new id and expiry. Note if old was removed.                   |
| `delegation revoke <id> [--calldata 0x...] [--keep-local]`                                                      | `Done: delegation revoked.` Include tx hash if on-chain. Note if local record kept.               |
| `delegation remove <id>`                                                                                        | `Done: local delegation record removed.` Note this does NOT revoke on-chain.                      |
| `request --dry-run <url>`                                                                                       | `Preview:` paywall requires amount to payee. No funds moved.                                      |
| `request <url> [--method POST --json ...]`                                                                      | `Paid:` amount to payee. Tx hash from settlement. Only after user approval.                       |

**Paid request decision tree for the agent:**

1. User wants to find a paid API -> `services` to browse, `services <id>` for endpoint details and example commands.
2. User has a URL (or picked one from services) -> `request --dry-run <url>` to preview the price.
3. If dry-run shows ERC-7710 requirement -> check `delegation list`. If no match -> guide user through `delegation add` with the server-provided parameters.
4. If dry-run shows EIP-3009 (USDC) -> no delegation needed, proceed directly.
5. Before paying -> tell user the amount, token, and payee, then wait for approval.
6. After paying -> report settlement tx hash. If payment fails with "expired" -> suggest `delegation renew` or `delegation sync --prune`.

---

## Agent: user approval before running

Say what you will run, wait for explicit yes, then execute.

**Money and deploy:** `tx send`, `account activate`, `request <url>` (non-dry-run)
**Delegation (on-chain):** `delegation revoke` (with `--calldata`)
**Security:** `security 2fa install`, `security 2fa uninstall`, `security email bind|change`, `security spending-limit` (when setting)
**Recovery (write):** `recovery contacts set`, `recovery contacts clear`, `recovery initiate`
**OTP / config:** `otp submit` (user provides code, agent executes), `otp cancel`, `config remove`, `update`

---

## Error codes (debug only)

If the user cares about numbers: `-32602` bad parameters, `-32002` wallet/account not ready, `-32005` send failed, `-32007` hook auth / recovery blocked, `-32010` to `-32014` OTP family, `-32000` generic.
