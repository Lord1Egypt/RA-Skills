## Description:

Helps developers diagnose DNS resolution, network connectivity, port reachability, and TLS certificate issues through guided checks and command examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation workflows use this skill to troubleshoot DNS resolution, network connectivity, port reachability, and certificate diagnostics. It is not intended for non-technical general-purpose tasks or complex decisions that require human judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run shell commands for live network and certificate diagnostics.

Mitigation: Review proposed commands before execution and use the skill only when live network checks and local diagnostic output are intended.

Risk: The documented scope and safety claims are broader than the DNS and networking behavior supported by the artifact.

Mitigation: Limit use to DNS, connectivity, port, and certificate troubleshooting rather than relying on it for broader operational or security decisions.

Risk: Use in sensitive environments may expose local diagnostic details or trigger outbound network probes.

Mitigation: Run in an approved environment with appropriate network permissions and avoid sharing sensitive command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dns-networking-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON-style diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live network diagnostic commands and local diagnostic output for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
