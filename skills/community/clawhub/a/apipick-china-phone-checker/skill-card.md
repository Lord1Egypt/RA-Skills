## Description: <br>
Validate Chinese mobile phone numbers using the apipick China Phone Checker API, returning carrier, province, city, zip code, and area code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to verify Chinese mobile numbers and retrieve carrier and geographic metadata from the apipick API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried Chinese phone numbers are sent to apipick.com. <br>
Mitigation: Submit only numbers the user is authorized to check and disclose that the lookup uses the apipick API. <br>
Risk: The apipick API key may be exposed if pasted into chat or logs. <br>
Mitigation: Prefer APIPICK_API_KEY from the environment and avoid asking users to paste secrets unless necessary. <br>
Risk: Successful requests consume apipick account credits. <br>
Mitigation: Confirm the user wants to perform the lookup before making API calls that may consume credits. <br>


## Reference(s): <br>
- [apipick China Phone Checker API Reference](references/api_reference.md) <br>
- [apipick](https://www.apipick.com) <br>
- [China Phone Checker](https://www.apipick.com/check-china-phone) <br>
- [Get API Key](https://www.apipick.com/dashboard/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/javainthinking/apipick-china-phone-checker) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or text summaries with optional JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIPICK_API_KEY and sends queried phone numbers to apipick.com; each successful request costs 1 credit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
