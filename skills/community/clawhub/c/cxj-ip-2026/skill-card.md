## Description:

Get both public (external) and local (internal) IP addresses using simple shell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxinjie005](https://clawhub.ai/user/chenxinjie005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support engineers, and end users use this skill to identify the machine's public IP for allowlists, VPNs, and firewall setup, or its local IPv4 address for LAN troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public IP lookup commands disclose the requester IP address to the selected external service.

Mitigation: Use the documented HTTPS endpoints only when that disclosure is acceptable; in restricted enterprise environments, use an approved internal endpoint or ask before running the public-IP step.

Risk: Local IP commands can reveal internal network addressing in chat transcripts or logs.

Mitigation: Share local IP output only in trusted troubleshooting contexts and redact addresses when they are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenxinjie005/skills/cxj-ip-2026)
- [ifconfig.me public IP endpoint](https://ifconfig.me)
- [api.ipify.org public IP endpoint](https://api.ipify.org)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public HTTPS IP lookup endpoints and local network inspection commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
