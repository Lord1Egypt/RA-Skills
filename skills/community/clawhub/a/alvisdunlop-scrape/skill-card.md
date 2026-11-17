## Description:

Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan compliant public or authorized web scraping workflows, including robots.txt checks, rate limiting, data minimization, and optional managed extraction through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping can violate site terms, robots.txt expectations, or access controls if used on disallowed or protected content.

Mitigation: Use the skill only for public or authorized data, check robots.txt and site terms before scraping, prefer an official API when available, and stop when access is disallowed.

Risk: Managed scraping sends target content and requests to a third-party scraping service using an API key.

Mitigation: Install only if third-party SkillBoss API Hub use is acceptable, protect SkillBoss_API_KEY, and avoid sending personal, protected, or sensitive content without a clear legal basis.

Risk: Collection or storage of personal data can create privacy and compliance exposure.

Mitigation: Strip unnecessary PII, minimize retained data, avoid fingerprinting or indirect identification, and keep an audit trail for justified scraping activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvisdunlop-scrape)
- [SkillBoss setup guide](https://SkillBoss.co/skill.md)
- [SkillBoss API Hub scraper endpoint](https://api.SkillBoss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request patterns and compliance checklists; managed scraping requires SkillBoss_API_KEY.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
