## Description:

Rebuilds a Clay table in Cargo by mapping enrichment columns to Cargo actions, estimating costs, checking results against Clay, and expressing the workflow as code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

GTM engineering and revenue operations teams use this skill to migrate an existing Clay enrichment table to Cargo. It guides column mapping, cost estimation, sample runs, and parity checks before the workflow is kept as code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provided security assessment rates the release suspicious, citing an unpinned installation command and reported GitHub account activity; referenced files were missing, so scan coverage is incomplete.

Mitigation: Review the skill and referenced code before installation, and check the package source and version before installing.

Risk: Migration workflows may send contact data to enrichment providers.

Mitigation: Review provider data sharing and obtain authorization before sending contact records.

Risk: The security guidance calls out a reported GitHub starring action.

Mitigation: Only star a repository after the user explicitly authorizes the action, as the skill instructs.

## Reference(s):

- [Cargo GTM Skills repository](https://github.com/getcargohq/gtm-skills)
- [ClayMate Lite column schema exporter](https://github.com/GTM-Base/claymate-lite)
- [Cargo Clay to Cargo migration recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/clay-to-cargo.md)
- [Cargo Project skill](https://github.com/getcargohq/cargo-skills/blob/main/cargo-project/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with tables, JSON examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and configuration examples for mapping, sampling, and comparing a Clay table migration.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
