## Description: <br>
Queries Eqxiu marketing calendar holidays and builds template mall search URLs via msearch-api.eqxiu.com for future promo events, marketing calendar planning, and Eqxiu festival templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eqxiu](https://clawhub.ai/user/eqxiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and operations users use this skill to query future Eqxiu marketing holidays, plan promotional topics, and generate Eqxiu template mall links from API-returned calendar data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Date and month queries are sent to msearch-api.eqxiu.com. <br>
Mitigation: Use the skill only for public Eqxiu marketing-calendar lookups and avoid sending sensitive or personal calendar information. <br>
Risk: The skill is not intended for legal holiday advice, personal calendars, historical lookups, or non-Eqxiu design tools. <br>
Mitigation: Route those requests to another appropriate source and limit this skill to future Eqxiu marketing events and template links. <br>
Risk: Marketing calendar answers can be wrong if the external API is unavailable or returns unexpected data. <br>
Mitigation: Use the CLI-provided current date and holiday records, preserve API errors instead of fabricating events, and rely on the generated mall_url field for links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eqxiu/eqxiu-market-calendar) <br>
- [Eqxiu publisher profile](https://clawhub.ai/user/eqxiu) <br>
- [API reference](references/API.md) <br>
- [Eqxiu current-date API](https://msearch-api.eqxiu.com/yyyymm) <br>
- [Eqxiu monthly holiday API](https://msearch-api.eqxiu.com/m/holiday/queryByMonth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with CLI-derived JSON calendar records and Eqxiu mall links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses future-only marketing calendar data and CLI-generated mall_url links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
