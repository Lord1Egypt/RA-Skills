# Output Templates

## Standard debug report

```text
DEBUG REPORT
Failure:      [exact issue]
Root cause:   [specific cause]
Proof:        [test/log/code evidence]
Fix:          [minimal change]
Verified:     [command/test/repro result]
Prevention:   [test/monitoring/doc/learning, or "not needed" + why]
Remaining:    [risk/blocker, or "none known"]
Next optimization: [optional meaningful improvement potential]
```

## Incident snapshot

```text
INCIDENT SNAPSHOT
Impact:       [who/what is affected]
Severity:     [low/medium/high/critical + why]
Started:      [time/commit/deploy if known]
Evidence:     [logs/status/metrics; redacted]
Hypothesis:   [testable cause]
Stabilize:    [rollback, feature flag, hotfix, monitor, no-op]
Next action:  [one concrete diagnostic action]
```

## Hypothesis update

```text
HYPOTHESIS
Current:      [specific suspected cause]
Test:         [how to prove/disprove]
Result:       [passed/failed + evidence]
Decision:     [narrow further / fix / new hypothesis]
```

## After 3 failed fixes

```text
ESCALATION REPORT
What failed:      [3 attempted fixes]
Why insufficient: [evidence each did not address root cause]
Known facts:      [confirmed evidence]
Unknowns:         [missing data]
Recommended next: [one safer diagnostic path]
```

## User-facing concise summary

```text
Gefunden: [root cause in one sentence]
Gefixt: [minimal change]
Beweis: [test/log result]
Offen: [remaining risk or none]
```
