## Description:

Keep your constraints healthy -- lifecycle management with automatic staleness detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage constraint governance state, periodic reviews, index generation, round-trip verification, and schema migration within an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional dependency install commands reference unpinned third-party packages.

Mitigation: Verify the publisher and package contents before installation, and prefer pinned or internally reviewed versions for managed environments.

Risk: The skill reads and writes governance-related workspace files and generated indexes.

Mitigation: Review the configured workspace paths and generated changes before relying on governance status, indexes, or review records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/agentic-governance)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON reports with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes governance state, review records, alerts, constraint metadata, and skill indexes to workspace paths.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
