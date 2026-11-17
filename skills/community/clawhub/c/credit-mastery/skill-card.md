## Description:

Provides guidance and examples for building Swarms API agents, multi-agent swarms, streaming workflows, tool integrations, marketplace publishing, Solana token launches, and ATP payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newsoulontheblock](https://clawhub.ai/user/newsoulontheblock)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to draft Swarms API agent, swarm, streaming, tool, marketplace, token launch, and ATP integration workflows with example requests and configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes workflows that normalize sending Solana wallet private keys to remote services.

Mitigation: Avoid funded or primary wallets; prefer local signing, wallet adapters, hardware wallets, or a dedicated low-balance test wallet.

Risk: The skill describes broad autonomous file-tool configurations for agents.

Mitigation: Restrict autonomous agents to the minimum required tool allowlist and avoid selected_tools="all" unless file access is intentionally sandboxed and reversible.

Risk: The skill recommends SDK and API workflows that may change or execute against third-party services.

Mitigation: Pin and isolate SDK installs, keep API keys in environment variables, and review generated requests before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/newsoulontheblock/skills/credit-mastery)
- [Publisher Profile](https://clawhub.ai/user/newsoulontheblock)
- [Swarms Docs Index](https://docs.swarms.ai/llms.txt)
- [Swarms API Architecture](references/architecture.md)
- [Sub-Agent Delegation](references/sub-agents.md)
- [ATP Agent Trade Protocol](references/atp-protocol.md)
- [Swarms Marketplace](references/marketplace.md)
- [Streaming Responses](references/streaming.md)
- [Tools Integration](references/tools.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code examples and API request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Python, TypeScript, cURL, JSON payloads, environment-variable guidance, and endpoint configuration details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
