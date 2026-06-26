## Description: <br>
Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan web scraping workflows that respect robots.txt, site terms, rate limits, authentication boundaries, and privacy obligations. It can guide either direct HTTP scraping or managed scraping through the SkillBoss API Hub when a SkillBoss API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the SkillBoss managed-scraping option may send target URLs and extracted content to a third-party API. <br>
Mitigation: Use local or direct scraping for sensitive or regulated targets, and only use SkillBoss when its data handling is acceptable for the target content. <br>
Risk: Scraping without authorization can violate site terms, access controls, privacy laws, or copyright obligations. <br>
Mitigation: Confirm authorization, respect robots.txt and terms of service, avoid login-protected or personal data, and minimize collection and storage. <br>
Risk: The skill requires a sensitive SkillBoss API key when using managed scraping. <br>
Mitigation: Store SkillBoss_API_KEY in a secret manager or environment variable, avoid committing it, and rotate it if exposed. <br>


## Reference(s): <br>
- [Scrape skill page](https://clawhub.ai/alvisdunlop/alvis-scrape-v2) <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>
- [SkillBoss API Hub endpoint](https://api.SkillBoss.co/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with inline code and API configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include robots.txt checks, rate-limit guidance, data-handling constraints, and SkillBoss API Hub integration details.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
