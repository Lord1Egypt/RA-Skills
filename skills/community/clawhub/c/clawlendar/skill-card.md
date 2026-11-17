## Description:

Timestamp-first perpetual calendar interop for AI agents that need cross-calendar conversion, timestamp normalization, true month boundaries, and day-level almanac payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hosuke](https://clawhub.ai/user/hosuke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Clawlendar to normalize calendar, timeline, month-boundary, daily-profile, and almanac data across MCP, CLI, and HTTP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended pip install command is not version-pinned, so installation depends on current external package integrity.

Mitigation: Prefer a pinned reviewed version of clawlendar and its dependencies, inspect the package source, and run the MCP server with only the filesystem and network access it needs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hosuke/skills/clawlendar)
- [Clawlendar Source Homepage](https://github.com/Hosuke/Clawlender)

## Skill Output:

**Output Type(s):** [JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports MCP tools, CLI commands, and HTTP endpoints for calendar conversion and timestamp-based timeline normalization.]

## Skill Version(s):

0.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
