## Description:

Checks whether a phone number is registered on Telegram using the apipick Telegram Checker API and returns registration status plus available public profile details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent to check Telegram registration status for specific phone numbers when they have a legitimate, authorized reason to do so.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone numbers and returned Telegram profile data are sent to apipick.

Mitigation: Use the skill only for specific phone numbers where there is consent, authorization, or another legitimate basis, and avoid retaining raw lookup results longer than necessary.

Risk: The lookup capability can support broad enumeration, stalking, or profiling.

Mitigation: Avoid bulk checks and refuse requests that appear to target people without a legitimate purpose.

Risk: The APIPICK_API_KEY is a credential required for API access.

Mitigation: Store the key in the APIPICK_API_KEY environment variable and do not paste, log, or expose it in agent output.

## Reference(s):

- [apipick Telegram Phone Checker API Reference](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/javainthinking/skills/apipick-telegram-phone-check)
- [apipick API Platform](https://www.apipick.com)
- [Telegram Checker Product Page](https://www.apipick.com/check-phone-telegram)
- [apipick API Keys](https://www.apipick.com/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIPICK_API_KEY and sends phone numbers to the apipick API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
