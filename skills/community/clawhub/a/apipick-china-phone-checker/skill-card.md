## Description:

Validate Chinese mobile phone numbers using the apipick China Phone Checker API, returning carrier, province, city, zip code, and area code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to validate Chinese mobile phone numbers, identify the carrier, and retrieve associated geographic details through the apipick API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried phone numbers are sent to the third-party apipick.com API.

Mitigation: Only submit numbers the user has permission to check, and disclose the third-party lookup before making requests.

Risk: The skill requires an apipick API key for authenticated requests.

Mitigation: Use the APIPICK_API_KEY environment variable and avoid pasting credentials into chat.

## Reference(s):

- [apipick China Phone Checker API Reference](references/api_reference.md)
- [apipick API Platform](https://www.apipick.com)
- [China Phone Checker Product Page](https://www.apipick.com/check-china-phone)
- [Get apipick API Key](https://www.apipick.com/dashboard/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/javainthinking/skills/apipick-china-phone-checker)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with optional inline bash commands and structured API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIPICK_API_KEY and sends queried phone numbers to apipick.com.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
