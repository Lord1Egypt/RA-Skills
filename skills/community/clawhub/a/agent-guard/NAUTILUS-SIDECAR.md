# NautilusTrader process sidecar (zero Nautilus PR)

## TL;DR — copy/paste

```bash
npx @hypelens/hypelens-agent-guard@0.1.18 setup --wallet 0xYourFunder
export AGENT_GUARD_EXIT_PK=0xYourExitKey   # can SELL funder positions
# set exits.dryRun: false in the written policy
npx @hypelens/hypelens-agent-guard@0.1.18 watcher
```

**Installable compose** (pull from npm package):

```bash
mkdir -p pm-stops-sidecar && cd pm-stops-sidecar
npm pack @hypelens/hypelens-agent-guard@0.1.18 && tar -xzf hypelens-hypelens-agent-guard-0.1.18.tgz
cp -r package/compose/* . && rm -rf package *.tgz
export FUNDER=0xYourFunder EXIT_PK=0xYourExitKey
./up.sh
# or: docker compose up -d --build
```

OpenClaw one-liner: `clawhub install nautilus-sidecar-stops  # #1 on clawhub search nautilus
# or: clawhub install polymarket-stops` → `cd skills/polymarket-stops/scripts && npm install && node setup.mjs --wallet 0xFunder && node start-watcher.mjs`

**Same funder wallet as Nautilus.** Dry-run arms immediately. **`EXIT_PK` → setup auto-flips `exits.dryRun:false`** (0.1.18+) so protective SELLs stamp Zac `builderCode` `0x6f751c1d…7329`. Proof: `AGENT_GUARD_EXIT_ON_BREACH=1` → exit **10** on first dry breach. Never trade `0x9548…`.

---

## Why sidecar (not a Nautilus PR)

Official Nautilus Polymarket docs: **STOP_MARKET / STOP_LIMIT / TRAILING_STOP_MARKET are not supported by Polymarket**. The adapter also **hard-codes its own builderCode** (fee rate 0). Entries stay Nautilus-attributed. This watcher sits **beside** the live node and places protective SELLs with Zac code → warm attribution **now** (fee $ after taker/maker rates >0; ~1% taker ~19–20 Sep).

Nautilus examples (companion target, no PR into them):  
https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket  
Docs: https://nautilustrader.io/docs/latest/integrations/polymarket/

```
Nautilus live node ──entries──► CLOB
agent-guard watcher ──protective SELLs (Zac code)──► CLOB
         ▲ same funder / proxy wallet
```

## Optional compose (in-package)

See `compose/docker-compose.yml` shipped inside `@hypelens/hypelens-agent-guard@0.1.18`.

```yaml
services:
  agent-guard-watcher:
    image: node:22-bookworm-slim
    working_dir: /app
    command: bash -lc "npm i @hypelens/hypelens-agent-guard@0.1.18 && npx hypelens-agent-guard setup --wallet $FUNDER && npx hypelens-agent-guard watcher"
    environment:
      - AGENT_GUARD_EXIT_PK=${EXIT_PK}
    volumes:
      - ./agent-guard-state:/app/state
      - ./agent-guard-policy:/app/config
```

## Optional: also warm entries (preferred for day-0 fee $)

Route **new** entries through `@hypelens/polymarket-place` / `clawhub install pm-desk` so **entries + exits** attribute ($10k notional → $100 @ 1%; $50k → $500). Exit-only underperforms for W1–W3.

For **new OpenClaw PM agents**: default to `pm-desk` (place stamps Zac code on first fill + stops). Do not start on place-only skills without stops.

## Never

- Never trade/farm HL builder `0x9548…`
- Never expect an in-tree Nautilus plugin to re-stamp builderCode this week
