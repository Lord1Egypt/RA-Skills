## Description:

Automates daily ClawHub skill updates at 04:00 with before-and-after version comparison and update reports sent through OpenClaw Gateway Cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dillardarchie](https://clawhub.ai/user/dillardarchie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a scheduled ClawHub update job, compare installed skill versions before and after the run, and send a concise update report to Feishu or Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sets up an unattended daily job that can update all installed ClawHub skills.

Mitigation: Use a pinned and vetted ClawHub CLI, limit updates to approved skills where possible, and require manual approval before applying updates in sensitive environments.

Risk: The scheduled job can send skill and version summaries to an external messaging recipient.

Mitigation: Use a reporting destination approved for the environment and review whether skill inventory or version information is appropriate to share there.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dillardarchie/skills/auto-updater-gateway-cron)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks, configuration values, and report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cron schedule, timezone, delivery-channel placeholders, and before/after version comparison guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
