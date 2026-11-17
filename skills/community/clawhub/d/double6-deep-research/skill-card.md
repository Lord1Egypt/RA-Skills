## Description:

Helps an agent conduct authorized multi-source research, produce an evidence-backed report bundle, record source and claim metadata, compute candidate SHA-256 hashes, and run a Python validator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[double6-ai](https://clawhub.ai/user/double6-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill when a task requires scoped deep research, source comparison, decision support, or complex fact checking with auditable deliverables. It is intended for work where the agent must bind conclusions to authorized sources and record limits, gaps, and validation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator may read or overwrite files outside the intended bundle when run on a crafted directory.

Mitigation: Run the validator only on trusted, freshly created bundle directories without elevated privileges, and verify candidate bundle files are not symlinks before validation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/double6-ai/skills/double6-deep-research)
- [Homepage](https://github.com/double6-ai/double6-skills/tree/main/skills/double6-deep-research)
- [Privacy and Fail-Closed Boundaries](references/privacy-and-fail-closed.md)
- [Report Quality and Review Requirements](references/report-quality.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON research records, validation receipts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a report bundle in an authorized output directory and uses a Python 3.10+ standard-library validator.]

## Skill Version(s):

2.0.2 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
