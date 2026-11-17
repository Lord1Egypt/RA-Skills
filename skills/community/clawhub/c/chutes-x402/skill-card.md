## Description:

Build a pay-per-inference proxy for Bittensor Chutes AI and accept USDC payments for decentralized AI inference using x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[primer-dev](https://clawhub.ai/user/primer-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI agent operators, and API resellers use this skill to scaffold and configure a paid proxy that forwards requests to Bittensor Chutes AI while collecting USDC payments through x402.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned third-party package and scaffolding commands.

Mitigation: Review or pin the referenced x402 packages and generated dependencies before installing or deploying.

Risk: The generated proxy requires Chutes API keys, wallet addresses, and payment configuration.

Mitigation: Use low-privilege or throwaway keys during testing, keep .env files out of version control and screenshots, and use platform secret managers for deployment.

Risk: The generated project may handle paid inference requests and customer-facing payment behavior.

Mitigation: Review generated code and pricing configuration before adding real API credentials, wallet details, or production payment settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/primer-dev/skills/chutes-x402)
- [Chutes AI](https://chutes.ai)
- [Bittensor](https://bittensor.com)
- [x402 Protocol](https://x402.org)
- [x402 Bittensor documentation](https://x402.org/docs/bittensor.html)
- [Primer Systems](https://primer.systems)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands, code snippets, tables, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include generated project scaffolding steps for Node.js/TypeScript or Python and environment variable setup for Chutes and wallet configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
