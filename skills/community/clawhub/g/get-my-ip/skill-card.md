## Description:

Get the machine's current public IP address by calling `curl ifconfig.me` when the user asks for their IP address, public IP, external IP, or explicitly wants to use ifconfig.me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hilaraklesantosw-art](https://clawhub.ai/user/hilaraklesantosw-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users use this skill to retrieve the current machine's public outbound IP address through ifconfig.me. It is scoped to public IP lookup and not local network discovery, routing diagnostics, interface inspection, or geolocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes an external request to ifconfig.me, which exposes the machine's public outbound IP address to that service.

Mitigation: Use it only when a public IP lookup is intended, and confirm that external IP-check services are allowed in restricted workplace or sensitive network environments.

Risk: The lookup can fail if curl is missing, network access is unavailable, or ifconfig.me is unavailable.

Mitigation: Report that the public IP could not be retrieved and include the brief failure reason when available.

## Reference(s):

- [Project homepage](https://github.com/hilaraklesantosw-art/skills)
- [ClawHub skill page](https://clawhub.ai/hilaraklesantosw-art/skills/get-my-ip)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or concise Markdown with an inline shell command when explanation is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns only the public IP by default; includes a brief error reason when curl, the network, or ifconfig.me is unavailable.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
