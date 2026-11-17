## Description:

Check AI token usage, quotas, and costs across Anthropic and other providers using Anthropic OAuth usage data and OpenClaw session logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bshandley](https://clawhub.ai/user/bshandley)

### License/Terms of Use:


## Use Case:

Developers and AI tool users use this skill to inspect Anthropic quota, token usage, request counts, and usage costs across local Claude Code and OpenClaw activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Claude Code OAuth credentials and OpenClaw session logs to generate usage reports.

Mitigation: Run it only when account usage reporting is intentionally requested, and review the credential and session-log paths before installation or execution.

Risk: Recurring heartbeat or cron-style use may repeatedly access local credentials and send authenticated usage requests to Anthropic.

Mitigation: Avoid unattended recurring execution unless the operator has approved the credential access pattern and network request behavior.

## Reference(s):

- [AI Usage ClawHub listing](https://clawhub.ai/bshandley/skills/ai-usage)
- [Anthropic OAuth usage endpoint](https://api.anthropic.com/api/oauth/usage)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Terminal report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quota utilization, reset timing, model-level token counts, request counts, and cost totals when the required local credentials and logs are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
