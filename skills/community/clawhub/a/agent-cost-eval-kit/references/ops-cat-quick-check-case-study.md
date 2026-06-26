# ops_cat Quick Check — Case Study (2026-05-30)

## What happened

User ran `quick check agent cost for ops_cat`.

Real session data from `openclaw sessions --agent ops_cat --limit 5 --json`:

```
direct       | gpt-5.4         | total= 67456 | in= 1024 out=  594 | cache=65838 (97%)
spawn-child  | MiniMax-M2.7    | total=  7350 | in= 7338 out= 1011 | cache=-999 (N/A)
cron         | MiniMax-M2.7    | total=  9339 | in= 4724 out=  492 | cache= 4123 (44%)
```

Key insight: The direct gpt-5.4 session had 97% cacheRead. Incremental tokens = 1,024 + 594 = 1,618. This is NOT a cost regression.

## Output produced (v2.2.1 expected)

```
Status: Watch

Plain-English conclusion:
There is no clear proof that ops_cat became more expensive. The gpt-5.4 direct session
has high totalTokens, but most appears to be cacheRead, so it should not be treated as
a direct cost regression. Mixed direct / cron / subagent sessions are not comparable.

Do now:
Watch only ops_cat direct sessions for the next 24 hours.

Don't do now:
Do not change routing, switch models, or run new operational tasks just to create a baseline.
```

## Technique: Parsing openclaw JSON in execute_code

`terminal()` with shell pipes (`| python3 -c ...`) times out on `openclaw sessions --json`. Use `execute_code` with `subprocess.run` instead:

```python
import json, subprocess

result = subprocess.run(
    ['openclaw', 'sessions', '--agent', 'ops_cat', '--limit', '5', '--json'],
    capture_output=True, text=True, timeout=20
)
d = json.loads(result.stdout)
for s in d['sessions']:
    total = s['totalTokens']
    inp = s.get('inputTokens', 0)
    out = s.get('outputTokens', 0)
    cache = total - inp - out
    print(f"kind={s['kind']}, cache%={cache*100//total if total else 0}%")
```

## CacheRead dominance rule

When `cacheRead / totalTokens > 80%` on a direct session:
- High totalTokens is misleading — most tokens are cached context, not new generation
- Incremental cost = inputTokens + outputTokens only
- Do NOT treat as a cost regression
- Status should be **Watch**, not "Not Comparable Yet"