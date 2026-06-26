## Description: <br>
Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to plan and implement web scraping workflows that check robots.txt, terms of service, rate limits, and privacy obligations before collecting public web data. It also guides managed extraction through SkillBoss API Hub when users provide the required SkillBoss_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs and extracted content may be sent to the third-party SkillBoss API when managed scraping is used. <br>
Mitigation: Use managed scraping only for public, authorized pages and avoid sending protected, personal, or sensitive data. <br>
Risk: Anti-bot handling could be misused to bypass access controls or explicit scraping prohibitions. <br>
Mitigation: Check robots.txt, site terms, authentication boundaries, and available APIs before scraping, and stop when permission is absent. <br>
Risk: Scraping too aggressively can burden target services and increase legal exposure. <br>
Mitigation: Apply conservative rate limits, honor 429 responses with backoff, reuse sessions, and keep an audit trail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-web-scrape) <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>
- [SkillBoss API Hub pilot endpoint](https://api.SkillBoss.co/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code and API call patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require SkillBoss_API_KEY for managed scraping through SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
