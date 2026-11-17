## Description:

Context Doctor reports an OpenClaw agent session's context usage, token consumption trends, largest tool-output consumers, remaining-turn estimates, and optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check the health of long-running OpenClaw conversations, identify the biggest context consumers, and decide when to compact or reduce tool output. It is intended for session diagnostics and practical context-management guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the skill unintentionally.

Mitigation: Use explicit phrases such as "context doctor" when requesting diagnostics.

Risk: The report may expose session metadata such as token usage, model or cost data, tool-call counts, and large-output rankings.

Mitigation: Enable and share diagnostics only in contexts where this session metadata is acceptable to disclose.

Risk: Heartbeat-based auto-checks can create periodic diagnostic reports when they are not desired.

Mitigation: Avoid heartbeat auto-check configuration unless periodic context-health reporting is intentional.

## Reference(s):

- [Context Doctor on ClawHub](https://clawhub.ai/wavmson/skills/ctx-doctor)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown diagnostic report with concise recommendations and optional shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports session-level metadata such as context usage, token totals, cost data, tool-call counts, and large-output rankings without including conversation content.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
