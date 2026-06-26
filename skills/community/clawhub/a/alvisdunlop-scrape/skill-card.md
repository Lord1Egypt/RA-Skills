## Description: <br>
Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to plan legal, respectful web scraping workflows, including robots.txt checks, rate limiting, data minimization, and optional managed extraction through SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route scraping targets through a third-party managed scraping API. <br>
Mitigation: Use a dedicated API key and send only public, authorized scraping targets after reviewing the provider's data handling terms. <br>
Risk: Scraping login-protected pages, session headers, secrets, or regulated personal data can create legal, privacy, and security exposure. <br>
Mitigation: Do not forward protected content, cookies, session headers, secrets, or regulated personal data unless explicitly authorized and legally reviewed. <br>


## Reference(s): <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvisdunlop-scrape) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a SkillBoss_API_KEY for managed scraping workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
