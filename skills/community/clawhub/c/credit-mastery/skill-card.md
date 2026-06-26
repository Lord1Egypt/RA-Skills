## Description: <br>
Despite the published Credit Mastery name, this release provides guidance and examples for building single-agent and multi-agent systems with the Swarms API, including orchestration patterns, streaming, marketplace publishing, ATP payments, and Solana token launch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NewSoulOnTheBlock](https://clawhub.ai/user/NewSoulOnTheBlock) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders can use this skill as a Swarms API reference for composing agents, selecting swarm architectures, enabling streaming, connecting tools or MCP servers, and preparing marketplace or token launch workflows. Users should treat the Credit Mastery name mismatch as a review signal before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published name does not match the artifact content, which is a Swarms AI orchestration guide rather than a credit-focused skill. <br>
Mitigation: Install only if the intended use is Swarms AI API orchestration, and review the artifact contents before relying on the skill. <br>
Risk: The skill includes workflows that use Solana wallet private keys and can launch tokens or process payments. <br>
Mitigation: Use testnet or a dedicated low-balance wallet, never paste a main wallet private key into prompts or generated code, and require explicit approval before token launches or payments. <br>
Risk: Autonomous sub-agent workflows can delegate tasks and perform file operations. <br>
Mitigation: Restrict selected tools, keep loop counts bounded unless delegation is required, and require human approval for autonomous sub-agent and file-operation workflows. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/NewSoulOnTheBlock/credit-mastery) <br>
- [Swarms Documentation Index](https://docs.swarms.ai/llms.txt) <br>
- [Swarms API Architecture](references/architecture.md) <br>
- [ATP Agent Trade Protocol](references/atp-protocol.md) <br>
- [Swarms Marketplace](references/marketplace.md) <br>
- [Streaming Responses](references/streaming.md) <br>
- [Sub-Agent Delegation](references/sub-agents.md) <br>
- [Tools Integration](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline Python, TypeScript, cURL, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Swarms API endpoint guidance, agent and swarm configuration examples, streaming patterns, tool integration notes, and security-sensitive wallet guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
