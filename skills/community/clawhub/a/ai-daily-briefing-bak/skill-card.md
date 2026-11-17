## Description:

Start every day focused with a daily briefing that summarizes overdue tasks, today's priorities, calendar context, and recent meeting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitsarp](https://clawhub.ai/user/gitsarp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and productivity-focused teams use this skill to generate concise morning, weekly, overdue-item, and calendar briefings from local task lists, meeting notes, calendar context, and optional memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings may summarize sensitive task, meeting, calendar, or memory/profile content.

Mitigation: Use explicit briefing commands, review or disable sensitive context sources, and avoid generating briefings in shared-screen or shared-chat contexts unless the output is safe to reveal.

Risk: Broad conversational triggers can cause the agent to gather personal or work context when the user did not intend a full briefing.

Mitigation: Prefer direct trigger phrases such as "daily briefing" and confirm context sources before enabling persistent task, meeting, calendar, or memory files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gitsarp/skills/ai-daily-briefing-bak)
- [Publisher Profile](https://clawhub.ai/user/gitsarp)
- [Creator Homepage](https://jeffjhunter.com)
- [Quick Start](artifact/examples/quick-start.md)
- [Example Output](artifact/examples/output-example.md)
- [Briefing Preferences Template](artifact/assets/PREFERENCES-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style briefing text with optional YAML preference examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single concise briefing response and skips empty sections when source data is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
