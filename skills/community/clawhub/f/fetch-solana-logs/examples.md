# Example: user asks to fetch txs

## User

> 帮我获取这个 Solana 地址的 tx：`DLvbp3sZCdoK6FoGnMdLSP2NZCCZdVfSGHD8KAGazZQH`

## Agent does (no extra confirmations)

```bash
# 0) validate first (isSolanaAddress)
pnpm validate -- --addr DLvbp3sZCdoK6FoGnMdLSP2NZCCZdVfSGHD8KAGazZQH

# 1) if no project; when user supplied a key, init creates .env
HELIUS_API_KEY="$HELIUS_API_KEY" \
  bash ~/.cursor/skills/fetch-solana-logs/scripts/init-project.sh ./fetch_solana_logs
cd ./fetch_solana_logs

# 2) write config (only after OK)
printf '%s\n' '["DLvbp3sZCdoK6FoGnMdLSP2NZCCZdVfSGHD8KAGazZQH"]' > target_solana_addr.json

# 3) if project already existed, create/update its .env with the supplied key
# HELIUS_API_KEY=<user-provided-key>

# 4) pull + parse
pnpm s1 -- --limit 50
pnpm s2
```

## Agent replies

Configured `target_solana_addr.json` → pulled 50 recent txs → outputs at:

```
output/DLvbp3sZCdoK6FoGnMdLSP2NZCCZdVfSGHD8KAGazZQH/
  tx_logs_….txt
  tx_logs_parsed_….json
  idl_….json   # only if on-chain IDL exists
```
