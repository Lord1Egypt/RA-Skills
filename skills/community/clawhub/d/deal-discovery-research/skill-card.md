## Description:

Find and compare Slickdeals and RetailMeNot offers through Crawlora to build deal shortlists with eligibility and expiry caveats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and purchasing researchers use this skill to find, compare, and assess posted deals and merchant offers, with conditions and unresolved checkout details clearly identified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deal-search terms and lookup parameters are sent to Crawlora using a Crawlora API key.

Mitigation: Do not include secrets, private account data, or sensitive purchasing plans in queries; keep searches bounded.

Risk: Posted deals, coupons, and community reports may not reflect current stock, eligibility, or final checkout prices.

Mitigation: Preserve source links and observation times, disclose exclusions and unknowns, and verify terms before purchasing.

## Reference(s):

- [Deal discovery endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/deal-discovery-research)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Markdown deal shortlist with source links and eligibility caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observation times and unresolved checkout questions; posted offers are not verified checkout prices.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
