## Description:

Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling, including direct HTTP scraping and managed scraping through SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and generate compliant web-scraping workflows for public web data, including robots.txt checks, rate limiting, data minimization, and optional managed extraction through SkillBoss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Managed scraping requests may expose target URLs, request context, and retrieved content to SkillBoss.

Mitigation: Use a dedicated API key, a role-based contact address, and send only data that is authorized for third-party processing.

Risk: Scraping protected, personal, confidential, or regulated data can create legal, privacy, or contractual exposure.

Mitigation: Follow robots.txt and site terms, prefer official APIs, avoid protected content, and collect personal or regulated data only with clear authorization.

## Reference(s):

- [SkillBoss setup guide](https://SkillBoss.co/skill.md)
- [Alvis Web Scrape on ClawHub](https://clawhub.ai/alvisdunlop/skills/alvis-web-scrape)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists, code patterns, and API usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference SkillBoss_API_KEY for managed scraping requests.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
