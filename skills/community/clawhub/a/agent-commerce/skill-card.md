## Description:

Put the Agent Commerce Gateway (npm @devlab.group/agent-commerce) in front of an existing HTTP API so AI agents can call and pay for its endpoints over HTTP or MCP, with x402 stablecoin payments. Use when adding agent payments, x402 or paid MCP tools to an API, when configuring, validating or starting the gateway, or when fixing errors from its validate, doctor or start commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergeevdmitry](https://clawhub.ai/user/sergeevdmitry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API operators use this skill to put a payment gateway in front of an existing HTTP API, configure agent access over HTTP or MCP, and validate, operate, or troubleshoot fixed-price x402 stablecoin payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public gateway or directly reachable backend could expose unintended API endpoints or let callers bypass payment checks.

Mitigation: Expose only intended endpoints, restrict backend access to the gateway or equivalent controls, and apply the documented authentication and TLS protections before public deployment.

Risk: Secrets and payment receipts contain sensitive operational data, and a payment may settle even when the backend later fails.

Mitigation: Keep secrets out of chat and logs, protect the receipt database, start on testnet, and check receipts after backend failures before retrying. Require explicit user approval before mainnet.

Risk: The security review covers the bundled skill instructions and configuration, not the external npm runtime or its dependencies.

Mitigation: Review the installed package and dependencies as part of deployment; do not treat the bundled-file review as an audit of runtime code.

## Reference(s):

- [Project repository](https://github.com/devlab-group/agent-commerce)
- [Configuration reference](https://github.com/devlab-group/agent-commerce/blob/master/docs/configuration.md)
- [Config reference](references/config.md)
- [Production guidance](references/production.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Operational guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup steps, configuration examples, validation checkpoints, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
