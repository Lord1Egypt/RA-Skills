## Description:

Track per-project Claude usage estimates and local GPU budgets, preview admission, atomically reserve capacity, and reconcile actual usage with a local dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Butler to check local agent and GPU budget posture, reserve GPU capacity before authorized compute launches, and reconcile measured usage afterward. It is intended for local, single-user project-budget custody with explicit operator configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local ledgers, transcripts, account caches, machine inventories, tokens, and local paths may contain sensitive information.

Mitigation: Use a dedicated private BUTLER_ROOT, keep state out of public packages and issues, and enable transcript scanning, local process inspection, or SSH collection only with explicit authorization.

Risk: The dashboard is a local, single-user interface with no remote authentication layer.

Mitigation: Keep the web port bound to loopback and do not expose it through a network or unauthenticated reverse proxy.

Risk: Gate checks and cached provider reports can be stale or advisory.

Mitigation: Reserve capacity with a stable idempotency key before authorized launches and reconcile measured usage after terminal outcomes.

## Reference(s):

- [Accounting contract](references/accounting.md)
- [ClawHub Skill Page](https://clawhub.ai/antreasantoniou/skills/butler-agent-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown/text guidance with CLI commands and local dashboard instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory unless the actual execution path follows the gate and reservation workflow.]

## Skill Version(s):

1.0.0 (source: release evidence and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
