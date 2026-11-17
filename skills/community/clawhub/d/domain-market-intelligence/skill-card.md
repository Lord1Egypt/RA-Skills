## Description:

Domain Market Beat produces time-bounded domain-market news briefings with source tiers, event types, explicit inference limits, notable sales, registration trends, and recent domain movements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abtdomain](https://clawhub.ai/user/abtdomain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and domain-market analysts use this skill to generate current, sourced market-intelligence briefings that separate verified sales, active offers, registration trends, and technical domain movements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings may overstate market signals if stale or incomplete web and domain-data sources are treated as definitive.

Mitigation: Query sources fresh on every run, report the actual observation window, mark missing fields as Not Provided, and disclose data gaps and public-sales disclosure bias.

Risk: Registrar transfers, nameserver changes, or expiry dates may be mistaken for sales, ownership changes, launches, or deletions.

Mitigation: Validate lifecycle status with WHOIS and DNS state with DNS tools; if validation is unavailable, report only the observed technical change.

Risk: Completed sales, reported sales, bids, and listing prices may be conflated.

Mitigation: Keep sales and active offers in separate tables, and label sale type, source tier, and verification status independently.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abtdomain/skills/domain-market-intelligence)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown briefing with tables and sourced sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an explicit time window, source tiers, verification statuses, event dates, publication dates, data gaps, and a market-intelligence disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
