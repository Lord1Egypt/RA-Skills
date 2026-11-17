# FunctionSpace / propSPACE Skill Handoff

Skill: `fs-worldcup-knockout`  
Published ClawHub owner: `@bridgeaisocial`  
Published version verified: `0.1.5` after this feedback pass.  
Repo path used for verification: `/root/projects/@bridgeaisocial/fs-worldcup-knockout`

## What this skill does

`fs-worldcup-knockout` trades propSPACE World Cup knockout player fantasy-score markets.

- Venue: FunctionSpace / propSPACE play-money engine only.
- It is not Simmer `$SIM`, Polymarket, Kalshi, or real-money trading.
- Default mode is dry-run.
- `--live` places mutating propSPACE play-money positions in the FunctionSpace competition engine.
- Default mode selects the best 1 FWD + 1 MID + 1 DEF for the currently open round.
- Live campaign page: `https://propspace.fun`; signup: `https://app.propspace.fun`.
- Prize pool per live campaign page/partner feedback: `$6,500` total (`$1,000` each knockout round R32 through Semis plus `$2,500` grand prize across all rounds); each round starts with a fresh `$1,000` play-money bankroll.

## Install / run

```bash
npx --yes clawhub@latest install fs-worldcup-knockout --dir ./skills --force
cd ./skills/fs-worldcup-knockout

export FS_USERNAME=<agent_username>
export FS_PASSWORD=<agent_password_min_6_chars>
export FS_BASE_URL=https://fs-engine-api-mech-v0-4.onrender.com

python3 main.py --list-markets
python3 main.py --inspect <market_id>
python3 main.py
python3 main.py --live   # propSPACE play-money mutation
```

## Verification performed on 2026-06-29 UTC

### Static validation

```bash
python3 -m py_compile main.py fs_client.py fs_beliefs.py scripts/enrich_from_web.py
python3 -m json.tool clawhub.json
```

Result: passed.

### Market discovery

Command:

```bash
python3 main.py --list-markets
```

Result:

- Authenticated successfully.
- Open WC markets: `round=R32`, `47 markets`.
- Position coverage present: FWD, MID, DEF.

### Representative inspections

FWD market inspected:

```text
Market 5: Ayase Ueda (R32)
  Round: R32  Position: FWD  Range: -2.5–25.5  Buckets: 28
  FS expected: 4.24pts  Consensus mean: 7.33pts
  Our belief:  4.24pts  Edge: 11.1%
  Recipe:      {'position_type': 'normal', 'position_params': {'mean': 0.2407, 'std_dev': 0.1607}}
  Ayase Ueda (Japan) [FWD]: E=4.2pts  [FS line=4.2pts + player not in DB — using FS line as-is]
  Winning bucket if our prediction is right: 6
```

DEF market inspected:

```text
Market 16: Achraf Hakimi (R32)
  Round: R32  Position: DEF  Range: -8.5–20.5  Buckets: 29
  FS expected: 4.14pts  Consensus mean: 6.92pts
  Our belief:  4.14pts  Edge: 9.6%
  Recipe:      {'position_type': 'normal', 'position_params': {'mean': 0.4359, 'std_dev': 0.1655}}
  Achraf Hakimi (Morocco) [DEF]: E=4.1pts  [FS line=4.1pts + player not in DB — using FS line as-is]
  Winning bucket if our prediction is right: 12
```

### Dry-run selection

Command:

```bash
python3 main.py
```

Result:

```text
[FWD] Best pick  edge=13.8%
  [30] Folarin Balogun (R32)
    → WOULD BUY collateral=333.0 (dry run)

[MID] Best pick  edge=15.7%
  [2] Vinícius Júnior (R32)
    → WOULD BUY collateral=333.0 (dry run)

[DEF] Best pick  edge=9.6%
  [16] Achraf Hakimi (R32)
    → WOULD BUY collateral=333.0 (dry run)

Done. Picks selected: 3/3  Trades executed: 0/3
```

### Live propSPACE play-money execution

A fresh test account was used: `hermes_wc_publish_1782726923`.

Command:

```bash
python3 main.py --live
```

Result:

```text
→ BOUGHT position_id=7 trade_size=326.4705882352941
→ BOUGHT position_id=20 trade_size=326.4705882352941
→ BOUGHT position_id=6 trade_size=326.4705882352941
Done. Picks selected: 3/3  Trades executed: 3/3
```

Position verification:

```text
position_id=7 market=30 collateral=333.0 status=open
position_id=6 market=16 collateral=333.0 status=open
position_id=20 market=2 collateral=333.0 status=open
```

### Published-package verification

Commands:

```bash
npx --yes clawhub@latest publish . --dry-run --version 0.1.3
npx --yes clawhub@latest publish . --version 0.1.3
npx --yes clawhub@latest install fs-worldcup-knockout --dir /tmp/fs-worldcup-knockout-verify-013 --force
python3 -m py_compile /tmp/fs-worldcup-knockout-verify-013/fs-worldcup-knockout/main.py \
  /tmp/fs-worldcup-knockout-verify-013/fs-worldcup-knockout/fs_client.py \
  /tmp/fs-worldcup-knockout-verify-013/fs-worldcup-knockout/fs_beliefs.py \
  /tmp/fs-worldcup-knockout-verify-013/fs-worldcup-knockout/scripts/enrich_from_web.py
```

Result:

- Publish dry-run: `Would publish fs-worldcup-knockout@0.1.3`
- Publish: successful.
- Fresh install: `Installed fs-worldcup-knockout v0.1.3`
- Fresh install compile/json validation: passed.
- ClawHub inspect: `@bridgeaisocial · v0.1.3 · latest=0.1.3`, moderation `CLEAN` / `pending.scan`.

## Important caveats for FunctionSpace to verify

1. All observed players currently show missing sentiment enrichment (`✗` / player not in DB). This is intentional fallback behavior: the skill still trades using FS `expectedPts` / `line` as-is. If FunctionSpace wants sentiment-backed edges, run or improve `scripts/enrich_from_web.py` and/or provide a seeded player file.
2. Please confirm the official fantasy scoring/variance assumptions. The strategy uses FS metadata for the mean expectation and position-specific spread constants in `main.py`.
3. Please confirm the engine URL and whether `https://fs-engine-api-mech-v0-4.onrender.com` is the exact backend the live `propspace.fun` competition settles on, whether API trades count toward the `$6,500` competition, and whether agent/bot trading is allowed under competition rules.
4. Please confirm whether `position_id` is globally unique or scoped by `(market_id, position_id)`; current automation treats the pair as the safer unique handle for future sell/management automation.
5. `--live` is a real mutation against the propSPACE play-money engine, despite not being real-money trading.
