## Description:

This skill enables IP address masking and accessing hidden services on the Anyone Network by routing requests through the Anyone Protocol VPN network using a local SOCKS5 proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ra3ka](https://clawhub.ai/user/ra3ka)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to install and run an Anyone Network SOCKS5 proxy, then route HTTP requests through it for IP masking or access to hidden services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and run a mutable third-party npm package with authority over network traffic.

Mitigation: Use a pinned, reviewed package version where possible, avoid global installation, and run the proxy with least privilege.

Risk: Traffic routed through the proxy may include secrets or regulated data.

Mitigation: Do not route sensitive data through the proxy unless the provider, environment, and compliance posture have been approved.

## Reference(s):

- [Anyone Network](https://anyone.io)
- [Anyone IP Check API](https://check.en.anyone.tech/api/ip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the third-party @anyone-protocol/anyone-client npm package and a local SOCKS5 proxy process.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
