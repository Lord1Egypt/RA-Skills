## Description:

Live Technical SEO, AEO & GEO website diagnostic API (62 rules, RFC 9727, AEO-Sem semantic engine, and 4-AI citation checks) via AEORank Edge Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aizaloapp](https://clawhub.ai/user/aizaloapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and website owners use this skill to inspect technical SEO rules and request live technical, AEO, and GEO audits for a website through AEORank. It returns diagnostic results and can report live AI citation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live audits send the submitted website URL to AEORank, consume service credits, and use a provider whose availability and data-retention practices were not independently verified.

Mitigation: Submit only URLs you are comfortable sharing, review the provider's current terms and availability, and account for audit credits before running live checks.

Risk: The skill requires an AEORank API key for authenticated live audits.

Mitigation: Configure only the service-specific AEORANK_API_KEY and keep it private.

## Reference(s):

- [AEORank Global Diagnostic Station](https://aeorank.app/)
- [AEORank Open Knowledge Hub](https://aeorank.app/learn)
- [AEORank Public Rule Index](https://aeorank.app/api/v1/rules?lang=en)
- [RAG Architecture & 8-Tier GEO Framework](https://aeorank.app/learn/rag-architecture-8-tier-geo-publishing-framework.md)
- [ClawHub Release Page](https://clawhub.ai/aizaloapp/skills/aeorank-seo-geo-auditor)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON]

**Output Format:** [JSON diagnostic responses and concise analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live audit results depend on AEORank availability; paid audit endpoints consume credits.]

## Skill Version(s):

2.1.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
