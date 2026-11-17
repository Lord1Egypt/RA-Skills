## Description:

Access weather, IP geolocation, SMS, email, crypto prices, QR codes, Danish CVR, Whois, phone lookup, UUID, stock data, passwords, and more via the API KISS unified gateway (apikiss.com).

This skill is ready for commercial/non-commercial use.

## Publisher:

[theill](https://clawhub.ai/user/theill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to form authenticated API KISS requests for common utility services such as weather, IP lookup, messaging, email, crypto and stock prices, QR codes, UUIDs, password tools, and domain or phone lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMS, email, and password-check data are sent to API KISS, and documented calls may place sensitive values in URLs.

Mitigation: Send only data you are comfortable sharing with apikiss.com, avoid real or reused passwords, and avoid private SMS or email content unless the user has explicitly approved it.

Risk: Messaging and email endpoints can send content to third-party recipients.

Mitigation: Confirm recipient addresses or phone numbers and message content before issuing any send request.

## Reference(s):

- [API KISS homepage](https://www.apikiss.com)
- [API KISS API base URL](https://www.apikiss.com/api/v1/)
- [ClawHub skill page](https://clawhub.ai/theill/skills/apikiss)
- [ClawHub publisher profile](https://clawhub.ai/user/theill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIKISS_API_KEY for authenticated API calls]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
