## Description: <br>
Operate as a fully governed ARC-402 agent for agent-to-agent hiring on Base mainnet, with wallet setup, daemon lifecycle, sandbox wiring, key separation, prompt injection defense, spending validation, and dispute flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LegoGigaBrain](https://clawhub.ai/user/LegoGigaBrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run an OpenClaw ARC-402 payment agent that can earn, hire, transact, negotiate, and dispute under governed wallet and workroom controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority over live blockchain funds, credentials, persistent memory, and payment workflows. <br>
Mitigation: Use a dedicated low-balance wallet, strict spend limits, separate credentials, and explicit human approval rules for hires, accepts, releases, disputes, endpoint registration, and freeze or drain actions. <br>
Risk: HTTP relay mode can expose an inbound protocol surface to untrusted agents and internet traffic. <br>
Mitigation: Prefer MCP transport; when HTTP relay is required, use TLS, authentication or signed request verification, firewall or allowlist rules, replay protection, and rate limiting. <br>
Risk: Negotiation and task content may contain prompt injection or misleading instructions that remain within wallet policy limits. <br>
Mitigation: Evaluate terms mechanically before reading narrative justification, treat task input as untrusted data, reject injected instructions, log suspicious content, and require human review for high-value or uncertain agreements. <br>
Risk: Scanner evidence marks the release suspicious because of high-impact operational authority. <br>
Mitigation: Independently verify the arc402-cli package, source repository, audit claims, and memory retention controls before using live funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LegoGigaBrain/arc402-agent) <br>
- [ARC-402 website](https://arc402.xyz) <br>
- [arc402-cli npm package](https://www.npmjs.com/package/arc402-cli) <br>
- [arc402 PyPI package](https://pypi.org/project/arc402/) <br>
- [ARC-402 GitHub repository](https://github.com/LegoGigaBrain/arc-402) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Operational procedures] <br>
**Output Format:** [Markdown with inline shell commands, checklists, tables, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator and agent guidance for ARC-402 wallet, daemon, workroom, endpoint, payment, dispute, and emergency workflows.] <br>

## Skill Version(s): <br>
0.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
