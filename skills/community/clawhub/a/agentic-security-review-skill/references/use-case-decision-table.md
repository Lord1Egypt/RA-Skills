# Use-Case Decision Table

| Scenario | Primary Artifact | Supporting Artifact |
| --- | --- | --- |
| New agent launch | `agentic-risk-intake` | `production-readiness-security-checklist` |
| New tool integration | `tool-permission-inventory` | `sandbox-least-privilege-checklist` |
| Sensitive/client/personal data access | `data-exposure-review` | `data-retention-review` |
| Email, calendar, chat, filesystem, payment, or production action | `external-action-review` | `approval-gate-audit` |
| New API key, token, service account, or secret | `credential-secret-handling-checklist` | `logging-auditability-review` |
| Retrieval/RAG/indexed source added | `retrieval-source-trust-review` | `prompt-injection-test-plan` |
| Model, provider, prompt, runtime, or safety setting changed | `model-provider-configuration-review` | `red-team-test-report` |
| Package, script, dependency, or vendor added | `dependency-supply-chain-review` | `sandbox-least-privilege-checklist` |
| Need evidence for launch decision | `launch-blocker-checklist` | `security-signoff-memo` |
| Need backout path | `rollback-plan` | `production-readiness-security-checklist` |
| Incident or near miss | `incident-response-plan` | `human-escalation-procedure` |
| Adversarial testing complete | `red-team-test-report` | `security-signoff-memo` |

Choose the narrowest artifact that answers the immediate decision. Add supporting artifacts when the decision depends on access, data handling, external actions, logs, or rollback evidence.
