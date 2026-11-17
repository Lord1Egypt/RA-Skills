## Description:

Produces concise Bitcoin market briefs with live price, derivatives, liquidation, and notable-signal data for on-demand or morning updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

Bitcoin-focused users and agents use this skill to review a current market snapshot on demand or in a morning update. It summarizes market observations and is not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags broad activation guidance, which may cause the skill to run on loosely related requests.

Mitigation: Activate it only for explicit Bitcoin market questions or requested morning briefs; clarify ambiguous requests.

Risk: Paid data calls can spend up to $0.25 per task without asking.

Mitigation: Use the free preview first, verify the quoted recipient, Base network, and USDC asset before payment, and ask for approval above $0.25.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/shakeelamjid/agentreeve-skills/tree/main/btc-market-brief)
- [BTC Market Brief on ClawHub](https://clawhub.ai/shakeelamjid/skills/btc-market-brief)
- [AgentReeve Bitcoin preview API](https://agentreeve.com/api/v1/btc/preview)
- [AgentReeve Bitcoin brief API](https://agentreeve.com/api/v1/btc/brief)
- [AgentReeve Bitcoin signals API](https://agentreeve.com/api/v1/btc/signals?days=30)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Four to six line market brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the data timestamp; market observations are not financial advice.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
