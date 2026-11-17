## Description:

Uses WenDaoYun company data to assess whether an organization is suitable as a customer, supplier, partner, or investment target across operating, administrative, enforcement, and legal-risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rose-develop](https://clawhub.ai/user/rose-develop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to screen companies for cooperation, supplier onboarding, customer-risk review, and investment suitability. It searches for a company, requires user confirmation of the target organization, then produces a concise recommendation with supporting risk signals and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication errors or troubleshooting transcripts could expose API-key or bearer-token details.

Mitigation: Store WENDAOYUN_API_KEY only in the environment, redact API keys and Authorization headers from errors, and avoid sharing raw authentication failures in chat transcripts.

Risk: The skill depends on WenDaoYun as a third-party data provider and may direct users toward paid API usage.

Mitigation: Review WenDaoYun account terms, pricing, and data-provider suitability before enabling the skill for normal workflows.

Risk: Company cooperation recommendations can be incomplete if based only on the returned WenDaoYun data.

Mitigation: Treat the report as a decision-support summary, verify important findings against source records, and request additional materials before high-impact business decisions.

## Reference(s):

- [fuzzy-search-org API reference](references/fuzzy-search-org.md)
- [get-cooperate-evaluate API reference](references/get-cooperate-evaluate.md)
- [WenDaoYun Open Platform](https://open.wendaoyun.com/home)
- [ClawHub skill page](https://clawhub.ai/rose-develop/skills/company-cooperate-evaluate-search-wdy)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown report with conclusion, key signals, evidence limitations, and next actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WENDAOYUN_API_KEY and user confirmation of the target company before detailed lookup.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
