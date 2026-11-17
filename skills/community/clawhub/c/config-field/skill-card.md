## Description:

Validate OpenClaw configuration fields against the official Zod schema for agents, channels, tools, logging, and session configuration when reading or writing openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redcontritio](https://clawhub.ai/user/redcontritio)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when reading, writing, debugging, or migrating OpenClaw configuration files to check whether field paths exist, inspect field details, and validate openclaw.json files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create false confidence by accepting some unknown OpenClaw configuration fields as valid while presenting itself as schema validation.

Mitigation: Treat results as field lookup assistance, and verify high-impact sandbox, filesystem, execution, token, and channel settings against the authoritative OpenClaw schema before approval.

Risk: Schema or documentation mismatches can make validation results stale or incomplete.

Mitigation: Confirm the current OpenClaw version and schema status before relying on the skill output for configuration changes.

## Reference(s):

- [OpenClaw Configuration Schema Fields](references/schema-fields.md)
- [ClawHub Skill Page](https://clawhub.ai/redcontritio/skills/config-field)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown with inline shell commands and validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include field existence results, type details, suggestions for invalid paths, and configuration validation summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
