## Description: <br>
Fetch exchange rates and convert currencies with the free Frankfurter API (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanookai](https://clawhub.ai/user/nanookai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch current or historical foreign exchange reference rates, convert currencies, inspect available currencies and providers, and shape Frankfurter API responses for integration work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to use public Frankfurter API exchange rates as if they were live trading prices. <br>
Mitigation: Treat returned rates as daily reference rates, read the response date, and avoid using them as live tick data. <br>
Risk: Compliance-sensitive work may require an official data source rather than blended exchange-rate data. <br>
Mitigation: Check the returned provider information and pin an appropriate provider when official or compliance-sensitive rates are required. <br>


## Reference(s): <br>
- [Frankfurter API Skill Page](https://clawhub.ai/nanookai/skills/frankfurter-api) <br>
- [Frankfurter API](https://api.frankfurter.dev) <br>
- [Frankfurter API v2 Endpoint Reference](references/endpoints.md) <br>
- [Frankfurter v1 API Legacy Reference](references/v1-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, markdown] <br>
**Output Format:** [Markdown guidance with HTTP request examples, JSON or CSV response examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable files; the skill may guide agents to call the public Frankfurter API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
