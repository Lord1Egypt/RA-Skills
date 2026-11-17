## Description:

Looks up geographic location and network information for public IPv4 or IPv6 addresses using the apipick IP Geolocation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

External users, developers, and support teams use this skill to geolocate public IP addresses or inspect ISP, ASN, timezone, currency, and related network data through the apipick API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IP addresses submitted for lookup, including the caller's current public IP in no-parameter mode, are sent to apipick with the API key.

Mitigation: Avoid submitting sensitive, customer, internal, or unauthorized IP data, and confirm the user intends to send the address to apipick before lookup.

Risk: The skill requires an apipick API key for requests.

Mitigation: Use the APIPICK_API_KEY environment variable and avoid exposing the key in prompts, logs, screenshots, or shared output.

## Reference(s):

- [apipick IP Geolocation API Reference](artifact/references/api_reference.md)
- [apipick API platform](https://www.apipick.com)
- [apipick IP Geolocation product page](https://www.apipick.com/ip-geolocation)
- [ClawHub skill page](https://clawhub.ai/javainthinking/skills/apipick-ip-geolocation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown or plain text with optional curl commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIPICK_API_KEY; each successful API request uses 1 apipick credit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
