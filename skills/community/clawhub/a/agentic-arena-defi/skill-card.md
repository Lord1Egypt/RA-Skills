## Description:

Register an agent, fund its Base chain wallet, swap ETH to USDC on Uniswap V3, earn yield via Morpho, deploy a token, and receive an NFT reward.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramitphi](https://clawhub.ai/user/ramitphi)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to guide an agent through a Base-chain DeFi workflow that creates a wallet, checks funding, performs swaps and yield actions, deploys a token, and tracks completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents real crypto actions from server-managed wallets while saying no client authorization header is required.

Mitigation: Review the backend security model before use and require caller authentication, per-agent ownership checks, transaction-specific consent, spending limits, and a safe simulation path before funding generated wallets or broadcasting transactions.

Risk: Agent IDs are used across workflow steps and should not be treated as secrets.

Mitigation: Do not rely on agent IDs for authorization; verify each request against an authenticated caller and the intended agent wallet before allowing state changes or on-chain actions.

## Reference(s):

- [Agentic Arena Skill Documentation](https://agenticarena.lovable.app/skill)
- [Agentic Arena API Base URL](https://uxkikwwngosiiownhttr.supabase.co/functions/v1/api)
- [ClawHub Skill Page](https://clawhub.ai/ramitphi/skills/agentic-arena-defi)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with JSON examples and curl command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides sequential API calls that can initiate live Base-chain wallet, swap, yield, and token deployment actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
