# Fetch Solana Logs — Reference

## Skill layout

```
fetch-solana-logs/
├── SKILL.md
├── reference.md
├── examples.md
├── scripts/
│   ├── init-project.sh
│   └── probe-idl.mjs
└── templates/
```

## Agent contract

1. User wants Solana txs for address(es)
2. **`isSolanaAddress(addr)` must be true** (`pnpm validate`) — abort if not
3. Write `target_solana_addr.json`
4. Run `pnpm s1` then `pnpm s2`
5. Report `output/<addr>/`

Default first pull: `--limit 50`. Full history: omit `--limit` (needs Helius).

Validation uses `src/utils/utils.ts` → `isSolanaAddress` (via `PublicKey`), also enforced inside `common.ts` `validateAddresses` on every s1/s2.

## Config file

`target_solana_addr.json`:

```json
["Addr1", "Addr2"]
```

## Data sources

| Mode | Needs | When |
|------|-------|------|
| Helius | `HELIUS_API_KEY` | Preferred always |
| Public RPC | none | Fallback for `--limit` only |

## IDL

Auto on s1 via `Program.fetchIdl` → `output/<addr>/idl_<addr>.json`.  
If missing and decode needed → ask user for IDL file; never invent.
