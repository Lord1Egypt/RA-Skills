## Description:

Reviews and revises Word contract documents by identifying risky clauses, generating attorney-review-ready reports, supporting client confirmation, and producing revised document versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baichenwzj](https://clawhub.ai/user/baichenwzj)

### License/Terms of Use:

MIT-0

## Use Case:

Legal teams and contract reviewers use this skill for first-pass review of .docx commercial contracts, risk clause identification, suggested revisions, and generation of review reports or revised Word documents for qualified attorney review.

### Deployment Geography for Use:

Global, with primary support for Chinese and English contracts and jurisdiction-specific legal review required before reliance.

## Known Risks and Mitigations:

Risk: The skill may read confidential or privileged contract materials.

Mitigation: Use only with documents the user is authorized to process and keep contract content within the relevant matter.

Risk: Legal recommendations or revised wording may be incorrect, incomplete, or jurisdiction-dependent.

Mitigation: Confirm the contract language, governing jurisdiction, client role, and review mode, then have a qualified attorney review outputs before reliance.

Risk: Automated Word document revision can change formatting, layout, or clause wording in ways that need review.

Mitigation: Preserve the original file, compare the generated revision against the source document, and manually inspect formatting before use.

## Reference(s):

- [Skill documentation](artifact/SKILL.md)
- [Legal Document Review Agent](artifact/agents/legal-document-review.md)
- [ClawHub skill page](https://clawhub.ai/baichenwzj/skills/contract-review-revise)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown review reports, modification comparison lists, and revised .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations and edited documents require qualified attorney review before reliance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
