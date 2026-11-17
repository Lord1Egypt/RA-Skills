## Description:

A CLI skill that generates CSV lead lists with company and contact-style fields; current evidence indicates it produces synthetic sample leads despite advertising Apollo.io and LinkedIn integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:

MIT

## Use Case:

Sales teams, consultants, and B2B marketers can use the skill to create CSV lead-list drafts or sample prospecting datasets from industry, role, company-size, and region inputs. Users should not treat generated contacts as verified real leads without separate validation and compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises real Apollo.io and LinkedIn lead collection, but the reviewed code appears to generate synthetic CSV leads.

Mitigation: Treat generated records as sample data unless the implementation is independently reviewed and connected to lawful, approved data sources.

Risk: The skill advertises personal-data collection and GDPR compliance with little privacy scoping in the evidence.

Mitigation: Do not use it for real contact scraping or outreach unless a lawful basis, consent or compliance controls, and dependency review are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highlander89/skills/ai-lead-generator-skill)
- [Publisher profile](https://clawhub.ai/user/highlander89)

## Skill Output:

**Output Type(s):** [text, CSV file, JSON preview]

**Output Format:** [CLI console text, generated CSV file, and JavaScript object preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output count, industry, role, company size, and region are controlled by CLI flags.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
