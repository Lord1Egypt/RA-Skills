## Description: <br>
Gets current weather, multi-day forecasts, clothing index, and feels-like temperature for worldwide city queries, with SkillPay.me billing at 0.001 USDT per call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kim1903](https://clawhub.ai/user/kim1903) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch weather conditions, short-range forecasts, feels-like temperature, and clothing recommendations for a requested city. The billing command can charge a SkillPay account when configured with credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The billing script can charge a SkillPay account by default when a SKILLPAY_API_KEY is configured. <br>
Mitigation: Require explicit user approval before running billing actions, and do not provide SKILLPAY_API_KEY unless billing is intended. <br>
Risk: Weather requests send user-provided city names to wttr.in. <br>
Mitigation: Use the weather and forecast commands only when the user is comfortable sharing the requested city with the external weather service. <br>
Risk: Payment flow trust depends on the package identity and publisher. <br>
Mitigation: Verify the publisher handle kim1903 and the skill page before trusting SkillPay payment links or charge behavior. <br>


## Reference(s): <br>
- [Clothing Index Reference](references/clothing-index.md) <br>
- [Skill page](https://clawhub.ai/kim1903/aaad123) <br>
- [Publisher profile](https://clawhub.ai/user/kim1903) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON returned by command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Weather and clothing outputs may include city, country, temperature, feels-like temperature, humidity, wind, UV, precipitation, and recommendation fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
