---
name: fetch-solana-logs
description:
  Auto-fetch Solana address/program transactions and optionally decode Anchor IDL
  instructions. Trigger whenever the user asks to get/pull/fetch/sync Solana txs,
  program logs, instruction data, 交易, 交易日志, or gives a base58 Solana address
  and wants its txs — e.g.「帮我获取这个 Solana 地址的 tx」「拉一下这个 program 的交易」
  「fetch txs for <addr>」. Agent must write the address into target_solana_addr.json
  and immediately run s1/s2 (scaffold project if missing). Pull + parse only.
---

# Fetch Solana Logs

中文版：[SKILL.zh.md](SKILL.zh.md)

**Agent-first workflow:** when the user wants txs for a Solana address, **do not stop at explaining** — configure the address and start pulling.

```
address from user
  → validate with isSolanaAddress (must pass)
  → ensure project (scaffold if needed)
  → write target_solana_addr.json
  → ensure .env (HELIUS_API_KEY)
  → pnpm s1 → pnpm s2
  → report output paths
```

## When to use (triggers)

Start this skill immediately on asks like:

| User says | Action |
|-----------|--------|
| 「帮我获取 / 拉取某个 Solana 地址的 tx」 | Auto-config + pull |
| 「帮我拉这个 program 的交易 / instruction」 | Auto-config + pull |
| 「fetch txs for `<base58>`」 | Auto-config + pull |
| Pastes a Solana address + wants history / logs | Auto-config + pull |

**Do not use** for EVM logs (→ `fetch-evm-logs`), stats-only analytics, or general Solana Q&A without wanting txs.

## Mandatory agent behavior

Once the user names an address, execute the following. **Do not pull until validation passes.**

### 0. Validate address (`isSolanaAddress`) — required before anything else

Use the project helper (do **not** invent your own check):

```typescript
import { isSolanaAddress } from './src/utils/utils';
isSolanaAddress(addr) // must be true
```

Or run:

```bash
pnpm validate -- --addr <ADDR>
# or after writing JSON:
pnpm validate
```

- If `false` / exits non-zero → **stop**, tell the user it is not a valid Solana address, ask for a corrected base58 pubkey. Do **not** write it to `target_solana_addr.json` or call s1.
- `s1`/`s2` also call `isSolanaAddress` via `validateAddresses` in `common.ts` as a second guard.

### 1. Ensure project

If cwd (or an agreed dir) already has `src/tx_logs/s1.pull.tx.ts`, use it.

Otherwise scaffold:

```bash
bash ~/.cursor/skills/fetch-solana-logs/scripts/init-project.sh [target_dir]
cd [target_dir]
```

Default dir: `./fetch_solana_logs`.

### 2. Write `target_solana_addr.json`

**Only after** `isSolanaAddress` passes. Persist the user’s address(es) here (project root):

```json
["DLvbp3sZCdoK6FoGnMdLSP2NZCCZdVfSGHD8KAGazZQH"]
```

Rules:

- Multiple addresses → JSON array; each must pass `isSolanaAddress`
- New request for a **different** address → replace or append as the user implies (default: set to the address(es) they just named)

### 3. Ensure `.env`

Need `HELIUS_API_KEY` for reliable pulls.

- If the user provides `HELIUS_API_KEY`, create `<project>/.env` immediately and write:

  ```dotenv
  HELIUS_API_KEY=<user-provided-key>
  ```

- Write the key directly to the project being operated on; do not put it in the skill directory or print the key in logs/responses
- If `.env` already exists, update only `HELIUS_API_KEY` and preserve unrelated entries
- If `.env` is missing and no key was supplied → copy from `.env.example`
- If key is empty → **ask once** for the key, write it, then continue
- If user has no key → still run with `--limit` (public RPC fallback); warn about rate limits

When scaffolding and the key is already available, pass it through the environment so `init-project.sh` creates `.env`:

```bash
HELIUS_API_KEY="$HELIUS_API_KEY" \
  bash ~/.cursor/skills/fetch-solana-logs/scripts/init-project.sh [target_dir]
```

### 4. Pull + parse (start immediately)

Default for a new “帮我拉一下” request (user did not specify full history):

```bash
pnpm s1 -- --limit 50
pnpm s2
```

This reads addresses from `target_solana_addr.json`.

Overrides:

| User intent | Command |
|-------------|---------|
| Recent N txs | `pnpm s1 -- --limit N` then `pnpm s2` |
| Only one addr while JSON has many | `pnpm s1 -- --addr <ADDR> --limit 50` then same for s2 |
| Full history (needs Helius) | `pnpm s1` (no `--limit`) then `pnpm s2` |
| Re-pull clean | delete `output/<addr>/` then s1/s2 |

### 5. Report results

Tell the user:

- Which address(es) were written to `target_solana_addr.json`
- Output paths under `output/<addr>/`
- Whether IDL was auto-saved; if program has **no** on-chain IDL and decode is needed, ask for IDL JSON and write `output/<addr>/idl_<addr>.json`, then re-run `pnpm s2`

## If address is missing

User said “帮我获取 Solana 的 tx” with **no** address → ask only:

> 请提供 Solana 地址（base58）。

Then go straight to steps 2–5. Do **not** ask for unnecessary options up front.

## IDL notes

- `s1` auto-tries on-chain Anchor IDL → `output/<addr>/idl_<addr>.json`
- Optional probe: `node ~/.cursor/skills/fetch-solana-logs/scripts/probe-idl.mjs --addr <ADDR>` (run inside project after `pnpm install`)
- Never invent an IDL

## Output layout

```
output/<addr>/
  ├── idl_<addr>.json              # if found / user-provided
  ├── tx_logs_<addr>.txt           # s1 NDJSON
  └── tx_logs_parsed_<addr>.json   # s2 (+ parsed instructions when IDL works)
```

## Checklist (agent)

```
- [ ] isSolanaAddress(addr) === true (pnpm validate)
- [ ] Project ready (existing or init-project.sh)
- [ ] Address(es) written to target_solana_addr.json
- [ ] HELIUS_API_KEY in .env (or public-RPC fallback acknowledged)
- [ ] pnpm s1 (default --limit 50) completed
- [ ] pnpm s2 completed
- [ ] User told output paths / IDL status
```

## Pitfalls

- Invalid address → fail validation; never write/pull
- Always use `pnpm s1 -- --limit 50` form (`--` before flags)
- Full sync without `--limit` requires Helius
- Wallets / non-Anchor programs may have no IDL — txs still pull fine

## Additional Resources

- [SKILL.zh.md](SKILL.zh.md) — Chinese version
- [scripts/init-project.sh](scripts/init-project.sh)
- [scripts/probe-idl.mjs](scripts/probe-idl.mjs)
- [reference.md](reference.md)
- [examples.md](examples.md)
