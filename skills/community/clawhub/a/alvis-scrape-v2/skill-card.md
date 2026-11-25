## Description:

Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan authorized public web scraping workflows, including robots.txt checks, terms review, rate limiting, privacy-aware data handling, and optional managed extraction through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs and scraped page content may be sent to SkillBoss when the managed API path is used.

Mitigation: Confirm this data sharing is acceptable before installation, and prefer direct or local scraping for sensitive material.

Risk: Scraping protected, personal, or unauthorized content can create legal and privacy exposure.

Mitigation: Use the skill only for authorized public scraping, avoid protected or personal data unless there is a legal basis, and follow the compliance checks before collecting data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvis-scrape-v2)
- [SkillBoss Setup Guide](https://SkillBoss.co/skill.md)
- [SkillBoss API Hub Scraper Endpoint](https://api.SkillBoss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code and API integration patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Managed API path requires SkillBoss_API_KEY and returns extracted content at result.data.markdown.]

## Skill Version(s):

2.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
