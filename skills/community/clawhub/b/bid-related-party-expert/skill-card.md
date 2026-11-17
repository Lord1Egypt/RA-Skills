## Description:

Identifies prohibited related-party bidding among tenderers using public business-registration data, including same legal representative, controlling or managing relationships, equity penetration, affiliation-network analysis, and negative-rule checks while staying within the business-registry boundary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement reviewers and compliance teams use this skill to screen multiple bidders for business-registration relationships that may make bids invalid or require further review. It produces review assistance only and does not replace a legal, regulatory, or tender committee determination.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill may process commercially sensitive bidder information or personal contact details when users provide raw procurement materials.

Mitigation: Use redacted or public business-registration data where possible, avoid submitting unnecessary personal details, and handle inputs under applicable procurement confidentiality and privacy requirements.

Risk: Users may over-rely on the report as a final legal or procurement decision.

Mitigation: Treat conclusions as review assistance only and route high-risk or uncertain findings to the tender committee, legal counsel, or the relevant regulator for final determination.

## Reference(s):

- [Equity Penetration Data Dimensions and Completion Guide](references/equity-penetration.md)
- [Example Dialog](references/example-dialog.md)
- [IMA Knowledge Base Review Strategy](references/ima-kb.md)
- [Test Cases and Acceptance Criteria](references/test-cases.md)
- [Project Homepage](https://github.com/chesaram/my-skill-hub)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [XML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured report with summary, findings, network analysis when applicable, data gaps, and a non-binding recommendation.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
