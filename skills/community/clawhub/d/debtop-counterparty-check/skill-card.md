## Description:

Checks public debt notices for a named company and summarizes notice matches, debt amounts, recent activity, creditors, and guarantee clues in a one-page brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjaliang](https://clawhub.ai/user/ninjaliang)

### License/Terms of Use:

MIT-0

## Use Case:

Business, procurement, investment, and legal users can check publicly disclosed debt notices before engaging a counterparty. The brief is an initial reference, not a credit report or complete due-diligence assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company lookup terms, client and skill identifiers, and a stable guest device ID are sent to Debtop.

Mitigation: Use only for company names appropriate to share with Debtop and keep the default endpoint unless you control an alternate deployment.

Risk: Cached guest access and refresh tokens may grant access if exposed.

Mitigation: Treat the guest token cache as a credential and restrict access to it.

Risk: Public-notice matches can be mistaken for a complete credit or due-diligence finding.

Mitigation: Identify the notice source and query time, verify the company identity, and state that no match does not mean no debt.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ninjaliang/skills/debtop-counterparty-check)
- [ClawHub publisher profile](https://clawhub.ai/user/ninjaliang)
- [Guest access and service endpoint](artifact/references/guest-access.md)
- [Debt lookup tools and fields](artifact/references/tools-and-fields.md)
- [Counterparty check report template](artifact/templates/counterparty-check-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [One-page Markdown brief with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes query time and public-notice scope; missing matches do not establish absence of debt.]

## Skill Version(s):

1.0.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
