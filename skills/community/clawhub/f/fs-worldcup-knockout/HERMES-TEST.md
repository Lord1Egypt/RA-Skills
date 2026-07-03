# FS World Cup Knockout — Hermes Test Brief

Test the `fs-worldcup-knockout` skill against the live propSPACE engine.
The skill picks 1 FWD + 1 MID + 1 DEF per round and places belief trades on
their FIFA fantasy point markets.

Requires: Python 3.8+, git, internet access. No pip installs needed.

---

## Setup

### A) GitHub PAT (recommended — works for all future tests too)

Create a fine-grained PAT at github.com → Settings → Developer settings →
Personal access tokens → Fine-grained tokens. Scope: repository `SupaFund/simmer`,
permission `Contents: Read-only`. Then:

```bash
export GITHUB_TOKEN=<paste-token-here>
git clone --depth=1 https://$GITHUB_TOKEN@github.com/SupaFund/simmer.git /root/projects/simmer
cd /root/projects/simmer/skills/fs-worldcup-knockout
```

### B) Tarball (one-off — no GitHub auth needed)

Nick runs locally: `tar czf fs-wc.tar.gz skills/fs-worldcup-knockout/`
then transfers to Hermes. Extract with:

```bash
tar xzf fs-wc.tar.gz   # produces skills/fs-worldcup-knockout/
cd skills/fs-worldcup-knockout
```

---

### Env vars (required for both paths)

```bash
export FS_USERNAME=hermes_wc_test
export FS_PASSWORD=simmer-wc-bot
export FS_BASE_URL=https://fs-engine-api-mech-v0-4.onrender.com
```

Note: the engine may cold-start after idle — first request can take 10–15s. Normal.

---

## Step 1 — List open markets

```bash
python3 main.py --list-markets
```

Expected output:
```
Authenticated as hermes_wc_test  balance=1000.0

Open WC markets  round=MDx  (N markets)

  [312] FWD ✗  Michael Gregoritsch      Austria       FS=3.01  consensus=3.1pts
  [313] MID ✓  Kylian Mbappé            France        FS=6.20  consensus=5.8pts
  ...
```

Check:
- `balance=1000.0` on the auth line (new account, play-money)
- At least one FWD, one MID, one DEF in the list
- ✓ = player has sentiment data, ✗ = no sentiment (uses FS line as-is, still trades)

Report back: total market count, which round (e.g. MD1), any auth errors.

---

## Step 2 — Inspect one market

Pick any market ID from the list. Run for one FWD and one DEF:

```bash
python3 main.py --inspect <market_id>
```

Expected output:
```
Market 312: Michael Gregoritsch (Austria, MD3)  [FWD]
  Round: MD3  Position: FWD  Range: -5.5–20.5  Buckets: 26
  FS expected: 3.01pts  Consensus mean: 3.10pts
  Our belief:  3.01pts  Edge: 0.3%
  Recipe:      {'position_type': 'normal', 'position_params': {'mean': 0.327, 'std_dev': 0.173}}
```

Report back: paste the full output for one FWD and one DEF.

---

## Step 3 — Dry run

```bash
python3 main.py
```

Expected output:
```
[DRY RUN] Pass --live to execute real trades.

Authenticated as hermes_wc_test  balance=1000.0

3-pick mode: finding best FWD / MID / DEF from N market(s)...

[FWD] Best pick  edge=12.3%
  [312] Michael Gregoritsch (Austria, MD3)
    Our E: 3.45pts  Consensus: 3.01pts  Edge: 12.3%
    → WOULD BUY collateral=333 (dry run)

[MID] Best pick  edge=8.1%
  ...

[DEF] Best pick  edge=9.5%
  ...

Done. Picks selected: 3/3  Trades executed: 0/3
```

Check:
- "Picks selected: 3/3" — one per position
- Edges are non-zero (if all edges are 0.0% every player is flat against consensus — worth reporting)

Report back: the 3 picks (player name, position, edge %).

---

## Step 4 — Live trade

Only run if Steps 1–3 passed without errors.

```bash
python3 main.py --live
```

Expected output for each pick:
```
[FWD] Best pick  edge=12.3%
  [312] Michael Gregoritsch (Austria, MD3)
    ...
    → BOUGHT position_id=7 trade_size=326.8
```

Final line should be: `Trades executed: 3/3`

**Error codes:**
- `HTTP 401` — token issue. Delete `.auth/hermes_wc_test.json` and rerun.
- `HTTP 403` — insufficient balance. Report the balance shown on auth line.
- `HTTP 410` — market past trading cutoff (kickoff already happened). Report which market ID.
- `HTTP 400` — report the full error body.

Report back: paste the 3 "BOUGHT" lines including position_ids and trade_sizes,
or the full error if it failed.

---

## Step 5 — Verify positions (after live trade)

```bash
python3 - <<'EOF'
import os, json, sys
from pathlib import Path
sys.path.insert(0, '.')
from fs_client import FSClient
c = FSClient(
    base_url=os.environ['FS_BASE_URL'],
    token_store=Path('.auth/hermes_wc_test.json'),
)
for p in c.positions():
    print(f"  position_id={p['position_id']} market={p['market_id']} "
          f"collateral={p['collateral']} status={p['status']}")
EOF
```

Expected: 3 lines, each with `status=open` and `collateral=333.0`.

---

## What to report back

1. Step 1 — market count, round name, any errors
2. Step 2 — paste `--inspect` output for one FWD + one DEF
3. Step 3 — the 3 dry-run picks (player, position, edge)
4. Step 4 — the 3 BOUGHT lines with position_ids, or error details
5. Step 5 — positions output confirming 3 open positions

Engine: `https://fs-engine-api-mech-v0-4.onrender.com`
Repo:   `https://github.com/SupaFund/simmer` (skills/fs-worldcup-knockout/)
Token stored at: `skills/fs-worldcup-knockout/.auth/hermes_wc_test.json`
