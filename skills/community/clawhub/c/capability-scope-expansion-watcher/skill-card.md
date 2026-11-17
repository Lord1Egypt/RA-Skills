## Description:

Helps detect incremental capability scope expansion across skill versions, including risk-class contradiction detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and agent platform maintainers use this skill to examine skill version history for cumulative permission drift, behavioral scope expansion, capability composition amplification, changelog gaps, and risk-class contradictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reviews metadata and version history that may include installed-skill lists or capability declarations supplied by the user.

Mitigation: Review inputs before use and avoid providing sensitive installed-skill inventories or capability records unless they are needed for the audit.

Risk: Scope expansion analysis requires complete historical metadata, so incomplete version history can produce incomplete conclusions.

Mitigation: Use the report as an audit aid and confirm findings against preserved version metadata, changelogs, and capability declarations before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/capability-scope-expansion-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with per-version deltas, cumulative expansion analysis, alignment assessment, amplification points, changelog review, and an expansion verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report depends on user-provided skill identifiers, version ranges, installed-skill lists, capability declarations, and available version history.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
