## Description:

Reviews tender documents, bid responses, award notices, and draft or signed contracts to identify substantive deviations such as inconsistent scope, price, quality, schedule, remedies, wording games, or concealed concessions, then produces an auditable compliance review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, legal, audit, and bid-compliance teams use this skill to compare Chinese tender, bid, award, and contract materials before or after signing and surface consistency risks that need remediation or professional review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may provide unrelated or sensitive local files when using document-handling integrations.

Mitigation: Provide only the intended procurement, bid, award, and contract materials, and avoid unnecessary local-file access.

Risk: Optional Office-document tooling could modify source documents unintentionally.

Mitigation: Require separate confirmation before allowing any optional tool to modify Office documents.

Risk: AI-generated findings could be treated as final legal or procurement advice.

Mitigation: Use the report as compliance screening and have lawyers, evaluators, or audit authorities confirm final legal and signing decisions.

Risk: Legal citations or knowledge-base results may be outdated or unavailable.

Mitigation: Verify cited statutes, regulations, and official interpretations against authoritative current sources before relying on them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/chesaram/skills/contract-and-tender-document-consistency-review-assistant-1-0-0)
- [Test cases and success criteria](artifact/references/test-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown compliance review report with a conclusion summary, comparison matrix, risk analysis, and remediation recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires labeled tender, bid or award, and contract materials; scanned or image-only documents need OCR text before reliable review.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
