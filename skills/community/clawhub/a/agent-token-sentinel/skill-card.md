## Description:

Agent Token Sentinel helps monitor AI-agent API usage, token burn rates, and session quotas so runaway loops or excessive reasoning can be stopped before they exceed budget limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to add cost and quota guardrails around AI-agent sessions, including loop detection, budget caps, and quota alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A floating npx package may change between runs and is not locally reviewable from the artifact.

Mitigation: Use a pinned, audited OpenClaw package version and review the resolved package before deployment.

Risk: Budget enforcement that can terminate processes may interrupt legitimate agent work or be difficult to reverse.

Mitigation: Run with least privilege, document what the skill can read and terminate, and define a clear disable or rollback procedure before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmstudio667-commits/skills/agent-token-sentinel)
- [ClawHub publisher profile](https://clawhub.ai/user/tmstudio667-commits)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on configuring budget caps, monitoring token consumption, and responding to quota or loop alerts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
