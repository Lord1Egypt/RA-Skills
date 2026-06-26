---
name: atxswap
description: >-
  Manage ATX on BSC with wallet creation, price and balance queries, PancakeSwap
  V3 swaps, liquidity operations, LP positions and holdings, and BNB/ERC20 transfers.
  Use when the user mentions ATX, BSC, PancakeSwap V3, wallet creation, price checks,
  buying, selling, liquidity, fees, holdings, LP positions, or token transfers.
version: "0.0.31"
compatibility: Requires Node.js 18+ and npm. Network access to BSC RPC required.
inject:
  - bash: echo "${CLAUDE_SKILL_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
    as: SKILL_DIR
metadata:
  author: agentswapx
  openclaw:
    requires:
      bins:
        - node
        - npm
    homepage: https://github.com/agentswapx/skills/tree/main/atxswap
    os:
      - linux
      - macos
---

# ATXSwap Skill

Execute ATX trading and wallet workflows on BSC. This skill is designed for
agents that need safe, repeatable commands for wallet management, ATX/USDT
quotes, swaps, V3 liquidity actions, and transfers.

- **SDK**: [`atxswap-sdk`](https://www.npmjs.com/package/atxswap-sdk) on npm ([source](https://github.com/agentswapx/atxswap-sdk))
- **Docs (team / project)**: [Team introduction (EN)](https://docs.atxswap.com/guide/team) · [Team introduction (ZH)](https://docs.atxswap.com/zh/guide/team)
- **Keystore dir**: `~/.config/atxswap/keystore` (fixed, not configurable)
- **Secrets dir**: `~/.config/atxswap/` (master.key + secrets.json)

## Use This Skill For

- Create the single wallet used by this skill instance (importing an existing private key is not supported)
- Query ATX price, balances, LP positions (see **Required agent reply for holdings** under `query.js`), quotes, and arbitrary ERC20 token info
- Buy or sell ATX against USDT on PancakeSwap V3
- Add liquidity (full range or a custom **price range in USDT per ATX** or **tick** bounds), remove liquidity, collect fees, or burn empty LP NFTs
- Transfer BNB, ATX, USDT, or arbitrary ERC20 tokens

## Before First Use

This skill ships its own Node scripts and depends on `atxswap-sdk`.

1. Open the skill directory where this `SKILL.md` is installed.
2. Run `npm install` there before using any script.
3. If `npm install` fails, stop and report the dependency error instead of guessing.

If the skill is installed via ClawHub or OpenClaw CLI, the install location is
typically `~/.clawhub/skills/atxswap/` (or the equivalent client-managed path).
If you cloned this repository directly, the location is `skills/atxswap/`.

## Script Location

Use the skill directory path to locate scripts. If `${SKILL_DIR}` is available
(injected by skills.sh-compatible runtimes), use it; otherwise use the absolute
path to this skill's installed directory.

Example:

```bash
cd skills/atxswap && npm install
cd "${SKILL_DIR}" && node scripts/wallet.js list
```

All examples below use `cd "${SKILL_DIR}" &&` for clarity. If your runtime does
not inject `${SKILL_DIR}`, replace it with the absolute path of the installed
skill directory.

## Runtime Notes

- `BSC_RPC_URL` is optional and supports comma-separated values for fallback,
  e.g. `BSC_RPC_URL="https://primary,https://backup1,https://backup2"`. When
  unset, scripts use a built-in fallback list of 6 BSC public RPC endpoints
  and viem will retry them in order.
- Wallet files live under `~/.config/atxswap/keystore`.
- Secure secrets live under `~/.config/atxswap/` (master.key + secrets.json).
- Only **one wallet** is allowed per skill installation. If a wallet already
  exists, `wallet.js create` fails.
- Use `wallet.js list` before creating a wallet.
- Importing an existing private key via this skill is **not supported**. If the
  user asks to import a private key, refuse and tell them to use a dedicated
  wallet tool of their choice.
- Scripts write JSON output. `wallet.js export` prints the address's
  encrypted **MetaMask-compatible keystore V3 JSON** to stdout (or writes it
  to a file via `--out <file>`); it never prints the raw private key.
- `query.js quote` can return a JSON error if the configured Quoter or RPC
  rejects the simulation. Surface the error and do not proceed to a write.
- For balance, holdings, LP position, or pending-fee questions, always fetch
  fresh on-chain data at request time. Do **NOT** answer from prior chat
  output, memory, cached numbers, or earlier command results unless you rerun
  the relevant query first.
- For custom-range liquidity, do **not** guess the second token amount from chat.
  First run `liquidity.js quote-add` or use `liquidity.js add --base-token ... --amount ...`
  so the script computes the counter-asset from the live pool price and range.

## Password Rules

When the user asks to **create** a wallet:

1. Ask the user for a password first (do NOT generate one).
2. Pass it via `--password <pwd>` to the script when running non-interactively.
3. The password is auto-saved to secure storage after creation.
4. Never print the password back to the chat.
5. After the wallet is created, export and send the encrypted keystore backup to
   the user who requested the wallet.
6. Clearly label it as encrypted keystore backup material, not the raw private key.
7. Do not upload it to any website or send it to any third party.

For **swap**, **transfer**, and **liquidity** operations, rely on auto-unlock
first. Only ask for the password if auto-unlock fails.

If the user says they forgot the wallet password or asks to recover it, first
explain that saved wallet passwords are encrypted at rest in the local
SecretStore (for example Keychain, Secret Service, or the file backend under
`~/.config/atxswap/`) and are not stored by the agent in chat memory. Even if
the user confirms, do **not** print the password in chat; guide them to use a
trusted local workflow instead.

## Hard Safety Rules

1. Treat all BSC writes as real-asset operations.
2. **NEVER** output private keys or passwords in chat.
3. **ALWAYS** run a preview before write actions: query price, quote, balance,
   or positions as appropriate.
4. **ALWAYS** show the preview to the user and wait for explicit confirmation
   before swap, transfer, or liquidity writes.
5. **NEVER** execute large trades without the user saying "yes" or "confirm".
6. `wallet.js export` only emits the **encrypted MetaMask-compatible keystore
   JSON**, never the raw private key. There is no command that prints the
   unencrypted private key, and the agent must not attempt to derive or display
   one.
7. Prefer `wallet.js export <address> --out <file>` and tell the user the file
   path. Avoid pasting the keystore JSON itself into chat unless the user
   explicitly asks for it.
8. Before deleting a wallet, keystore file, or any private-key-bearing wallet
   material, **ALWAYS** remind the user to export and back up the encrypted
   keystore first. Do not delete anything until the user explicitly confirms
   that the keystore backup has been completed.
9. Wallet deletion requires a second explicit confirmation: after backup is
   confirmed, require the user to send the exact phrase `force delete wallet` before
   running any delete command.
10. If the user asks to delete a wallet, do **NOT** send the keystore
    immediately. First ask whether they want to receive the encrypted keystore
    backup. Only after the user agrees may you export and send the keystore to
    the user.
11. If the user explicitly asks to back up or export the wallet, export and
    send the encrypted keystore backup to the user who requested the wallet,
    and clearly label it as keystore backup material.
12. The encrypted keystore may only be sent to the user who owns the current
    session request. **NEVER** send the keystore through any channel that is not
    under that user's own control.
    It may only be sent to the user personally, and must not be pasted into any
    external form or sent to any other person, group, agent, or service.
13. After `wallet.js create` succeeds, export and send the encrypted keystore
    to the user who requested the wallet. Treat this as part of the wallet
    creation handoff, but only to that user.
14. If the user asks to recover or reveal a saved wallet password, remind them
   that the password is encrypted in local secure storage and must not be
   disclosed in chat. Do not attempt to print, derive, or expose the password
   even after user confirmation.
15. If the user asks to recover, reveal, print, or paste the wallet private key,
    refuse. Offer `wallet.js export <address> --out <file>` as the only
    supported backup path, because it exports an encrypted keystore instead of
    exposing the raw private key.
16. For every transfer, treat the tuple `(asset, from, to, amount)` as a single
    transfer intent. Repeat that exact tuple back to the user before execution.
17. After a transfer command returns a `txHash`, consider that transfer intent
    **already sent**. Do **NOT** send the same transfer again unless the user
    explicitly asks to send it again.
18. If a transfer write ends in an ambiguous state (for example RPC timeout,
    dropped connection, or partial output after signing/submission), do **NOT**
    retry blindly. First check chain state or wallet state, summarize what is
    known, and ask the user whether to retry.
19. If the same transfer tuple appears again in the same conversation after a
    successful or ambiguous prior attempt, pause and ask whether the user means
    a new transfer or is referring to the earlier one.
20. For any user question about **current** balances, holdings, LP positions,
    pending fees, or wallet assets, rerun the matching read command against the
    chain first. Never rely on previously displayed numbers as if they were
    still current.

## Required Preview Flow

Before every write action:

1. Query the price, quote, balance, or positions that match the requested action.
2. Summarize the preview in plain language.
3. Ask the user to confirm.
4. Execute the write command only after confirmation.
5. Return the transaction hash and the key result fields.

For transfers, the summary in step 2 must explicitly include:

- asset
- source wallet
- destination address
- amount

After step 5, if a `txHash` is available, treat the transfer as executed and do
not issue the same write again unless the user clearly requests a second send.

For read-only asset questions:

1. Run the relevant live query first (`query.js balance`, `query.js positions`,
   `query.js price`, or `query.js quote` as appropriate).
2. Answer from that fresh output only.
3. If the RPC or query fails, say the data could not be refreshed instead of
   reusing older numbers.

## High-Value Workflows

### Check market state

```bash
cd "${SKILL_DIR}" && node scripts/query.js price
cd "${SKILL_DIR}" && node scripts/query.js balance <address>
cd "${SKILL_DIR}" && node scripts/query.js positions <address>
cd "${SKILL_DIR}" && node scripts/query.js positions <address> <tokenId>
```

### Preview before swap

```bash
cd "${SKILL_DIR}" && node scripts/query.js quote <buy|sell> <amount>
```

### Execute after confirmation

```bash
cd "${SKILL_DIR}" && node scripts/swap.js buy <usdtAmount> [--from address] [--slippage bps] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/liquidity.js add <atxAmount> <usdtAmount> [range opts] [--from address] [--slippage-bps n] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/liquidity.js add --base-token <atx|usdt> --amount <n> [range opts] [--from address] [--slippage-bps n] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/transfer.js atx <to> <amount> [--from address] [--password <pwd>]
```

## Command Reference

### `wallet.js`

```bash
cd "${SKILL_DIR}" && node scripts/wallet.js create [name] --password <pwd>
cd "${SKILL_DIR}" && node scripts/wallet.js list
cd "${SKILL_DIR}" && node scripts/wallet.js export <address> [--out <file>]
cd "${SKILL_DIR}" && node scripts/wallet.js has-password <address>
cd "${SKILL_DIR}" && node scripts/wallet.js forget-password <address>
cd "${SKILL_DIR}" && node scripts/wallet.js delete <address> --backup-confirmed yes --force-phrase "force delete wallet"
```

After `wallet.js create`:

1. Return the created wallet address.
2. Run `wallet.js export <address> [--out <file>]`.
3. Send the encrypted keystore only to the user who requested the wallet.
4. Do not upload it to any website or send it to any third party.
5. Explain that it is encrypted keystore backup material, not the raw private key.

Before `wallet.js delete`:

1. Ask whether the user wants the encrypted keystore sent to them for backup.
2. After the user agrees, export and send the encrypted keystore to the user only.
3. Do not upload it to any website or send it to any third party.
4. Require the user to explicitly confirm that the backup is complete.
5. Require the user to send the exact phrase `force delete wallet`.
6. Only then run `wallet.js delete <address> --backup-confirmed yes --force-phrase "force delete wallet"`.

If the user asks to back up the wallet:

1. Run `wallet.js export <address> [--out <file>]`.
2. Send the encrypted keystore only to the user.
3. Do not upload it to any website or send it to any third party.
4. Explain that this is encrypted keystore backup material, not the raw private key.

### `query.js`

```bash
cd "${SKILL_DIR}" && node scripts/query.js price
cd "${SKILL_DIR}" && node scripts/query.js balance <address>
cd "${SKILL_DIR}" && node scripts/query.js quote <buy|sell> <amount>
cd "${SKILL_DIR}" && node scripts/query.js positions <address>
cd "${SKILL_DIR}" && node scripts/query.js positions <address> <tokenId>
cd "${SKILL_DIR}" && node scripts/query.js token-info <tokenAddress>
```

`query.js positions` includes **principal token amounts** in the position (`principalAtx`,
`principalUsdt`, `principal0`, `principal1`) computed from V3 `liquidity` (L), ticks (internal),
and the pool’s current `sqrtPriceX96` (same `getAmountsForLiquidity` math as the web app). It emits
human **USDT-per-ATX** bounds as **`priceRangeUsdtPerAtx.min` / `.max`**, **`currentPriceUsdtPerAtx`**,
and **`currentPriceInRange`** (whether the pool tick lies inside that position). It includes
**`pendingFees.atx`** and **`pendingFees.usdt`** as the simulated collect notionals (`collectable*`),
plus raw `tokensOwed0`/`1` and `collectable0`/`1` for debugging. Use `collectable*` / `pendingFees`
to decide whether a fee harvest is worth executing. Each object also includes **`feePercent`**
(e.g. `"0.25%"`) for the pool’s swap-fee tier; raw **`fee`** stays the on-chain code
(`100` / `500` / `2500` / `10000`). **Tick indices are not included** in the JSON — quote
USDT/ATX prices and in-range state instead.

When the user asks "how much do I have now", "what is my current balance", "what
positions are left", "how much ATX is still in the LP", or similar present-tense
questions, rerun `query.js balance` and/or `query.js positions` immediately.
Do not answer from previously captured JSON.

**Required agent reply for holdings** when the user asks about their positions, LP NFTs, or liquidity holdings (per position):

Run `query.js positions <address>` (omit `tokenId` to list all ATX/USDT V3 NFTs). The CLI prints
**one JSON object per NFT**; include **every** position. For each position, the answer **must**
address the topics below (label them in the user’s language when replying). **Do not** show raw
V3 tick numbers to the user — use **USDT per 1 ATX** from the JSON below.

| Topic | What to include | CLI JSON fields |
|-------|-----------------|-----------------|
| **Tokens in the position** | **In-range liquidity** as ATX and USDT notionals — always cite **`principalAtx`** and **`principalUsdt`** (and optionally `principal0` / `principal1` in pool token0/token1 order). These are computed at the **current pool price**. Mention `liquidity` only as the raw **L** scalar if explaining detail. Do **not** treat **`query.js balance`** as LP “position tokens”: wallet ATX/USDT/BNB balances are unrelated to NFT principal — if shown, label them distinctly (e.g. “Wallet balances, separate from this LP NFT”). |
| **NFT token ID** | The V3 LP NFT id | `tokenId` |
| **Pool swap fee tier** | The pool’s trading fee as a **percentage** for end users | Prefer **`feePercent`** (e.g. `"0.25%"`). If you show the raw tier code, pair it with **`feePercent`** (e.g. `2500` + `0.25%`). |
| **Price range & spot** | Configured **min/max USDT per 1 ATX** for the position, and current pool price in the same unit | **`priceRangeUsdtPerAtx.min`**, **`priceRangeUsdtPerAtx.max`**, **`currentPriceUsdtPerAtx`**, **`currentPriceInRange`** (confirm “in range” / “out of range” in natural language). |
| **Pending fees** | Uncollected fees (both tokens) | Always show **`pendingFees.atx`** and **`pendingFees.usdt`** explicitly. Prefer these over quoting only one asset. Optionally reference `collectableAtx`/`collectableUsdt` synonyms. State fees stay **pending** until `liquidity.js collect`. |

Do not answer with only raw pool indices (ticks). If there are no positions, relay `No ATX/USDT positions found.` exactly.

Minor mismatch vs on-chain bookkeeping can occur because `principal*` uses the same float-based
tick→√P path as other tooling (~wei-level); values are intended for humans and routing, not audits.

### `swap.js`

```bash
cd "${SKILL_DIR}" && node scripts/swap.js buy <usdtAmount> [--from address] [--slippage bps] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/swap.js sell <atxAmount> [--from address] [--slippage bps] [--password <pwd>]
```

### `liquidity.js`

**`add` — price / tick range** (same USDT/ATX semantics as the web app; default full range = full-width liquidity):

- Default: no extra flags means **full range** (same as before).
- `--full-range`: explicit full range (do not combine with the two groups below).
- `--min-price` / `--max-price`: band in **USDT per 1 ATX**; the script reads pool `token0` and maps to `tickLower` / `tickUpper` like the app (`token1/token0` + `tickSpacing`). **Both** prices are required.
- `--range-percent`: band around **current ATX price** as a percentage; e.g. `20` means about `-20%` to `+20%` of the current price.
- `--tick-lower` / `--tick-upper`: raw V3 ticks (**both** required; script uses the smaller as lower, larger as upper, clamped to valid V3 bounds).
- `quote-add <atx|usdt> <amount>`: given live price and range, estimate the other leg — use before a write.
- `add --base-token <atx|usdt> --amount <n>`: single-sided notional; script computes the other leg and executes the add.

Optional: `--slippage-bps` (0–10000; default from SDK).

```bash
cd "${SKILL_DIR}" && node scripts/liquidity.js quote-add <atx|usdt> <amount> [range opts]
cd "${SKILL_DIR}" && node scripts/liquidity.js add <atxAmount> <usdtAmount> [range opts] [--from address] [--slippage-bps n] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/liquidity.js add --base-token <atx|usdt> --amount <n> [range opts] [--from address] [--slippage-bps n] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/liquidity.js remove <tokenId> <percent> [--from address] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/liquidity.js collect <tokenId> [--from address] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/liquidity.js burn <tokenId> [--from address] [--password <pwd>]
```

`liquidity.js remove` already uses a single `multicall`:
`decreaseLiquidity` -> `collect` -> and when `percent = 100`, `burn`.
That means a full removal automatically collects withdrawable funds and destroys the LP NFT in the same transaction, so
running `collect` again for the same `tokenId` is expected to fail because the position no longer exists.

Before `collect`, preview the target position with:

```bash
cd "${SKILL_DIR}" && node scripts/query.js positions <address> <tokenId>
```

Prefer `pendingFees` / `collectableAtx` / `collectableUsdt` over relying on `tokensOwed0/1` alone when deciding whether
fees are available, because the raw `tokensOwed` fields may stay at zero while
`collect()` can still succeed.

Example (not full-range; align the range with the user using `query.js price` before writes):

```bash
cd "${SKILL_DIR}" && node scripts/liquidity.js quote-add usdt 0.1 --range-percent 20
cd "${SKILL_DIR}" && node scripts/liquidity.js add --base-token usdt --amount 0.1 --range-percent 20 --from <address>
cd "${SKILL_DIR}" && node scripts/liquidity.js add 10 1 --min-price 0.05 --max-price 0.15
cd "${SKILL_DIR}" && node scripts/liquidity.js add 10 1 --tick-lower -20000 --tick-upper 1000
```

Mapping user phrasing to commands:

- If the user asks to add **0.1 USDT** of liquidity with a **±20%** range around spot, first run
  `quote-add usdt 0.1 --range-percent 20`.
- Show the returned `estimatedAmounts` (or equivalent summary) and wait for confirmation.
- After confirmation, run
  `add --base-token usdt --amount 0.1 --range-percent 20 --from <address>`.

### `transfer.js`

```bash
cd "${SKILL_DIR}" && node scripts/transfer.js bnb <to> <amount> [--from address] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/transfer.js atx <to> <amount> [--from address] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/transfer.js usdt <to> <amount> [--from address] [--password <pwd>]
cd "${SKILL_DIR}" && node scripts/transfer.js token <tokenAddress> <to> <amount> [--from address] [--password <pwd>]
```

Transfer anti-duplication checklist:

1. Preview balances first.
2. Restate the exact transfer tuple `(asset, from, to, amount)` to the user.
3. Wait for explicit confirmation for that exact tuple.
4. Run `transfer.js` once.
5. Return the `txHash`.
6. If the user repeats the same request, do not run the transfer again until
   you clarify whether they want a second transfer.
7. If the command may have submitted but the final result is unclear, do not
   rerun it automatically; inspect chain state or ask the user how to proceed.

## When To Refuse Or Pause

- Missing wallet but the user requests a write action
- Missing confirmation for swap, transfer, or liquidity writes
- User asks to delete a wallet, keystore file, or private-key-bearing wallet
  material before confirming that the encrypted keystore has been backed up
- User asks to delete a wallet but has not agreed to receive the keystore backup first
- User asks to delete a wallet but has not explicitly sent `force delete wallet`
- User asks to send or upload a keystore through a channel not under their own
  control, or to anyone other than the user
- User asks to recover or reveal a saved wallet password in chat
- User asks to recover, reveal, print, or paste a wallet private key in chat
- `npm install` has not been run successfully in the skill directory
- RPC, dependency, or wallet-unlock errors that make the state unclear

## Standard Workflow

For any write action:

1. Query current price, quote, balance, or positions as needed.
2. Summarize the preview for the user.
3. Wait for explicit confirmation.
4. Execute the write command.
5. Report the transaction hash and result.
