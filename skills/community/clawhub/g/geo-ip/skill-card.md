## Description:

Look up geographic location for any IP address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up city, region, country, coordinates, and ISP details for a public IP address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Looking up sensitive internal, customer, or confidential IP addresses sends those addresses to ipinfo.io.

Mitigation: Use the skill only for public IP lookups unless sharing the queried address with ipinfo.io is acceptable.

Risk: The skill depends on curl and the availability of the public ipinfo.io API.

Mitigation: Confirm curl is available and treat API failures or missing responses as lookup failures rather than authoritative location results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xejrax/skills/geo-ip)
- [ipinfo.io](https://ipinfo.io)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text output from an IP geolocation lookup, with shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and uses the public ipinfo.io API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
