## Description:

Daily Tutor retrieves new study items from a local JSON study list, supports arbitrary subject data, and tracks learned items so sessions do not repeat content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buiphuc](https://clawhub.ai/user/buiphuc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch daily learning items from a local study list, present them for review, and optionally create a short practice quiz through a configured Quizbuild MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Study data can include secrets, confidential notes, or proprietary material that may be sent to the configured external Quizbuild MCP service during optional quiz generation.

Mitigation: Keep sensitive material out of data/data.json when using Quizbuild, and review the configured MCP service before sending generated quiz content.

Risk: The skill records learning progress in a local file-backed tracker, so local data changes determine which items are shown or skipped.

Mitigation: Review data/data.json and data/config.json before use, and manage data/learned_items.json intentionally when resetting or preserving study progress.

## Reference(s):

- [Daily Tutor ClawHub page](https://clawhub.ai/buiphuc/skills/daily-tutor)
- [Data format examples](references/EXAMPLES.md)
- [Project README linked by artifact](https://github.com/buiphuc/daily-tutor#readme)
- [Quizbuild MCP endpoint](https://api.quizbuild.com/mcp/quizbuild)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads study items from local JSON, writes local progress state, and may provide quiz-generation guidance when Quizbuild is configured.]

## Skill Version(s):

1.0.4 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
