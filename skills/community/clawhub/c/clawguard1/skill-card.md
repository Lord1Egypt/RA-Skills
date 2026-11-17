## Description:

ClawGuard governance layer that must run before any SQL, file-system, or API write. Use evaluate_action(action_type, justification, risk_level) to log/authorize actions and get_audit_report(limit) to review the SQLite-based audit ledger. Blocks risk_level >= 4 automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mithileshgau](https://clawhub.ai/user/mithileshgau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to require logged governance checks before write-capable SQL, file-system, or API actions and to review recent decisions from a persistent audit ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims session-wide control over write-capable actions, which can create false assurance if actions bypass the governance call.

Mitigation: Use it only in workflows where write-capable actions are explicitly routed through evaluate_action and blocked results are honored.

Risk: Action types and justifications are persisted in a SQLite audit ledger and may expose sensitive context if users include secrets or personal data.

Mitigation: Keep secrets and sensitive personal data out of justifications, restrict access to clawguard.db, and define retention controls before real governance use.

Risk: Redis-based velocity checks introduce a network dependency and use REDIS_URL or a localhost default.

Mitigation: Contain, remove, or explicitly configure Redis unless velocity throttling is required for the deployment.

Risk: The package uses range-based dependency versions for governance-relevant runtime components.

Mitigation: Pin and review dependencies before relying on the skill for production governance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mithileshgau/skills/clawguard1)
- [ClawGuard Governance Protocol](GUIDANCE.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON-style tool responses and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns approval status, block messages, optional Civic escalation flags, and audit ledger rows.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
