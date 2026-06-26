## Description: <br>
Provides Chinese-language productivity lookups for express tracking, currency conversion, China holiday schedules, and phone or IP location queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxg852621787](https://clawhub.ai/user/dxg852621787) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query common China-focused logistics, currency, holiday, phone-number, and IP-location information from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup identifiers such as tracking numbers, phone numbers, and IP addresses are sent to public third-party services. <br>
Mitigation: Avoid using sensitive, private, or regulated identifiers unless the providers are acceptable for the user's environment and data handling requirements. <br>
Risk: IP location lookup uses an HTTP endpoint according to the security guidance. <br>
Mitigation: Treat IP lookup results as unsuitable for sensitive contexts until the skill documents providers clearly and uses HTTPS for that lookup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxg852621787/china-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/dxg852621787) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON-formatted command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lookup results may include third-party API responses for tracking, exchange rates, holiday schedules, phone location, and IP location.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
