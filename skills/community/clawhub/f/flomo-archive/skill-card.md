## Description:

Flomo Archive retrieves a specified month of Flomo notes with a week-to-day fallback strategy and evaluates note quality with built-in rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayshna](https://clawhub.ai/user/jayshna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to fetch a complete monthly archive of their Flomo notes and review basic quality signals such as tags, length, links, images, and short or routine entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves personal Flomo notes through the local mcporter Flomo configuration.

Mitigation: Install and run it only when access to that local Flomo configuration is intended, and avoid shared or privileged environments.

Risk: The skill saves note exports to a predictable /tmp path.

Mitigation: Review or modify the export location before use so note data is written to a private user-controlled directory with restrictive permissions.

Risk: The security scan notes a shell-built command used to call the local MCP tool.

Mitigation: Review the command invocation before deployment and run the skill with the least privileges needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayshna/skills/flomo-archive)
- [Declared package repository](https://github.com/uena/flomo-archive)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands, console summaries, quality reports, and optional JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save retrieved notes as /tmp/flomo_YYYY_MM.json and can evaluate an existing JSON export.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
