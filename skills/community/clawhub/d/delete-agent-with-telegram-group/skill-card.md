## Description:

Safely and thoroughly deletes an OpenClaw agent and related artifacts, including workspace files, agent configuration, bindings, Telegram routing configuration, optional dedicated Telegram group deletion guidance, and cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheetaa](https://clawhub.ai/user/sheetaa)

### License/Terms of Use:


## Use Case:

OpenClaw operators and developers use this skill when they need an agent removed from local OpenClaw configuration, workspace files, Telegram routing, and scheduled jobs while preserving dry-run and confirmation checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local cleanup can permanently remove OpenClaw agent directories, workspace folders, Telegram routing entries, and cron jobs.

Mitigation: Run the dry-run first, inspect the planned removals, verify the exact workspace path, and keep generated backups before executing deletion.

Risk: The authoritative security summary flags the deletion checks as too loose for the possible impact.

Mitigation: Avoid workspace deletion unless the OpenClaw configuration is trusted, and confirm the target path is under the user home and matches the expected claw-* workspace pattern.

Risk: Dedicated Telegram group deletion is irreversible and may affect group members.

Mitigation: Require a separate explicit confirmation for browser or session control, then report the final group status as deleted, left-only, or pending-manual.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheetaa/skills/delete-agent-with-telegram-group)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires dry-run review and explicit confirmations before destructive local deletion or Telegram group deletion.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
