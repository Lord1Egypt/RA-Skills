## Description:

Registers AI-generated outputs with fingerprints and attribution details for integrity checks, lookup, and audit reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to record AI outputs with hashes, model details, timestamps, and ownership claims, then check integrity and retrieve audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent registry files retain output summaries and provenance details that may be confidential.

Mitigation: Register only material approved for local retention and restrict access to the registry files.

Risk: The declared permissions omit filesystem and subprocess access despite the documented local ledger writes.

Mitigation: Review actual file access and reconcile permission declarations before deployment.

## Reference(s):

- [Agent Output Registry on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/agent-output-registry)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [CLI guidance and text results; local JSONL, CSV, and Markdown ledger files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registration records output summaries, model and ownership details, hashes, and timestamps locally; verification returns an integrity result.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata; bundled frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
