## Description:

Use when writing or formatting an ADR document using the MADR template, applying Definition of Done (E.C.A.D.R.) criteria, or verifying ADR completeness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, format, and verify Architectural Decision Records from extracted requirements, meeting notes, PR discussions, or design documents. It helps produce MADR-style ADR markdown with completeness checks and investigation markers for missing decision evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ADRs may contain inaccurate decisions, incomplete rationale, or investigation markers when source material is incomplete.

Mitigation: Review each generated ADR for factual accuracy, completeness against E.C.A.D.R. criteria, and unresolved investigation prompts before treating it as proposed or accepted.

Risk: The numbering helper reads local ADR directories to choose the next sequence number, which can be stale during parallel ADR creation.

Mitigation: Use pre-assigned numbers or the helper's count allocation mode for parallel writes, then verify the final file path before committing.

## Reference(s):

- [Definition of Done: E.C.A.D.R. Criteria](references/definition-of-done.md)
- [MADR Template](references/madr-template.md)
- [Markdown Any Decision Records](https://adr.github.io/madr/)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown ADR documents with YAML frontmatter and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [ADR files are expected under docs/adrs/ using zero-padded sequence numbers and slugified filenames.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
