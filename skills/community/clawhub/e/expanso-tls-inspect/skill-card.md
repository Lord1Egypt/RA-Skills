## Description:

Inspect TLS certificates for expiry, subject alternative names, chain validity, and cipher details using Expanso Edge pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to inspect TLS certificate metadata for a supplied host through CLI or MCP-style Expanso Edge pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host input can run unintended shell commands in one execution path.

Mitigation: Only pass trusted hostnames and review the shell command construction before installing or running the skill.

Risk: One execution path can return fabricated certificate-valid results.

Mitigation: Do not rely on MCP certificate validity results until the certificate validation logic is fixed.

Risk: The MCP server could be exposed on a network.

Mitigation: Run the MCP server locally only and do not expose it on a network.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-tls-inspect)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON certificate inspection results with supporting Markdown and bash usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include certificate details, validity status, and inspection metadata for a supplied host.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
