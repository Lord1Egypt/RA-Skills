## Description:

Reads local documents and project knowledge into an auditable scan plan, per-slice findings, and a cited synthesis report on disk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scan local plain-text or Markdown project materials and produce auditable, path-cited analysis artifacts for downstream planning or documentation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags possible exposure of sensitive credential-file contents during local document analysis.

Mitigation: Review before installing, use explicit paths and output_dir values, avoid no-parameter auto-discovery on private projects, and provide only sanitized, redacted excerpts when skipped sensitive files are needed.

## Reference(s):

- [Artifact Analysis ClawHub Skill Page](https://clawhub.ai/anderskev/skills/artifact-analysis)
- [Citation Schema](references/citation-schema.md)
- [Companion Invocation Contract](references/companion-contract.md)
- [Failure Modes](references/failure-modes.md)
- [Synthesis Skeleton](references/report-template.md)
- [Default Skip Patterns](references/skip-patterns.md)
- [Subagent Brief Template](references/subagent-brief.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown files with path-anchored citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plan.md, findings files, and report.md under an output directory; reports are citation-backed and stored on disk rather than returned inline.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
