## Description:

Financial management for AI agents. Track LLM inference costs, record confirmed income, manage multi-provider crypto wallets, and compute a Financial Health Score. Use when you need to check your balance, record a cost or expense, report financial health, manage your wallet, or assess economic sustainability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use AgentBooks to monitor an agent's financial state, record costs and confirmed income, manage wallet providers, and route agent behavior based on financial health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned third-party wallet and ledger CLI that can affect agent behavior.

Mitigation: Review and pin the AgentBooks npm package before use, run it first in an isolated directory or container, and require explicit approval before wallet connection, sync, income recording, or behavior changes based on financial-health output.

Risk: Wallet and provider operations may involve sensitive financial accounts.

Mitigation: Use testnets or throwaway wallets for initial evaluation and avoid production wallets or private keys until the provider authentication flow has been audited.

## Reference(s):

- [Financial Health Reference](references/financial-health.md)
- [AgentBooks Repository](https://github.com/acnlabs/agentbooks)
- [AgentBooks ClawHub Skill Page](https://clawhub.ai/neiljo-gy/skills/agent-books)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run the external agentbooks CLI and to adjust behavior based on financial-health output.]

## Skill Version(s):

0.1.5 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
