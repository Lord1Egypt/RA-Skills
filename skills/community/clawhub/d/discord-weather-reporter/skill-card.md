## Description: <br>
Fetches current weather conditions and forecasts and formats them for Discord display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Discord users and bot operators use this skill to request current conditions, precipitation checks, and multi-day forecasts for cities or airport codes as Discord-ready text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location queries are sent to wttr.in. <br>
Mitigation: Avoid submitting sensitive location details and review whether sharing a location with wttr.in is acceptable for the use case. <br>
Risk: Unnecessary secrets could be exposed if an agent or installer asks for credentials. <br>
Mitigation: Do not provide Discord credentials, webhooks, or API keys for this skill. <br>
Risk: Repeated weather requests may hit service rate limits. <br>
Mitigation: Throttle repeated requests and avoid polling wttr.in more often than needed. <br>


## Reference(s): <br>
- [Discord Weather Reporter on ClawHub](https://clawhub.ai/fuzzyb33s/discord-weather-reporter) <br>
- [wttr.in weather service](https://wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Discord-ready weather text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses wttr.in; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
