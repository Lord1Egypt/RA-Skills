## Description:

Feishu Cache Guardian checks and restores the OpenClaw Feishu plugin probe cache settings to 60 minutes so health checks do not quickly exhaust Feishu API quota.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhs0430-sudo](https://clawhub.ai/user/zhs0430-sudo)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators running OpenClaw with the Feishu extension use this skill to inspect and repair probe.ts cache TTL settings after upgrades or plugin overwrites, then restart Gateway when a repair is applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify an installed OpenClaw Feishu plugin file.

Mitigation: Review the script and run it manually first; keep a recovery plan or backup for the modified probe.ts file.

Risk: The skill can restart OpenClaw Gateway after applying a fix.

Mitigation: Run it during an acceptable maintenance window and be prepared to restart Gateway manually if automation fails.

Risk: Scheduled use can repeatedly apply local changes if the skill directory or target installation is not protected.

Mitigation: Avoid cron until the skill directory is protected and the behavior has been validated in the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhs0430-sudo/skills/feishu-cache-guardian)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to modify a local OpenClaw Feishu probe.ts file and restart OpenClaw Gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
