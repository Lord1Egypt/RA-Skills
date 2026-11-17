## Description:

Clause-by-clause BAA analysis against 45 CFR 164.504(e)(2), evaluating the 9 required HIPAA provisions with risk scoring and remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, compliance teams, and healthcare operations teams use this skill to review Business Associate Agreements for required HIPAA contract provisions, clause adequacy, risk level, and remediation recommendations. It supports review of user-provided BAA text, attachments, or file paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business Associate Agreements may contain sensitive healthcare-adjacent legal content, confidential business details, or patient identifiers.

Mitigation: Provide only the agreement needed for review, redact patient identifiers and unnecessary confidential details where possible, and handle outputs under applicable privacy and legal controls.

Risk: The generated compliance assessment may be incomplete or may not reflect jurisdiction-specific legal obligations.

Mitigation: Have qualified counsel verify findings and recommendations before relying on them for contract changes or compliance decisions.

## Reference(s):

- [Baa Review on ClawHub](https://clawhub.ai/dangsllc/skills/baa-review)
- [dangsllc Publisher Profile](https://clawhub.ai/user/dangsllc)
- [Rote](https://rotecompliance.com)
- [Dang's Solutions](https://dangssolutions.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON compliance report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes party identification, 9 provision findings, clause excerpts, status, gap descriptions, risk levels, recommendations, and reasoning.]

## Skill Version(s):

0.1.2 (source: server release metadata; skill frontmatter reports 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
