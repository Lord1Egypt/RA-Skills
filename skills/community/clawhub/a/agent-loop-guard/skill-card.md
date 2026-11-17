## Description:

Analyzes a supplied agent action trace for step-limit and repeated-action patterns, then reports a risk level, diagnosis, and suggested intervention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can inspect sanitized run traces for excessive step counts or repeated actions, then use the resulting diagnosis to decide whether to intervene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied script analyzes traces and suggests a breaker, but does not enforce path and symlink restrictions, redact diagnostics, or stop an agent automatically.

Mitigation: Use sanitized traces within an independently enforced sandbox with path and symlink restrictions and diagnostic redaction; define the scope of any external stopping mechanism.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zhaoxinghua09-cell/skills/agent-loop-guard)
- [Project homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Plain-text or JSON trace analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports trace-derived step counts, risk labels, diagnoses, and suggested interventions; it does not stop agents automatically.]

## Skill Version(s):

1.0.10 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
