# Example (GOOD) — the same procedure, atomic

The same Airbnb multicalendar task from `bad-mega-script-stall.md` — reach
June 2027 in a virtualized, lazily-loaded calendar grid and act on a target
date — executed the DecomTangle way. Every call is one verb; every result is
read before the next call is chosen. This exact shape completed successfully
on the same local model that stalled on the mega-script version.

Tool endpoints shown are ClawBridge-style (`/tools/browser/*`); the shape
applies to any browser tool surface.

## The call sequence

**Call 1 — navigate** (one verb: open the page)

```
POST /tools/browser/navigate   {"url": "https://www.airbnb.com/multicalendar"}
```

*Observe:* response says loaded. Nothing else attempted.

**Call 2 — snapshot** (one verb: look)

```
GET /tools/browser/snapshot
```

*Observe:* find the month selector ref (`combobox "Select a month to view"
[ref=e12]`). Decision made from the observation: the selector exists → select.

**Call 3 — select the month** (one verb: choose "June 2027")

```
POST /tools/browser/action     {"action": "select", "args": ["e12", "June 2027"]}
```

*Observe:* accepted. The grid animates and lazy-loads — arrival is NOT
assumed (Rule 4: attempted ≠ confirmed).

**Calls 4..k — poll, one read per call** (one verb each: look)

```
GET /tools/browser/snapshot | grep -m2 "2026\|2027"   → June 2026 visible, keep going
GET /tools/browser/snapshot | grep -m2 "2026\|2027"   → January 2027, keep going
GET /tools/browser/snapshot | grep -m2 "2026\|2027"   → January 2027 — stalled
```

(Poll reads are *bounded* — the read-side pipe filter keeps each result to the
one fact needed, per the giant-read anti-pattern. Pacing between polls is a
standalone wait as its own call — e.g. `sleep 8` alone — never a
sleep-and-act script.)

*Each poll is its own call and its own decision.* When the visible month
stops advancing for several polls, the *decision* is to re-fire the select —
a judgment no scripted loop could have made:

**Call k+1 — re-fire the select**

```
POST /tools/browser/action     {"action": "select", "args": ["e12", "June 2027"]}
```

**Calls k+2.. — resume polling** until the target cell's label is present.
Record the observed label — that is the **before-state**.

**Call m — act on the date** (one verb: click the cell)

The click needs a JavaScript event-dispatch payload — a script full of its own
quotes, destined for a JSON body. Inlined, that is quoting depth ≥ 2: the
Rule-5 tripwire. So it's TWO calls, not one inline-quoted call:

```
write file /tmp/click.json     {"script": "(() => { …event dispatch JS… })()"}
```

(A write tool takes raw content — no shell escaping exists to get wrong.)

```
exec: curl -s -X POST -H "Authorization: Bearer $TOKEN" \
      -d @/tmp/click.json http://<bridge-host>:3201/tools/browser/eval
```

This tool surface has no dedicated "eval" action endpoint, so a shell-out curl
with a **file payload** is the correct Rule-3 fallback here — the native
endpoints (navigate/action/snapshot) stay native, and the one generic call
carries no inline payload. Its quoting depth within the command is 1 (quoted
header tokens only).

*Observe:* result says `CLICKED June 16, 2027…` — the click was **attempted**.

**Calls m+2.. — verify by fresh load** (Rule 4 — and verification is itself a
multi-call procedure)

```
POST /tools/browser/navigate   {"url": "https://www.airbnb.com/multicalendar"}
```

A fresh load lands on the *current* month — in a virtualized grid the June
2027 cell is not in the DOM yet. So the verification leg **repeats the
select → poll sub-procedure** (calls 3..k, same shape) until the target month
is present, and only then re-reads the target cell's label with a targeted
eval (payload-to-file again; not a full snapshot). Compare to the
before-state: only now is the action **confirmed**, and the report to the
operator includes before-state, action, and verified after-state.

## Why this shape wins

- **~18 small calls instead of 1 giant one** — and it completes, because
  every emission is trivially parseable (quoting depth ≤ 1 within every
  argument value, per the tripwire metric).
- Every stall, mis-load, or animation hiccup was caught at the moment it
  happened, by observation, and answered with a local decision (re-fire,
  re-poll) instead of a blind script marching on.
- When one call failed mid-procedure in live testing, the failure was local:
  fix that call, continue — no ambiguity about which prior steps had executed.
- The operator got milestone reports, not silence.
