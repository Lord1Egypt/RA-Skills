## Description:

Register and manage ICANN domains for AI agents. Wallet authentication (SIWE/SIWS), USDC payments on Base or Solana, full DNS management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vibrant](https://clawhub.ai/user/vibrant)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to check domain availability, register ICANN domains with wallet-authenticated USDC payments, and manage DNS records, nameservers, and registrant profiles for agent projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-funded domain purchases can spend USDC if an agent proceeds without sufficient user review.

Mitigation: Use a dedicated low-balance wallet and require a clear quote plus explicit user approval before any domain purchase.

Risk: DNS record updates, DNS deletions, and nameserver changes can disrupt an active domain.

Mitigation: Require explicit user approval before DNS deletion, DNS update, or nameserver change, and review the proposed domain and record values before execution.

Risk: Wallet JSON files can expose funds or account control if mishandled.

Mitigation: Protect wallet JSON files and avoid sharing them with untrusted agents, logs, or repositories.

Risk: Installing an unpinned external Python package can introduce supply-chain uncertainty.

Mitigation: Pin and verify the agentns-client package where possible before installing or deploying the skill.

## Reference(s):

- [AgentNS homepage](https://agentns.xyz)
- [AgentNS API docs](https://agentns.xyz/docs)
- [agentns-client on PyPI](https://pypi.org/project/agentns-client/)
- [agentns_client GitHub repository](https://github.com/vibrant/agentns_client)
- [ClawHub skill page](https://clawhub.ai/vibrant/skills/agentns)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes client workflow examples, wallet setup notes, DNS operations, nameserver management, registrant profile handling, and error handling guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
