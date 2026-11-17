## Description:

Helps agents create engineering documents using 23 structured templates and document-specific writing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to draft and update product, architecture, delivery, process, and technical knowledge documents with consistent structure and review guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance may overwrite existing `.env.local` settings.

Mitigation: Check whether `.env.local` already contains settings and skip the environment copy step if it does.

Risk: Handoffs may expose secrets or unnecessary personal information.

Mitigation: Review handoff content and redact secrets and unnecessary personal information before sharing.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/zengfr/document-governance-skills/tree/main/doc-writer)
- [ClawHub release page](https://clawhub.ai/zengfr/skills/doc-writer)
- [Document format guides](artifact/references/format-guides.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown documents and writing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template-based; structure and review checks vary by document type.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
