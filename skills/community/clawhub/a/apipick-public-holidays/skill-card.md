## Description:

Queries the apipick Public Holidays API to return sorted public holiday dates and official names for 100+ countries by ISO country code and year.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up national public holidays for planning, date checks, and country-specific holiday lists. It is useful when a user provides a country name or ISO country code and an optional calendar year.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Holiday lookups send the requested country and year to apipick with the user's API key.

Mitigation: Store the key in APIPICK_API_KEY where possible and avoid including unrelated sensitive information in holiday lookup requests.

Risk: The skill depends on an external API, so invalid keys, insufficient credits, or service errors can prevent successful results.

Mitigation: Check that APIPICK_API_KEY is configured, account credits are available, and API error responses are reported clearly to the user.

## Reference(s):

- [apipick Public Holidays API Reference](references/api_reference.md)
- [apipick API Platform](https://www.apipick.com)
- [apipick Public Holidays Product Page](https://www.apipick.com/public-holidays)
- [Get apipick API Key](https://www.apipick.com/dashboard/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/javainthinking/skills/apipick-public-holidays)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with optional shell commands and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIPICK_API_KEY and sends the requested country and year to apipick.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
