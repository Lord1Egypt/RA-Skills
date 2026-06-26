## Description: <br>
Looks up geographic location and network information for public IPv4 or IPv6 addresses using the apipick IP Geolocation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and support teams use this skill to identify the country, city, timezone, currency, ISP, and ASN associated with a public IP address or with the caller's current public IP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an apipick API key and may spend apipick credits when requests are made. <br>
Mitigation: Use the APIPICK_API_KEY environment variable, avoid exposing the key in prompts or logs, and confirm credit-sensitive lookups before repeated use. <br>
Risk: Queried IP addresses are sent to apipick.com for geolocation. <br>
Mitigation: Avoid submitting sensitive IP addresses unless the user accepts sharing them with the provider. <br>
Risk: Omitting the IP parameter looks up the caller's own public IP and approximate network location. <br>
Mitigation: Require confirmation before self-IP lookup when the user has not clearly requested it. <br>


## Reference(s): <br>
- [apipick IP Geolocation API Reference](references/api_reference.md) <br>
- [apipick IP Geolocation API endpoint](https://www.apipick.com/api/ip-geolocation) <br>
- [apipick IP Geolocation product page](https://www.apipick.com/ip-geolocation) <br>
- [apipick API keys](https://www.apipick.com/dashboard/api-keys) <br>
- [ClawHub skill page](https://clawhub.ai/javainthinking/apipick-ip-geolocation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown text with optional curl examples and JSON field summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include location, timezone, currency, ISP, ASN, API error, credit usage, and remaining credit information returned by apipick.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
