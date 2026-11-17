## Description:

Scans documents, code, and logs for personal identifiers, secrets, internal paths, and project codenames before external release, then suggests masking for detected content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other people preparing documents, code, or logs for external sharing use this skill to identify and mask potentially sensitive content before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional audit report can reveal excerpts of the sensitive values the skill masks.

Mitigation: Do not share the report externally unless raw samples have been removed; retain only non-sensitive finding metadata.

Risk: The declared permissions do not match the CLI's file-reading behavior.

Mitigation: Review before installing, scan only files intentionally selected, and align declared permissions with actual behavior.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/doc-desens-scanner)
- [LGD theory (background reference)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Masked plain text with an optional JSON audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional audit report includes finding counts, types, and sample excerpts.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact frontmatter states 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
