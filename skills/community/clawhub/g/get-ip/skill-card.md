## Description:

Get current public IP address and geolocation information. Use when users ask about IP addresses, network location, or want to check their public IP. Supports both fetching IP info and displaying it clearly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for the current public IP address and approximate network location, with fallback commands when the primary lookup service fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IP and approximate location lookups contact third-party web services.

Mitigation: Install only when this network behavior is acceptable, ask explicitly before IP lookup, and prefer HTTPS-only endpoints, timeouts, response validation, and an explicit consent step before geolocation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidu/skills/get-ip)
- [Publisher profile](https://clawhub.ai/user/qidu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with inline shell commands and optional IP geolocation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact public IP and geolocation providers, including ipip.net, icanhazip.com, ifconfig.me, api.ipify.org, and ipinfo.io.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
