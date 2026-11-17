## Description:

JavaScript SDK and CLI guidance for Circle Chain, covering user authentication, wallet operations, blocks, mining, transfers, contacts, and HTTP configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lidh04](https://clawhub.ai/user/lidh04)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when integrating Circle Chain from Node.js or browser code, using the circle CLI, or maintaining the @lidh04/circle-chain-sdk package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external npm package for wallet, account, transfer, and payment-password workflows.

Mitigation: Use a reviewed pinned package version and avoid entering account, wallet, or payment-password data until package provenance and behavior are acceptable.

Risk: The SDK may contact a GeoIP service to choose the gateway host.

Mitigation: Set an explicit gateway host or set CIRCLE_SKIP_GEO=1 when automatic GeoIP-based host selection is not desired.

Risk: Global installation exposes the circle command from the trusted package on the local system.

Mitigation: Avoid global installation unless the circle command is required; prefer local project installation for scoped use.

## Reference(s):

- [Circle Chain Skill on ClawHub](https://clawhub.ai/lidh04/skills/circle-chain)
- [Publisher Profile](https://clawhub.ai/user/lidh04)
- [ipwho.is GeoIP Service](https://ipwho.is/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, SDK usage patterns, and HTTP configuration guidance.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
