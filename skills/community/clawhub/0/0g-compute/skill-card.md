## Description:

Use cheap, TEE-verified AI models from the 0G Compute Network as OpenClaw providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[in-liberty420](https://clawhub.ai/user/in-liberty420)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to discover 0G Compute Network model providers, verify provider integrity, manage wallet and sub-account funding, compare provider pricing, and configure verified providers for OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires wallet private keys and provider API secrets.

Mitigation: Use a dedicated low-balance wallet, avoid passing private keys directly in shell commands, restrict permissions on 0G and OpenClaw config files, and keep secrets out of source control and logs.

Risk: The workflow includes fund-moving commands such as deposits, transfers, retrievals, and refunds.

Mitigation: Confirm every fund-moving command manually, verify provider addresses before transferring funds, and monitor sub-account balances.

Risk: The installation path uses a global npm package install that may be unpinned.

Mitigation: Pin and verify the CLI package where possible, review the package before installation, and avoid running npm as root.

Risk: Model providers may be unhealthy, misconfigured, or fail TEE verification.

Mitigation: Run provider verification before use, check provider health and uptime, and avoid providers that fail attestation.

## Reference(s):

- [0G Compute CLI Reference](references/cli-reference.md)
- [Configuring OpenClaw for 0G Compute Network](references/openclaw-config.md)
- [0G Serving Broker npm Package](https://www.npmjs.com/package/@0glabs/0g-serving-broker)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [CoinGecko 0G Token Price API](https://api.coingecko.com/api/v3/simple/price?ids=zero-gravity&vs_currencies=usd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, OpenClaw provider configuration snippets, pricing comparisons, and provider verification guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
