## Description:

Helps prospective exotic-car renters compare company listings, prices, terms, reviews, ownership claims, and payment-related red flags before paying a deposit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External renters use this skill to review and compare 1 to 4 exotic-car rental companies before paying a deposit. It summarizes published company details and market pricing, flags concerns supported by available information, and suggests questions to ask; owner-verified status is not a background check or safety guarantee.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced catalog-data and renter-checklist documents are missing from the supplied artifact, limiting review of their data rules and guidance.

Mitigation: Obtain and review the missing documents and confirm the intended catalog client before relying on results.

Risk: An owner-verified listing does not establish that a company has passed a background check or is safe.

Mitigation: Treat claimed status only as a listing claim and independently check the company, contract, insurance, and payment details before paying.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sergebulaev/skills/exotic-rental-company-check)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Markdown with company profiles, comparison tables, flags, and questions to ask]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can compare 1 to 4 companies; findings depend on catalog information and user-provided details.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
