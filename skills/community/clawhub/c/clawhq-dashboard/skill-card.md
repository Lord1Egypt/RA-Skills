## Description:

Reports AI agent status, task context, completions, and heartbeat events to the ClawHQ dashboard for real-time monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachmael](https://clawhub.ai/user/zachmael)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to connect an agent to ClawHQ so status, current task summaries, completion events, and heartbeats appear in a dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent names, statuses, task descriptions, and heartbeat information are sent to ClawHQ and may contain sensitive operational context.

Mitigation: Avoid including secrets or client-confidential details in task summaries before reporting status.

Risk: The ClawHQ API key authorizes reporting to the dashboard and could be misused if exposed.

Mitigation: Store the API key as a protected environment variable, use a dedicated key, and revoke or rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zachmael/skills/clawhq-dashboard)
- [ClawHQ dashboard](https://app.clawhq.co)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with Bash and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWHQ_API_KEY and sends agent status, task summaries, and heartbeat information to ClawHQ.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
