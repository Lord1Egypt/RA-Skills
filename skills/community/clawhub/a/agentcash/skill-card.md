## Description:

Agentcash guides agents through pay-per-call x402/MPP API access with wallet-paid USDC requests, service discovery, endpoint checks, and fetch commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maliot100x](https://clawhub.ai/user/maliot100x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Agentcash to discover x402/MPP payment-protected services, check endpoint pricing and schemas, and call paid APIs through wallet-authenticated CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-enabled API calls can spend user funds or cause external side effects without enough scoping.

Mitigation: Require explicit spending limits and user confirmation before paid calls, especially for expensive operations.

Risk: The artifact uses unpinned `npx agentcash@latest` commands.

Mitigation: Pin the package version or run commands only in a low-privilege environment after review.

Risk: Credential-handling guidance in the artifact includes storing credentials under `/root`.

Mitigation: Use a user-scoped secret store or reviewed credential path with restrictive permissions, and avoid saving secrets under `/root`.

Risk: Persisting newly discovered origins can expand future agent behavior without review.

Mitigation: Require human review before adding or persisting discovered service origins.

## Reference(s):

- [Agentcash homepage](https://agentcash.dev)
- [ClawHub Agentcash skill page](https://clawhub.ai/maliot100x/skills/agentcash)
- [x402-Agent-Pay.com Reference](artifact/references/x402-agent-pay.md)
- [Pump.fun Token Data Sources](artifact/references/pumpfun-data-sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead to paid API calls when an agent follows the generated commands; use spending limits and explicit confirmations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
