## Description:

Generates standardized Word module design documents from front-end code, back-end code, and front-end page screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superchao9](https://clawhub.ai/user/superchao9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical documentation teams use this skill to inspect front-end and back-end module code, capture UI screenshots, and assemble standardized Word design documents with flows, table schemas, and implementation class listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read application repositories and capture authenticated UI pages, which can expose proprietary code, tenant data, personal data, or business data.

Mitigation: Limit access to the relevant repositories and review generated notes, screenshots, and documents for sensitive content before storing or sharing them.

Risk: The skill asks for login details when pages require authentication.

Mitigation: Do not provide production passwords in chat; prefer logging in yourself, using a temporary least-privilege account, or sharing only a short-lived session mechanism.

## Reference(s):

- [Document format reference](artifact/references/doc-format.md)
- [ClawHub skill page](https://clawhub.ai/superchao9/skills/design-doc-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown notes, local screenshots, and Word .docx files; may include Python script edits or commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized under workspace/outputs/<module>-design-doc-<date>/ with notes, screenshots, and a generated .docx document.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
