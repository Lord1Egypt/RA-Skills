## Description:

Show per-message token usage (tokens, cache %, duration, throughput, model, cost) under each assistant message in the OpenClaw Control UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhughyn](https://clawhub.ai/user/xhughyn)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to add per-message token and cost information to assistant replies in the browser Control UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation patches OpenClaw Control UI files and may request passwordless sudo access.

Mitigation: Review the JavaScript and shell scripts, verify the target Control UI directory, and run apply.sh manually without sudo unless you trust the package.

Risk: Optional cron or heartbeat reapplication keeps the UI patch in place after updates.

Mitigation: Avoid automated reapplication unless you explicitly want the patch to persist; use remove.sh to uninstall it.

## Reference(s):

- [Control UI Usage Badge on ClawHub](https://clawhub.ai/xhughyn/skills/control-ui-usage-badge)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adds a usage line to eligible assistant messages in the browser Control UI; reported metrics depend on available usage data.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
