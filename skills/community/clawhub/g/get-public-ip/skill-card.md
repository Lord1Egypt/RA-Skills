## Description:

Detects the user's public egress IP address by querying disclosed public IP-check services with timeout and fallback behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regexl](https://clawhub.ai/user/regexl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to ask an agent for the current public egress IP address and quickly check network routing across domestic and international connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party IP-check services may observe the user's public IP address and normal request metadata.

Mitigation: Use only when the user explicitly asks to check the public IP, and review the disclosed endpoint list before deployment in privacy-sensitive environments.

Risk: Network failures, service outages, or filtering can prevent a successful IP lookup.

Mitigation: The skill uses multiple disclosed endpoints with per-endpoint timeouts and returns a failure message when no endpoint succeeds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/regexl/skills/get-public-ip)
- [ip.sb public IP endpoint](https://ip.sb)
- [ipip.net public IP endpoint](https://myip.ipip.net)
- [icanhazip public IP endpoint](https://icanhazip.com)
- [httpbin IP endpoint](https://httpbin.org/ip)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status line with the detected IP address, source service, and elapsed time when successful; plain text failure message when unavailable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make short outbound requests to disclosed third-party IP-check services.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
