## Description: <br>
Forecast the probability of a future event with the Axion API. Use when asked the odds, likelihood, or a prediction for an uncertain or future event. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternis](https://clawhub.ai/user/eternis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to request research-backed probability forecasts for uncertain future events, scenarios, markets, deals, elections, geopolitics, and product launches through the Axion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecast questions and related context are sent to the Axion remote API. <br>
Mitigation: Install and use only when users are comfortable sending forecast prompts to Axion. <br>
Risk: API use consumes prepaid Axion credits and includes higher-impact account actions such as stopping paid work, deleting threads, configuring webhooks, sharing forecasts publicly, and starting credit purchases. <br>
Mitigation: Require explicit user confirmation before public sharing, deletion, stop requests, webhook configuration, or credit purchase flows. <br>
Risk: The skill depends on an Axion API key. <br>
Mitigation: Keep AXION_API_KEY private, read it from the environment, and never print or hard-code it. <br>


## Reference(s): <br>
- [Axion API reference](references/axion-api.md) <br>
- [Axion documentation](https://axion.eternis.ai/docs) <br>
- [ClawHub Axion skill page](https://clawhub.ai/eternis/skills/axion) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Markdown, Analysis] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast results include probabilities, confidence bounds, resolution dates, and reasoning from the Axion API.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
