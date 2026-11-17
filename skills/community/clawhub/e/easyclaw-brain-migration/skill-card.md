## Description:

Migrate EasyClaw workspace-level behavior into a new OpenClaw workspace by reporting, staging, and selectively importing legacy brain files with reviewable backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjingh](https://clawhub.ai/user/sjingh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when moving EasyClaw workspace memory, operating rules, heartbeat notes, and context-management materials into an OpenClaw workspace. It helps them inspect existing files, stage legacy content for review, and optionally import memory without replacing active prompt files wholesale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Legacy EasyClaw memory and prompt files may contain sensitive workspace data or stale instructions.

Mitigation: Run the report and staging workflow first, then manually review staged files before merging them into active OpenClaw instructions.

Risk: Using --import-memory can replace active MEMORY.md and make old instructions persistent in future sessions.

Mitigation: Avoid --import-memory unless the operator intentionally accepts persistent migration; rely on the script's backup behavior and review the result immediately.

Risk: Old launchd schedules and helper scripts may not match current OpenClaw automation expectations.

Mitigation: Rebuild automation as OpenClaw heartbeat or cron behavior instead of blindly copying legacy plists or wrappers.

## Reference(s):

- [EasyClaw Brain Migration Map](artifact/references/mapping.md)
- [ClawHub skill page](https://clawhub.ai/sjingh/skills/easyclaw-brain-migration)
- [Publisher profile](https://clawhub.ai/user/sjingh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated migration reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stage files under imports/easyclaw and may copy memory files when explicitly run with --import-memory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
