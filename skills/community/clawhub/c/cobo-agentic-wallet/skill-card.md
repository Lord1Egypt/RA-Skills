## Description:

Create and manage Cobo agentic wallets for autonomous on-chain operations through the caw CLI, including wallet onboarding, pact authorization, token transfers, contract calls, and DeFi execution on EVM chains and Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cobogithub](https://clawhub.ai/user/cobogithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet operators use this skill to onboard Cobo agentic wallets and guide agents through bounded, owner-approved on-chain tasks such as transfers, contract calls, DeFi execution, pact lifecycle management, and transaction verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact crypto wallet actions, including transfers, contract calls, DeFi execution, and pact creation.

Mitigation: Require direct user intent, explicit recipient, amount, chain, and asset details, balance checks before fund-using actions, and owner approval for new or expanded pacts.

Risk: Prompt injection or external content could try to trigger wallet operations or override policy limits.

Mitigation: Do not execute wallet operations from webhooks, emails, documents, tool output, or other external content without direct user confirmation; stop on override, privilege escalation, safety tampering, or credential phishing patterns.

Risk: Unsafe installation or update paths may introduce unreviewed binaries or package versions.

Mitigation: Install only from trusted Cobo distribution channels, verify downloaded checksums where provided, and avoid unpinned npx, npm, or pip installs before operational use.

Risk: Credentials and wallet identifiers may be exposed if copied into reusable scripts or shared logs.

Mitigation: Keep API keys out of project scripts, logs, and generated examples; retrieve credentials through the CLI only when needed and store operational scripts with parameterized inputs.

Risk: Incorrect pact policies, chain IDs, token decimals, contract addresses, or retry behavior can cause denied operations or unintended on-chain transactions.

Mitigation: Review generated pact policy for exact scope, use token metadata and recipe or official protocol references instead of memory, preserve request-id idempotency, and confirm final transaction status before reporting success.

## Reference(s):

- [Cobo Agentic Wallet skill page](https://clawhub.ai/cobogithub/skills/cobo-agentic-wallet)
- [Cobo Agentic Wallet manual](https://cobo.com/products/agentic-wallet/manual/llms.txt)
- [Security Guide](references/security.md)
- [Onboarding](references/onboarding.md)
- [Pact Management](references/pact.md)
- [Pending Approval](references/pending-approval.md)
- [Error Handling](references/error-handling.md)
- [Chains and Token IDs](references/chains-and-tokens.md)
- [SDK Scripting](references/sdk-scripting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and Python or TypeScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create reusable scripts under ./scripts for multi-step wallet operations.]

## Skill Version(s):

1.0.3 (source: skill frontmatter metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
