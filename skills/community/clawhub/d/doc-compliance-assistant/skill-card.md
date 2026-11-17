## Description:

Scans local text and Markdown for common personal information and secrets, returning masked findings and optionally writing a normalized copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to check drafts, configuration exports, and logs for recognizable personal information or credentials before sharing or committing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pattern-based scanning can miss sensitive information; a clean report does not establish that a document is safe to share.

Mitigation: Review the document and masked findings before sharing it; use a fuller DLP review when required.

Risk: An optional normalized copy retains any secrets or personal information found in the source.

Mitigation: Use --clean --out only for intended files and remove sensitive content before distributing either copy.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/doc-compliance-assistant)
- [LGD theory background (linked in README)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Masked finding report in plain text or JSON; optional normalized text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports matching rule and line number; a normalized copy is not redacted.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
