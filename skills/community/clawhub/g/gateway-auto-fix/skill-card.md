## Description:

Automatically monitor OpenClaw gateway status and fix when RPC probe fails. Uses OpenClaw cron system - just install and it works!

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwcalvin](https://clawhub.ai/user/nwcalvin)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to monitor an OpenClaw gateway and automatically run OpenClaw repair and restart commands when the RPC probe reports failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation can repeatedly change OpenClaw gateway configuration and restart the gateway without per-run approval.

Mitigation: Install only when unattended gateway repair is intended; review and run the included local scripts before deployment, pin installer versions, and add safeguards such as retry limits, locking, backoff, alerting, and private user-owned logs.

Risk: A one-minute repair loop can disrupt service or mask recurring gateway failures.

Mitigation: Set an appropriate schedule, monitor the repair log, and require operator review for repeated failures before enabling continuous automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nwcalvin/skills/gateway-auto-fix)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and shell commands for OpenClaw cron-based gateway repair.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
