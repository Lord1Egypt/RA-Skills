## Description:

Mechanism conflict detection and coordination for AI assistant systems. Automatically detects crontab conflicts, systemd service conflicts, script overlaps, and log path inconsistencies. Use for maintaining system harmony and preventing internal conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfredming-2026](https://clawhub.ai/user/alfredming-2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw-related crontab entries, user services, scripts, logs, and documentation for conflicting or inconsistent mechanisms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script sends system-status summaries to a hard-coded Feishu recipient.

Mitigation: Remove or configure the Feishu send line before scheduled or shared-environment use.

Risk: The script sources an unverified helper outside the package.

Mitigation: Package, review, or pin the expected task-utils.sh helper before execution.

Risk: The script inspects local scheduling, user services, scripts, logs, and docs, then writes a report under the OpenClaw workspace.

Mitigation: Run it only in environments where that inspection and report writing are expected and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alfredming-2026/skills/conflict-coordination)
- [Publisher profile](https://clawhub.ai/user/alfredming-2026)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown reports, status summaries, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local conflict report and send a status summary when its bundled script is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
