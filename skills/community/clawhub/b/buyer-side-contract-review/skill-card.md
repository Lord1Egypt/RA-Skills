## Description:

Reviews software, hardware, and implementation-service purchase contracts from a buyer-side perspective, identifying unfavorable terms and delivery, acceptance, payment, invoice, warranty, IP, data compliance, and breach-risk issues while producing a graded issue list and tracked DOCX revision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longtel-skill](https://clawhub.ai/user/longtel-skill)

### License/Terms of Use:

MIT

## Use Case:

Procurement, commercial, and contract-review teams use this skill to review buyer-side software, hardware, SaaS, custom development, installation, deployment, maintenance, framework agreement, order, and tender-following contracts. It helps identify signing blockers, pre-signature changes, negotiable improvements, and buyer-favorable terms, then prepares a DOCX redline with visible revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies Chinese buyer-side commercial defaults, including VAT invoice and payment standards that may not fit every jurisdiction or transaction.

Mitigation: Confirm the governing law, tax treatment, payment policy, and buyer-specific standards before relying on the recommendations.

Risk: The skill may process sensitive contract text and generate a DOCX redline containing contract terms.

Mitigation: Use only appropriately authorized contract materials and verify the output path and filename when overwrite avoidance matters.

Risk: The output is a business and contract-risk review, not legal advice.

Mitigation: Have qualified counsel review high-stakes, regulated-industry, dispute-related, or jurisdiction-specific conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longtel-skill/skills/buyer-side-contract-review)
- [Skill source](artifact/SKILL.md)
- [Test cases](artifact/test-cases.md)
- [Test report](artifact/test-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report plus DOCX redline file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a revision-tracked DOCX contract markup and concise in-chat summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
