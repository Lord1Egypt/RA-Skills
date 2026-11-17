## Description:

Generates IRS- and AICPA-compliant marketing content for accounting, CPA, enrolled agent, and tax preparation firms with required disclosures and no prohibited claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitflopez](https://clawhub.ai/user/gitflopez)

### License/Terms of Use:

MIT-0

## Use Case:

External accounting, CPA, enrolled-agent, and tax-preparation firms use this skill to draft marketing campaigns, ads, emails, SMS templates, referral programs, review responses, and compliance checklists for U.S. tax and accounting services.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Marketing drafts may include PTIN, EFIN, enrolled-agent, or CPA license identifiers that are sensitive or unnecessary for a specific channel.

Mitigation: Use placeholders during drafting, include identifiers only when required for the channel and jurisdiction, and remove unnecessary identifiers before publishing.

Risk: Generated copy may still require professional review because state board advertising rules, referral-fee rules, tax-practice rules, and consumer marketing requirements vary.

Mitigation: Have compliance counsel or the relevant licensing board rules reviewed before using ads, emails, SMS messages, web copy, referral incentives, or review requests.

Risk: Installing with an unversioned npx command can fetch a moving installer target.

Mitigation: Use a pinned and trusted ClawHub installer version when installing from the README.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitflopez/skills/accounting-cpa-tax-marketing-kit)
- [README](artifact/README.md)
- [Worked example](artifact/examples/accounting_example.md)
- [Firm Brand and Client Acquisition prompt](artifact/prompts/01_firm_brand_acquisition.md)
- [Tax Season Campaign prompt](artifact/prompts/02_tax_season_campaign.md)
- [Advisory Services Upgrade prompt](artifact/prompts/03_advisory_services_upgrade.md)
- [Referral, Retention, and Reputation prompt](artifact/prompts/04_referral_retention_reputation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown templates and prose with compliance notes, checklists, and channel-specific copy blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft marketing content that should be reviewed against current jurisdiction-specific advertising, tax-practice, email, SMS, and endorsement rules before publication.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
