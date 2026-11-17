## Description:

Knowledge base skill that uses the published clawsqlite CLI for ingest, search, show, and maintenance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ernestyu](https://clawhub.ai/user/ernestyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a configured local clawsqlite knowledge instance through the official CLI, including ingest, search, show, maintenance, and analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill wraps a PyPI-backed CLI and bootstrap may install dependencies into the active Python environment before falling back to a skill-local target.

Mitigation: Run bootstrap in an isolated Python environment when assurance matters and review the clawsqlite package provenance separately.

Risk: The CLI creates and uses a persistent local knowledge store that may contain private records and configuration.

Mitigation: Keep the knowledge database and clawsqlite.toml in the configured instance home, avoid storing them in the skill directory, and validate the setup with doctor before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ernestyu/skills/clawsqlite-knowledge)
- [clawsqlite homepage](https://github.com/ernestyu/clawsqlite)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON-emitting CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands rely on a local clawsqlite.toml configuration and commonly use --json for machine-readable results.]

## Skill Version(s):

1.0.12 (source: frontmatter, manifest, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
