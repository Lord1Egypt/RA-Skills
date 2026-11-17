## Description:

Auto Monitor guides an agent to proactively monitor server health, report normal status, and alert with suggestions when disk, memory, CPU, network, or process checks look abnormal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent check common server health indicators, summarize normal status, and report abnormal conditions with suggested next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill asks the agent to monitor proactively and perform immediate automatic repairs without clear user approval or limits.

Mitigation: Require explicit approval before repair actions and use the skill for reporting and recommendations unless narrow allowlists, logging, rollback guidance, and clear enable or disable controls are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/auto-monitor-zhouli)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown status reports, alerts, and suggested remediation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise normal reports and more detailed anomaly alerts.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
