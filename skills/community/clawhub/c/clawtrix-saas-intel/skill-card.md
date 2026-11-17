## Description:

Surfaces up to three ClawHub skill recommendations for SaaS-focused agents across auth, billing, onboarding, customer lifecycle, product analytics, and n8n workflow conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicope](https://clawhub.ai/user/nicope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SaaS teams use this skill to audit an agent's SaaS mission, search ClawHub for relevant skills, score candidates, and produce a concise top-three recommendation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read an agent mission and stack details and write a persistent recommendation report.

Mitigation: Review the generated report before acting on recommendations, especially for agents with billing, authentication, or customer-data access.

Risk: Recommended skills for SaaS agents can affect high-impact workflows such as payments, identity, onboarding, and customer data.

Mitigation: Run the suggested security audit and review ClawHub security signals before installing any recommended skill.

## Reference(s):

- [Clawtrix Saas Intel on ClawHub](https://clawhub.ai/nicope/skills/clawtrix-saas-intel)
- [ClawHub search API for Stripe billing skills](https://clawhub.ai/api/v1/search?q=stripe+billing&limit=10)
- [ClawHub search API for auth and identity skills](https://clawhub.ai/api/v1/search?q=auth+identity+saas&limit=10)
- [ClawHub search API for onboarding skills](https://clawhub.ai/api/v1/search?q=onboarding+activation&limit=10)
- [ClawHub search API for n8n workflow skills](https://clawhub.ai/api/v1/search?q=n8n+workflow&limit=10)
- [ClawHub search API for product analytics and retention skills](https://clawhub.ai/api/v1/search?q=product+analytics+retention&limit=10)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with scored recommendations and install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits recommendations to the top three candidates.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
