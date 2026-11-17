## Description:

Guidance for installing and using Fli correctly as a CLI and MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[punitarani](https://clawhub.ai/user/punitarani)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to install Fli with pipx, run Google Flights searches from the CLI, configure STDIO or HTTP MCP servers, and troubleshoot common setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the Fli package and dependencies from an untrusted source could introduce supply-chain risk.

Mitigation: Install only from trusted package sources, pin reviewed versions in higher-assurance environments, or use an approved internal mirror.

Risk: Running package installation with elevated privileges can increase the impact of a compromised dependency.

Mitigation: Use pipx or another isolated user-level installation path and avoid sudo or administrator privileges.

Risk: Live Google Flights requests can fail temporarily because of rate limiting or upstream availability.

Mitigation: Retry after a short delay and reduce repeated back-to-back searches before treating the local CLI or MCP setup as broken.

## Reference(s):

- [Fli introduction](https://punitarani-fli.mintlify.app/introduction)
- [Fli installation](https://punitarani-fli.mintlify.app/installation)
- [Fli MCP setup](https://punitarani-fli.mintlify.app/mcp/setup)
- [Fli docs index](https://punitarani-fli.mintlify.app/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on CLI and MCP setup guidance; does not produce executable artifacts.]

## Skill Version(s):

0.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
