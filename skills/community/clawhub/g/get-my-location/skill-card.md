## Description:

Get current IP location info, including country, province, city, and coordinates, with multi-source fallback and no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etmnb](https://clawhub.ai/user/etmnb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need IP-based geolocation for the current machine or a specified IPv4 or IPv6 address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IP/location lookups are sent to outside services.

Mitigation: Review before installing in privacy-sensitive environments and add a clear privacy notice or confirmation step before lookups.

Risk: The fallback chain can use an unencrypted HTTP provider.

Mitigation: Restrict lookups to HTTPS providers or remove the plaintext ip-api.com fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/etmnb/skills/get-my-location)
- [freegeoip.app JSON endpoint](https://freegeoip.app/json/)
- [api.ipbase.com JSON endpoint](https://api.ipbase.com/v1/json/)
- [ip-api.com JSON endpoint](http://ip-api.com/json/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable location summary or JSON from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IP address, country, region, city, postal code, coordinates, time zone, and data source.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
