## Description:

Automatically keep OpenClaw and installed workspace skills up to date using native OpenClaw commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zdy2019](https://clawhub.ai/user/zdy2019)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure recurring skill maintenance, update checks, and optional core update routines with native OpenClaw commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A cron schedule or timezone may run updates at an unintended time.

Mitigation: Confirm the schedule, timezone, and delivery session before creating a recurring update job.

Risk: Automatic OpenClaw core runtime updates can change the runtime more broadly than skill-only updates.

Mitigation: Prefer skills-only automatic updates unless the user explicitly opts into recurring OpenClaw core updates.

Risk: Repeated broad skill updates may encounter ClawHub remote rate limits.

Mitigation: Prefer gentle per-skill updates and stop the run with a clear explanation if a 429 rate-limit response appears.

Risk: Some update or scheduling commands may require user approval or elevated access.

Mitigation: Stop and ask before proceeding when a command requires approval or elevated access.

## Reference(s):

- [OpenClaw Auto-Updater Cron Examples](references/cron-examples.md)
- [Notes for the OpenClaw Auto-Updater Skill](references/notes.md)
- [Draft release notes for next public update](references/release-notes-draft.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and compact text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron schedules and update reports; automatic OpenClaw core runtime updates are opt-in.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
