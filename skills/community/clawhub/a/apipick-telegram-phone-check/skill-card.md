## Description: <br>
Check if a phone number is registered on Telegram using the apipick Telegram Checker API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to check Telegram registration status for a phone number with an international country code and return available public profile fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Phone-number lookups are privacy-sensitive and send queried numbers to apipick.com. <br>
Mitigation: Use the skill only for numbers you own or are authorized to check, and avoid contact discovery, stalking, doxxing, or bulk enumeration. <br>
Risk: The skill requires an apipick API key for authenticated requests. <br>
Mitigation: Keep the API key in APIPICK_API_KEY, do not expose it in chat or logs, and confirm the user is comfortable using apipick credits before making requests. <br>


## Reference(s): <br>
- [apipick Telegram Phone Checker API Reference](artifact/references/api_reference.md) <br>
- [apipick API Platform](https://www.apipick.com) <br>
- [Telegram Checker Product Page](https://www.apipick.com/check-phone-telegram) <br>
- [Get API Key](https://www.apipick.com/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, shell commands, guidance] <br>
**Output Format:** [Markdown with optional JSON response summaries and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIPICK_API_KEY for authenticated requests to apipick.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
