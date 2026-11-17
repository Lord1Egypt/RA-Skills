---
name: clv-journal
description: "Log bets with entry + closing odds, compute closing-line value (CLV) in odds pts and implied-prob pts, and roll up beat-close rate by sport/book/market."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": {
        "bins": ["python3"]
      }
    }
  }
---
# CLV Journal

Closing Line Value (CLV) is the process metric that predicts long-term betting edge. This skill keeps a **dedicated CLV journal** — entry price vs. close — separate from win/loss P&L. Beat the close consistently and the results follow.

Use alongside `bet-journal` (outcome/ROI) and `sports-odds` (live lines). This skill answers: *Did I get a better price than the market at close?*

## Formulas

**American → implied probability (no-vig single side):**

```
p = 100 / (a + 100)     if a > 0
p = |a| / (|a| + 100)   if a < 0
```

**Implied-prob CLV (pts):**

```
clv_prob = p_close − p_entry
```

Positive = you bought cheaper than the close (you beat the close). Example: entry −110 → p≈0.5238, close −120 → p≈0.5455 → CLV ≈ **+2.17 pts**.

**American odds CLV (pts):** for favorites (negative American), more negative close is better for the bettor who bought earlier:

```
clv_american_pts = entry − close     # e.g. −110 vs −120 → +10 pts
```

For underdogs (positive American), higher entry than close means you beat the close:

```
clv_american_pts = entry − close     # e.g. +150 vs +130 → +20 pts
```

**Spread / total line CLV (half-points):** if you bet a side, positive means the line moved in your favor after you bet:

```
# betting favorite −3.5 that closes −5.5 → +2.0 line pts
# betting underdog +3.5 that closes +1.5 → +2.0 line pts (same direction)
clv_line = signed_move_toward_your_side
```

**Beat-close rate:**

```
beat_close_rate = count(clv_prob > 0) / count(rows with both entry + close)
```

| Metric | Neutral | Good | Elite |
|--------|---------|------|-------|
| Avg CLV (prob pts) | ~0 | +1.0+ | +2.5+ |
| Beat-close rate | 50% | 55%+ | 60%+ |
| Sample size | — | 50+ | 200+ |

## Initialize the Journal

```bash
python3 -c "
import csv, os

JOURNAL = os.path.expanduser('~/.openclaw/clv-journal.csv')
os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)

HEADERS = [
    'id', 'ts_entry', 'ts_close', 'sport', 'event', 'market', 'side',
    'book', 'odds_entry', 'odds_close', 'line_entry', 'line_close',
    'clv_prob', 'clv_american', 'clv_line', 'beat_close', 'notes',
]

if not os.path.exists(JOURNAL):
    with open(JOURNAL, 'w', newline='') as f:
        csv.DictWriter(f, fieldnames=HEADERS).writeheader()
    print(f'Created {JOURNAL}')
else:
    print(f'Already exists: {JOURNAL}')

print('Markets: ML | SPREAD | TOTAL | PROP')
print('Leave odds_close / line_close blank until the market closes (pending).')
"
```

## Log an Entry (open price)

```bash
python3 -c "
import csv, os, uuid
from datetime import datetime, timezone

JOURNAL = os.path.expanduser('~/.openclaw/clv-journal.csv')
HEADERS = [
    'id', 'ts_entry', 'ts_close', 'sport', 'event', 'market', 'side',
    'book', 'odds_entry', 'odds_close', 'line_entry', 'line_close',
    'clv_prob', 'clv_american', 'clv_line', 'beat_close', 'notes',
]

def log_entry(sport, event, market, side, book, odds_entry,
              line_entry='', notes=''):
    row = {
        'id': str(uuid.uuid4())[:8],
        'ts_entry': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'ts_close': '',
        'sport': sport,
        'event': event,
        'market': market,
        'side': side,
        'book': book,
        'odds_entry': odds_entry,
        'odds_close': '',
        'line_entry': line_entry,
        'line_close': '',
        'clv_prob': '',
        'clv_american': '',
        'clv_line': '',
        'beat_close': '',
        'notes': notes,
    }
    with open(JOURNAL, 'a', newline='') as f:
        csv.DictWriter(f, fieldnames=HEADERS).writerow(row)
    print(f\"Logged entry {row['id']}: {sport} | {event} | {side} @ {odds_entry:+d} ({book})\")
    print('Fill close later with log_close(id, odds_close, line_close=...)')

# --- EDIT THESE ---
log_entry(
    sport='NBA',
    event='Lakers @ Warriors',
    market='SPREAD',
    side='Warriors -3.5',
    book='FanDuel',
    odds_entry=-110,
    line_entry=-3.5,
    notes='early steam, sharp-leaning',
)
"
```

## Fill Closing Odds + Compute CLV

```bash
python3 -c "
import csv, os, tempfile
from datetime import datetime, timezone

JOURNAL = os.path.expanduser('~/.openclaw/clv-journal.csv')

def american_to_prob(a):
    a = int(a)
    return 100 / (a + 100) if a > 0 else abs(a) / (abs(a) + 100)

def clv_line_pts(side, line_entry, line_close):
    if line_entry == '' or line_close == '':
        return ''
    le, lc = float(line_entry), float(line_close)
    # Convention: side string starts with team; use signed lines as stored.
    # Positive clv_line = line moved against the bettor's price (got better number).
    # For a negative line (favorite), more negative close → positive CLV.
    # For a positive line (dog), less positive / more negative close → positive CLV.
    return round(le - lc, 2)

def log_close(bet_id, odds_close, line_close=''):
    rows = []
    found = False
    with open(JOURNAL) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['id'] == bet_id:
                found = True
                entry = int(row['odds_entry'])
                close = int(odds_close)
                p_e = american_to_prob(entry)
                p_c = american_to_prob(close)
                clv_p = round((p_c - p_e) * 100, 3)  # probability points
                clv_a = entry - close                 # American pts
                clv_l = clv_line_pts(row['side'], row['line_entry'],
                                    line_close if line_close != '' else row['line_close'])
                row['ts_close'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                row['odds_close'] = close
                if line_close != '':
                    row['line_close'] = line_close
                row['clv_prob'] = clv_p
                row['clv_american'] = clv_a
                row['clv_line'] = clv_l
                row['beat_close'] = 'Y' if clv_p > 0 else ('T' if clv_p == 0 else 'N')
                print(f\"Closed {bet_id}: entry {entry:+d} → close {close:+d}\")
                print(f\"  CLV prob:     {clv_p:+.3f} pts\")
                print(f\"  CLV American: {clv_a:+d} pts\")
                if clv_l != '':
                    print(f\"  CLV line:     {clv_l:+.2f} half-pts\")
                print(f\"  Beat close:   {row['beat_close']}\")
            rows.append(row)
    if not found:
        print(f'No row with id={bet_id}')
        return
    fd, tmp = tempfile.mkstemp(text=True)
    os.close(fd)
    with open(tmp, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, JOURNAL)

# --- EDIT THESE ---
log_close('REPLACE', odds_close=-120, line_close=-5.0)
"
```

## One-shot: Entry + Close Together

When you already know both prices (post-game backfill):

```bash
python3 -c "
import csv, os, uuid
from datetime import datetime, timezone

JOURNAL = os.path.expanduser('~/.openclaw/clv-journal.csv')
HEADERS = [
    'id', 'ts_entry', 'ts_close', 'sport', 'event', 'market', 'side',
    'book', 'odds_entry', 'odds_close', 'line_entry', 'line_close',
    'clv_prob', 'clv_american', 'clv_line', 'beat_close', 'notes',
]

def american_to_prob(a):
    a = int(a)
    return 100 / (a + 100) if a > 0 else abs(a) / (abs(a) + 100)

def log_pair(sport, event, market, side, book, odds_entry, odds_close,
             line_entry='', line_close='', notes=''):
    p_e, p_c = american_to_prob(odds_entry), american_to_prob(odds_close)
    clv_p = round((p_c - p_e) * 100, 3)
    clv_a = int(odds_entry) - int(odds_close)
    clv_l = ''
    if line_entry != '' and line_close != '':
        clv_l = round(float(line_entry) - float(line_close), 2)
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    row = {
        'id': str(uuid.uuid4())[:8],
        'ts_entry': now, 'ts_close': now,
        'sport': sport, 'event': event, 'market': market, 'side': side,
        'book': book,
        'odds_entry': odds_entry, 'odds_close': odds_close,
        'line_entry': line_entry, 'line_close': line_close,
        'clv_prob': clv_p, 'clv_american': clv_a, 'clv_line': clv_l,
        'beat_close': 'Y' if clv_p > 0 else ('T' if clv_p == 0 else 'N'),
        'notes': notes,
    }
    with open(JOURNAL, 'a', newline='') as f:
        csv.DictWriter(f, fieldnames=HEADERS).writerow(row)
    print(f\"{row['id']} | {side} | {odds_entry:+d}→{odds_close:+d} | CLV {clv_p:+.3f} pts | beat={row['beat_close']}\")

# --- EDIT THESE ---
log_pair(
    sport='NFL', event='Chiefs @ Bills', market='ML',
    side='Bills', book='DraftKings',
    odds_entry=-130, odds_close=-145,
    notes='backfill from closing board',
)
"
```

## Rollup: Beat-Close Rate Dashboard

```bash
python3 -c "
import csv, os
from collections import defaultdict

JOURNAL = os.path.expanduser('~/.openclaw/clv-journal.csv')
if not os.path.exists(JOURNAL):
    print('No journal. Run init first.'); raise SystemExit(1)

closed = []
pending = 0
with open(JOURNAL) as f:
    for row in csv.DictReader(f):
        if row['odds_close'] in ('', None):
            pending += 1
            continue
        row['clv_prob'] = float(row['clv_prob'])
        closed.append(row)

if not closed:
    print(f'No closed rows yet ({pending} pending).'); raise SystemExit(0)

beats = sum(1 for r in closed if r['beat_close'] == 'Y')
ties  = sum(1 for r in closed if r['beat_close'] == 'T')
avg   = sum(r['clv_prob'] for r in closed) / len(closed)

print('=== CLV Journal Rollup ===')
print(f'Closed:           {len(closed)}  (pending: {pending})')
print(f'Avg CLV:          {avg:+.3f} prob pts')
print(f'Beat-close rate:  {beats}/{len(closed)} ({beats/len(closed):.0%})  ties={ties}')
print()

def rollup(key):
    buckets = defaultdict(list)
    for r in closed:
        buckets[r[key] or '?'].append(r)
    print(f'--- By {key} ---')
    for k, rows in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        b = sum(1 for r in rows if r['beat_close'] == 'Y')
        a = sum(r['clv_prob'] for r in rows) / len(rows)
        print(f'  {k:<12} n={len(rows):<4} beat={b/len(rows):.0%}  avg_clv={a:+.3f}')
    print()

rollup('sport')
rollup('book')
rollup('market')

print('Recent (last 8):')
for r in closed[-8:]:
    print(f\"  {r['id']}  {r['event']:<28} {r['side']:<18} {r['clv_prob']:+.3f}  {r['beat_close']}\")

if avg > 1.0 and beats / len(closed) >= 0.55:
    print()
    print('VERDICT: Positive process — you are beating the close.')
elif avg > -0.5:
    print()
    print('VERDICT: Near-neutral CLV — tighten timing and line shopping.')
else:
    print()
    print('VERDICT: Negative CLV — chase earlier numbers or better books.')
"
```

## Quick Single-Bet CLV (no journal)

```bash
python3 -c "
def clv(odds_entry, odds_close):
    def p(a):
        a = int(a)
        return 100 / (a + 100) if a > 0 else abs(a) / (abs(a) + 100)
    pe, pc = p(odds_entry), p(odds_close)
    pts = (pc - pe) * 100
    print(f'Entry {odds_entry:+d} (p={pe:.4f}) → Close {odds_close:+d} (p={pc:.4f})')
    print(f'CLV: {pts:+.3f} prob pts | American delta: {odds_entry - odds_close:+d}')
    print('Beat close' if pts > 0 else ('Push' if pts == 0 else 'Lost to close'))

clv(-110, -125)
"
```

## Workflow Tips

1. **Log entry immediately** when you bet — do not wait for the result.
2. **Fill close at tip-off / first pitch / kickoff** from the same book (or a consensus close if you track one).
3. **Judge process on CLV**, not on the W/L of any single ticket.
4. Pair with `sports-odds` to capture live prices and with `bet-journal` for stake/ROI.
5. Need ≥50 closed bets before trusting beat-close rate; noise dominates small samples.

## Author

Created by [Ian Alloway](https://github.com/ianalloway) — Data Scientist specializing in sports analytics and ML.

## License

MIT License
