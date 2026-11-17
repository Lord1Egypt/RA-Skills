# POC run input guide

## Readiness check before running

| Input | Minimum Requirements | Not Ready Processing |
|---|---|---|
| POC Contract | Goal, baseline, threshold, decision maker, stopping condition | Return to Stage 2 |
| PRD | Acceptance, scope, roles, data, exception scenarios | Return to Stage 3 |
| Deployment package | Environment, version, permissions, observation, rollback | Return to Stage 4 |
| Skills/Protocols | Behaviors, Tools, Guardrails, Assessment Cases | Return to Stage 5 or Instructions Not Applicable |
| Test data | Source, representativeness, permission, sensitivity level, version | Blocking runs or limiting conclusions |
| Participants | Real users, business confirmers, technical support | Rescheduling, not replaced by FDE self-assessment |
| Operational support | Incident owners, problem channels, escalation and stop permissions | Pre-operational patching |

## Data representativeness

Check timeframe, user type, task frequency, difficulty, language/format, boundaries, and failure samples. When using only ideal examples, the conclusion must be labeled as a "controlled demonstration" and cannot be written as a real-life workflow verification.

## Freeze list

```markdown
- Contract/PRD/Architecture Version:
- Skills, prompt words and configuration versions:
- Model, tool and interface versions:
- Data set and gold-labeled version:
- Evaluator/Rating Scale version:
- Environment and permissions snapshot:
- Running time box, participants and owners:
```
