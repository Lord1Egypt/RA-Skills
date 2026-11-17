## Description:

Automatically moves yesterday's Obsidian daily note into a past-days/ archive folder using the Obsidian CLI move command to preserve wiki-links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madebydia](https://clawhub.ai/user/madebydia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to schedule nightly Obsidian vault maintenance that archives the prior day's daily note while preserving wiki-links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies an Obsidian vault by moving a daily note and updating wiki-links.

Mitigation: Enable it only after confirming the vault's daily-note naming format, archive folder, and Obsidian CLI behavior match the documented assumptions.

Risk: A missing or mismatched archive folder or note naming convention can cause the scheduled task to skip the intended note.

Mitigation: Create the past-days/ folder and verify the MM-DD-YYYY DayOfWeek.md naming convention before enabling cron execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/madebydia/skills/archive-daily-note)
- [Project homepage](https://github.com/madebydia/archive-daily-note)
- [OpenClaw](https://openclaw.app)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command references and cron configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the obsidian binary and an Obsidian vault using the documented daily-note naming convention and past-days/ archive folder.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
