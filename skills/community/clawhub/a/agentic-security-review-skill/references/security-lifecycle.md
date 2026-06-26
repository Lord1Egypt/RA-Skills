# Security Review Lifecycle

## 1. Intake

Define the workflow, business purpose, users, environments, data classes, tools, credentials, retrieval sources, external actions, and known constraints. Use `agentic-risk-intake`.

## 2. Access And Data Review

Inventory tool permissions, secrets, sensitive data flows, retention, dependencies, and sandbox boundaries. Use the access and data artifacts before granting production access.

## 3. Control Review

Review approval gates, external actions, prompt-injection behavior, retrieval trust, model/provider configuration, logging, and auditability. Make launch blockers explicit.

## 4. Launch Readiness

Confirm mitigations, owners, evidence, monitoring, rollback, incident response, and signoff. Do not mark ready when blockers or unknown critical controls remain.

## 5. Change Review

Re-run the relevant artifact when tools, permissions, credentials, retrieval sources, models, dependencies, data classes, or external actions change.

## 6. Post-Incident Review

Use incident response, escalation, red-team, and signoff artifacts to document what happened, what changed, what remains open, and who approved resuming operations.
