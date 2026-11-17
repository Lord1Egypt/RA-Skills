## Description:

Use AgentPMT without an account: connect OpenClaw and autonomous AI agents to AgentPMT tools, workflows, skills, agent-to-agent work, and paid capabilities through a revocable AgentAddress with credits or a funded x402 wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let agents call AgentPMT tools and workflows without an account bearer token, using signed AgentAddress credit requests or direct x402 payments. It focuses on payment setup, approval gates, request signing, endpoint usage, and safe handling of wallet-backed access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet keys, signatures, payment headers, or session nonces could expose spending authority if copied into prompts, logs, commits, transcripts, or generated files.

Mitigation: Store secrets in a real secret manager and pass only scoped secret references to the agent runtime.

Risk: Direct x402 payments or signed AgentAddress requests can spend funds or credits if an agent signs unapproved actions, payees, networks, tokens, or amounts.

Mitigation: Use a dedicated low-balance wallet or AgentAddress and enforce allowlists, per-call spending limits, and explicit approval or a pre-approved policy before signing.

Risk: Unpinned install commands may pull changed package versions into privileged or shared environments.

Mitigation: Install from ClawHub/OpenClaw or pinned reviewed sources, and use hash-pinned dependencies in isolated environments for production.

## Reference(s):

- [AgentPMT AgentAddress](https://www.agentpmt.com/agentaddress)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/agentpmt-no-account-agentaddress-x402)
- [AgentPMT Account MCP/REST Setup Skill](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is Skill](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, JavaScript, shell, text, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint patterns, signing examples, payment approval checks, and error-handling guidance.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
