## Description:

Inspects Coinbase CDP and AgentKit wallet configuration, checks an existing account with read-only tools, and inventories exposed actions before protocol use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to diagnose an existing Coinbase wallet integration, verify scoped read access and network identity, and report available agent actions without signing or moving funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proposed correction or exposed action could grant financial authority beyond a readiness check.

Mitigation: Review corrections before applying them; require separate approval for account creation, signing, transfers, or payments.

Risk: Public balance reads or credential presence could be mistaken for authenticated wallet or signing readiness.

Mitigation: Record what was actually tested and mark authenticated lookup and signing as unverified unless separately confirmed.

Risk: Wallet credentials could be exposed during inspection.

Mitigation: Check credential presence only; never print or disclose secret values.

## Reference(s):

- [Inspection recipe](references/inspection.md)
- [Official sources and version guidance](references/sources.md)
- [Coinbase AgentKit](https://github.com/coinbase/agentkit)
- [Coinbase CDP SDK](https://github.com/coinbase/cdp-sdk)
- [Coinbase Agentic Wallet CLI documentation](https://docs.cdp.coinbase.com/agentic-wallet/cli/quickstart)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance]

**Output Format:** [Scoped readiness report with optional reviewable configuration correction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed network and account, tested reads, action classifications, and unresolved gaps without disclosing credentials.]

## Skill Version(s):

0.4.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
