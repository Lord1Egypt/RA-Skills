## Description: <br>
Generate daily morning briefings with weather, traffic limits, and news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyachao](https://clawhub.ai/user/caoyachao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual users use this skill to generate repeatable daily morning briefings, combining weather, Beijing traffic restriction information, and news summaries in text or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather fetching uses unsafe shell command construction when city values are not trusted. <br>
Mitigation: Review before installing and use only the default or trusted city values until the weather fetch uses a safer HTTP call. <br>
Risk: The scheduled email example could send briefings to an unintended outside recipient. <br>
Mitigation: Replace the example recipient with an intended address and explicitly approve recurring external delivery before enabling the cron job. <br>


## Reference(s): <br>
- [ClawHub Daily Briefing listing](https://clawhub.ai/caoyachao/dailybriefing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration] <br>
**Output Format:** [Markdown-style text briefing or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports current-day or next-day generation, simple and no-news modes, and 30-minute local caching.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
