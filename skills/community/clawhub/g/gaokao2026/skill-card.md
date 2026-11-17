## Description:

Helps agents guide Gaokao students, families, counselors, and education product teams through paid, read-only admissions data queries by score, province, subject selection, universities, and major groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackgl-hk](https://clawhub.ai/user/jackgl-hk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, education advisors, and developers use this skill to connect an agent or workflow to a paid Gaokao admissions data API for preliminary school and major-group lookup, comparison, and report generation. It is intended for read-only reference queries and not for database writes or administrative actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API Key and Secret exposure could allow unauthorized use of the paid API subscription.

Mitigation: Store credentials only in secure secret storage, avoid placing them in prompts, public configuration, client-side code, or logs, and rotate or revoke them if exposed.

Risk: Users may misunderstand the API as free or unrestricted.

Mitigation: Confirm trust in zhiyuanx.com and review the paid subscription terms, price, duration, and access limits before installation or use.

Risk: Admissions query results may be incomplete or vary by province, school, or major group.

Mitigation: Use results as reference material for preliminary comparison and verify important admissions decisions against official sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackgl-hk/skills/gaokao2026)
- [Publisher Profile](https://clawhub.ai/user/jackgl-hk)
- [Subscription and API Documentation](https://zhiyuanx.com/api.html)
- [Zhiyuanx Main Site](https://zhiyuanx.com/)
- [Official App Store App](https://apps.apple.com/cn/app/id6743759582/)
- [Official App Store App](https://apps.apple.com/cn/app/id6747729955)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with API subscription, credential handling, and read-only query integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference paid API credentials and subscription status; actual query fields vary by province, school, and major-group data availability.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
