## Description:

Verify numerical data against original papers and maintain traceable provenance for every value in datasets, tables, and plots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larry-of-cosmotim](https://clawhub.ai/user/larry-of-cosmotim)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, data curators, and developers use this skill to verify literature-derived numerical datasets, maintain citation source folders, and produce audit reports before values are used in tables, plots, or manuscripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs fetched from DOI or URL inputs may be unavailable, paywalled, or untrusted.

Mitigation: Review source identifiers before download, treat PDFs as untrusted files, and mark missing or paywalled sources as needing confirmation.

Risk: Literature values can be misattributed, estimated, or unverifiable.

Mitigation: Require exact paper, DOI, page, table, figure, method, data type, and verification status before treating a value as confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larry-of-cosmotim/skills/data-source-verification)
- [Project homepage](https://github.com/Larry-of-cosmotim/data-source-verification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with citation templates, audit summaries, provenance tables, and optional CSV or JSON examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces traceability records, verification statuses, discrepancy notes, and recommended actions for flagged values.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
