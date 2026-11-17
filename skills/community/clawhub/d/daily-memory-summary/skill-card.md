## Description:

Daily Memory Summary reads the current day's clipboard and notification records from a computer_io memory folder and writes a dated daily memory summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gift-is-coding](https://clawhub.ai/user/gift-is-coding)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to consolidate daily clipboard and notification logs into a dated Markdown memory file. Because the skill handles sensitive activity logs on a schedule, it should be used only in private workspaces with consent, review, redaction, and file-permission controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can archive passwords, tokens, private messages, or business notifications when those values appear in clipboard or notification logs.

Mitigation: Use only in a private workspace with explicit consent, review generated summaries, add redaction controls, and restrict file permissions on memory outputs.

Risk: The skill parses contact-like information from notification data without clear disclosure in the skill description.

Mitigation: Document or remove contact-extraction behavior before scheduling, and confirm that collection is appropriate for the workspace.

Risk: The script previews generated memory content to stdout, which can expose sensitive clipboard or notification data in logs.

Mitigation: Remove the stdout preview or run only in an environment where terminal output and task logs are access controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gift-is-coding/skills/daily-memory-summary)
- [Publisher profile](https://clawhub.ai/user/gift-is-coding)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown file with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes memory/YYYY-MM-DD.md from the latest clipboard and notification Markdown inputs for the current day.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
