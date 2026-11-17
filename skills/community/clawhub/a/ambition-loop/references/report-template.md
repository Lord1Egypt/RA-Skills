# Templates

## Plan card (Step 6)
```
Fit: ESCALATE — <tell>
You asked for: <literal ask>
Worth doing:  <elevated version>, because <reason>
Axes: <Altitude/Depth/Range> — <tell>

| Asked (floor) | Ambitious target | Judge | Pass line | Cost/needs |
|---|---|---|---|---|

Will touch: <files/systems/data>
Gates: none | G<n> <action> — awaiting approval
```

## Approval plan (Step 6, when a gate fires)
```
Gates fired: G<n> <name>, ...

| # | Gated action | What exactly happens (who/what is affected) | Cost / risk | Options |
|---|---|---|---|---|
| 1 | <e.g. email 5,000 subscribers> | <recipients, content, timing> | <reputation, unsubscribes, spam risk> | approve / smaller test (e.g. 200 opted-in) / skip |

Prepared without crossing a gate: <drafts, segment lists, dry-run output, analysis>
Not done and not attempted: <the gated actions>; no credentials were searched for.
Gates: G<n> <action> — awaiting approval
```

## Final report (Step 10)
Keep these headings (English or Chinese). `scripts/check_report.py` looks for them.

```
## Target comparison
| Target | Asked (floor) | Ambitious | Achieved | Met? |
|---|---|---|---|---|

## Verification
| Claim | Judge | Result | Evidence |
|---|---|---|---|
(Result is PASS / FAIL / UNVERIFIED. Self-assessment is never evidence.)

## Gaps
- <what fell short, by how much, and why>

## Next moves
- <the concrete next step that would close each gap>

## Gated or skipped
- <actions that needed approval, were denied, or were left out; "none" if none>
```
Optional: a "Durable workflow" section if the work could keep running without the human.
