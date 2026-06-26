# Severity Mapping

How each AWS alert source's severity maps to the normalized
`CRITICAL | HIGH | MEDIUM | LOW | INFORMATIONAL` scale.

## Table of contents

- [Security Hub ASFF](#security-hub-asff)
- [Inspector v2](#inspector-v2)
- [CloudWatch Alarms](#cloudwatch-alarms)
- [Noise filter](#noise-filter)
- [Extending the noise filter](#extending-the-noise-filter)

---

## Security Hub ASFF

Direct mapping from `Severity.Label`:

| ASFF Label      | Normalized       |
|-----------------|------------------|
| `CRITICAL`      | CRITICAL         |
| `HIGH`          | HIGH             |
| `MEDIUM`        | MEDIUM           |
| `LOW`           | LOW              |
| `INFORMATIONAL` | INFORMATIONAL    |

If `Label` is missing, the parser falls back to the numeric
`Severity.Normalized` score (0-100):

- 90-100: CRITICAL
- 70-89:  HIGH
- 40-69:  MEDIUM
- 1-39:   LOW
- 0:      INFORMATIONAL

---

## Inspector v2

Inspector v2 uses a direct label:

| Inspector severity | Normalized       |
|--------------------|------------------|
| `CRITICAL`         | CRITICAL         |
| `HIGH`             | HIGH             |
| `MEDIUM`           | MEDIUM           |
| `LOW`              | LOW              |
| `INFORMATIONAL`    | INFORMATIONAL    |
| `UNTRIAGED`        | INFORMATIONAL    |

`UNTRIAGED` maps to INFORMATIONAL because it represents a finding that
hasn't been scored yet — not a meaningful priority signal on its own.
If you want UNTRIAGED findings to trigger downstream handling, filter
for them explicitly before handing to this skill.

Inspector v2 findings also carry `inspectorScore` (CVSS-derived 0.0-10.0).
The parser extracts this as a separate `inspector_score` field in the
normalized output, useful for threshold-based routing (e.g. "alert on
anything ≥7.5" rather than relying on the categorical label).

---

## CloudWatch Alarms

CloudWatch alarms do not carry severity in the event payload. The parser
emits `INFORMATIONAL` as the default.

The parser does NOT infer severity from alarm names. Name-based
heuristics are unreliable — real-world alarm names contain tokens like
`AlarmHigh` and `AlarmLow` that denote autoscaling direction, not
severity.

To get explicit severity into the pipeline:

- *Tag the alarm with a `severity` tag* (CRITICAL / HIGH / MEDIUM / LOW /
  INFORMATIONAL). Caveat: this parser does NOT read AWS tags — tags are
  not present in the event payload and reading them requires an AWS API
  call. Tag-based enrichment must happen in a separate step (e.g. a
  Lambda that enriches the SNS message before it reaches your webhook).
- *Override downstream.* `incident-triage` applies its own
  classification logic on top of the normalized severity and can upgrade
  urgency based on context (environment, service tier, recent changes).

---

## Noise filter

Some CloudWatch alarm patterns represent routine operational machinery,
not incidents. The CloudWatch parser exits with a skip sentinel for
these:

```json
{
  "skip": "non-incident-alarm",
  "reason": "ecs-target-tracking-autoscaling",
  "alarm_name": "TargetTracking-...-AlarmHigh-...",
  "note": "..."
}
```

`parse-alert.sh` exits code `10` on skip so callers can distinguish skip
from success without parsing JSON.

Current patterns:

| Alarm-name pattern | Reason |
|---|---|
| `TargetTracking-*-AlarmHigh-*` / `TargetTracking-*-AlarmLow-*` | ECS target-tracking autoscaling |
| `awseb-*-AWSEBCloudwatchAlarmHigh-*` / `awseb-*-AWSEBCloudwatchAlarmLow-*` | Elastic Beanstalk default alarms |
| `AutoScaling-*-AlarmHigh-*` / `AutoScaling-*-AlarmLow-*` | EC2 AutoScaling policy alarms |
| `CloudWatchSynthetics-*` | Synthetics canary state changes |

---

## Extending the noise filter

The filter list lives in `scripts/parse-cloudwatch-alarm.sh` in a
`case "$alarm_name"` block. To add patterns for your own noise sources:

1. Fork the skill directory (or install as a local skill).
2. Edit `scripts/parse-cloudwatch-alarm.sh` and add a new pattern:
   ```bash
   case "$alarm_name" in
     # ... existing patterns ...
     my-noisy-pattern-*)
       skip_reason="my-org-scale-event" ;;
   esac
   ```
3. Re-package the skill (`package_skill.py`) and install your fork.

A config-driven noise filter (via `skill.config` or similar) is a
candidate for v0.2. Until then, forking is the path.

### What did not make the list

These patterns were considered and rejected:

- *AWS Console auto-named metric alarms* (e.g. `*-SuccessfulRequestLatency`,
  `*-5xxError`). Too risky — legitimate production alarms may use similar
  suffix conventions. Users whose setup includes these as noise should
  add a tighter pattern (e.g. `*-EC2-*-5xxError`) rather than a broad one.
- *Alarm descriptions containing "Scale Up/Down"*. The description string
  is not present in the EventBridge shape, so name-pattern matching is
  the only portable path.

Be conservative when adding new patterns — filtering out a real incident
signal is worse than posting a low-severity non-event.
