## Description:

Helps developers and operations teams debug DNS resolution, TLS certificate details, and network connectivity through guided agent commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to troubleshoot DNS failures, inspect certificate chains, test ports, and assess network connectivity. It is intended for explicit technical diagnostic requests rather than general non-technical tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes executable DNS, certificate, and connectivity command examples that could probe systems or networks.

Mitigation: Use it only for explicit network-diagnostic requests and avoid probing internal, third-party, or production hosts without permission.

Risk: Broad activation wording could cause the skill to be used outside its intended diagnostic scope.

Mitigation: Restrict use to DNS, certificate, port, and connectivity troubleshooting tasks.

Risk: The artifact includes a generic API key environment variable example.

Mitigation: Do not provide credentials unless a concrete, reviewed command requires them, and keep secrets out of logs and version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dns-networking-paid)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable network diagnostic commands and structured JSON-style result summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
