---
name: anomaly-watcher
description: "Continuous behavioral monitoring for OpenClaw agents. Detect anomalies in command patterns, resource usage, and skill invocations against established baselines."
metadata: {"openclaw":{"emoji":"👁️","category":"blue-team"}}
---

# Anomaly Watcher — Behavioral Baseline Monitor

## Purpose

Establish a behavioral baseline for the agent and continuously monitor for deviations that may indicate compromise, misconfiguration, or abuse.

## Integration

Always-on monitoring via hooks:
- `PostToolUse` — log every tool invocation
- `UserPromptSubmit` — log input patterns
- `PostSkillExecution` — log skill results

## Monitored Metrics

| Metric | Baseline Unit | Alert Threshold |
|--------|---------------|-----------------|
| Command exec frequency | per hour | >2σ from 7-day avg |
| File access patterns | unique paths/hour | >2σ |
| Network request volume | requests/hour | >2σ |
| Skill invocation frequency | per skill per hour | >2σ |
| Token consumption rate | tokens/hour | >2σ |
| Error rate | errors/hour | >2σ |
| Memory write patterns | writes/hour | >2σ |
| Cross-session messages | messages/hour | >2σ |
| New file creation rate | files/hour | >2σ |
| Unique external domains | domains/hour | >2σ |

## Anomaly Detection Algorithm

1. **Collect** — append each action to `.security/baseline/metrics.jsonl`
2. **Baseline** — rolling 7-day average and standard deviation per metric
3. **Compare** — current window (1 hour) vs baseline
4. **Classify**:
   - `NORMAL` — within 1σ
   - `ELEVATED` — between 1σ and 2σ
   - `ANOMALOUS` — between 2σ and 3σ
   - `CRITICAL` — above 3σ or matches known attack signature
5. **Alert** — based on classification

## Alert Actions

| Classification | Action |
|---------------|--------|
| NORMAL | No action |
| ELEVATED | Log to anomaly.jsonl |
| ANOMALOUS | Log + notify human via preferred channel |
| CRITICAL | Log + notify + recommend pause (human decides) |

## Known Attack Signatures

- Sudden spike in file reads across many directories → possible reconnaissance
- Outbound to new external domain + high data volume → possible exfiltration
- Rapid skill installs from ClawHub → possible supply chain attack
- Memory writes with encoded content → possible persistence attempt

## Guardrails

- Monitoring is strictly read-only — never modifies agent behavior
- Baseline calibration requires minimum 48 hours of data
- False positives are tracked in `.security/false-positives.jsonl`
- Baseline resets require human approval
- The watcher itself has no network access (local analysis only)
