## Description:

Source-backed company context retrieval for OpenClaw agents via the fourok CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonvanlaak](https://clawhub.ai/user/simonvanlaak)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and OpenClaw agents use this skill to retrieve permission-filtered company, project, customer, and operational context from an existing fourok backend before answering. Agents can open decisive source references and cite returned evidence instead of relying on unsupported context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes code that can persist full OpenClaw chat messages without clear user-facing disclosure.

Mitigation: Require explicit opt-in documentation for chat-message capture plus redaction, retention, deletion, audit, and access-control guarantees; disable message ingestion for retrieval-only deployments.

Risk: Agents may send sensitive values in retrieval queries or over-trust retrieved cards.

Mitigation: Do not include secrets, raw environment values, database URLs, tokens, or private keys in queries; treat retrieved cards as evidence to inspect and cite, not as a final-answer oracle.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonvanlaak/skills/fourok)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text]

**Output Format:** [Markdown instructions with inline shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing fourok CLI and backend; retrieved results are permission-filtered and should be cited with durable refs.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
