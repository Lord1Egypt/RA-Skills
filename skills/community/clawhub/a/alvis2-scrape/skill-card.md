## Description:

Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and produce web-scraping guidance, code patterns, API calls, shell commands, and configuration that account for robots.txt, terms of service, rate limits, and privacy-sensitive data handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Managed scraping sends requested content through SkillBoss as a third-party processor.

Mitigation: Use the SkillBoss API only for data you are permitted to process, and avoid protected, personal, confidential, or terms-restricted data.

Risk: The external setup guide was referenced by the artifact but was not part of the inspected release evidence.

Mitigation: Review the external setup guide separately before installation or operational use.

Risk: Scraping workflows can violate site terms, privacy requirements, or access restrictions if used without review.

Mitigation: Follow the skill's checklist for robots.txt, terms of service, authentication boundaries, rate limits, and PII minimization before scraping.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvis2-scrape)
- [Publisher Profile](https://clawhub.ai/user/alvisdunlop)
- [SkillBoss Setup Guide](https://SkillBoss.co/skill.md)
- [SkillBoss API Endpoint](https://api.SkillBoss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration details, and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SkillBoss_API_KEY when using the managed SkillBoss API Hub scraping flow.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
