## Description:

A short, data-backed Bitcoin market brief on demand or each morning - price and 24h change across exchanges, funding and basis, liquidations, notable signals and what is unusual right now. Uses AgentReeve's live multi-exchange data; free preview, full brief per request over x402 (USDC on Base).

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request an on-demand or morning Bitcoin market summary to understand recent price moves, derivatives positioning, liquidations, and notable signals. The brief is observational market data, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls can spend up to $0.25 per task without an approval prompt.

Mitigation: Use the free preview when sufficient; verify the payment quote's recipient, Base network, and USDC asset before paying, and ask for approval above $0.25.

Risk: The skill may activate for unrelated quick-status requests.

Mitigation: Use it only for Bitcoin market requests, and run recurring briefs no more than once daily unless the user asks otherwise.

## Reference(s):

- [Source repository (btc-market-brief)](https://github.com/shakeelamjid/agentreeve-skills/tree/main/btc-market-brief)
- [AgentReeve free preview API](https://agentreeve.com/api/v1/preview)
- [AgentReeve Bitcoin brief API](https://agentreeve.com/api/v1/brief)
- [AgentReeve market signals API](https://agentreeve.com/api/v1/signals?days=30)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [A concise Markdown brief, typically 4-6 lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an as-of timestamp; observational market data, not financial advice.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
