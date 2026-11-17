## Description:

Daily Memory Keeper helps an agent archive memory files by date, search retained memories by keyword, continue context across sessions, generate daily memory briefings, and clean older retained files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users can use this skill to keep persistent memory files organized, searchable, and summarized across daily work sessions. It is most relevant when an agent keeps a local memory directory and the user wants routine archiving, retrieval, and retention cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process persistent memory files that contain sensitive or private information.

Mitigation: Review the configured memory directory before use and limit it to files the user is comfortable having indexed, summarized, and reused.

Risk: Automatic cleanup may delete retained memory before the user has confirmed it is no longer needed.

Mitigation: Disable automatic cleanup or require explicit confirmation before deleting older memory files.

## Reference(s):

- [Daily Memory Keeper on ClawHub](https://clawhub.ai/linbo405/skills/daily-memory-keeper)

## Skill Output:

**Output Type(s):** [markdown, files, configuration, guidance]

**Output Format:** [Markdown summaries, search-result lists, archived knowledge-base files, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, summarize, reuse, and clean files in the configured memory directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
