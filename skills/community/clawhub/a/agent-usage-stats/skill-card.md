## Description:

Token Stats helps users inspect local token consumption for supported AI assistants, including Hermes, Claude Code, CodeX, OpenClaw, Reasonix, and DeepSeek TUI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhaoyong](https://clawhub.ai/user/zhouhaoyong)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI assistant users use this skill to review local token usage by agent, model, and time period; monitor live usage deltas; compare periods; and export usage summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup, update, and uninstall commands can change shell PATH entries, create persistent wrappers, update installed files, or remove directories.

Mitigation: Run maintenance commands only from the expected installation context, avoid custom uninstall directories unless reviewed, and confirm any directory the tool says it will remove.

Risk: The tool reads local agent usage and history data from SQLite, JSONL, and JSON files on the current device.

Mitigation: Use it only on devices and accounts where access to local agent usage records is acceptable, and handle exported summaries as potentially sensitive.

Risk: CSV exports can carry spreadsheet-specific risks when opened in office software.

Mitigation: Treat exported CSV files as untrusted and review them before opening or sharing in spreadsheet applications.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouhaoyong/skills/agent-usage-stats)
- [README.md](README.md)
- [README.zh.md](README.zh.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Terminal text with optional CSV, XLSX, and JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local agent usage and history files on the current device; exported spreadsheet files should be treated as untrusted.]

## Skill Version(s):

2.7.13 (source: SKILL.md frontmatter, CHANGELOG.md, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
