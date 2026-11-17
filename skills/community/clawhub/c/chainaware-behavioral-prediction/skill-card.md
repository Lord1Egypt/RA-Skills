## Description:

Connects agents to ChainAware's remote MCP service for wallet fraud screening, behavioral profiling, rug-pull prediction, crypto credit scoring, token holder ranking, token auditing, and AI-agent trust scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chainaware](https://clawhub.ai/user/chainaware)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to integrate ChainAware's MCP endpoint into agent workflows that assess blockchain wallets, contracts, tokens, launch activity, and AI-agent wallet trust. It supports risk triage, DeFi personalization, compliance screening, token community analysis, and integration setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends wallet addresses, contract or LP addresses, network identifiers, and the ChainAware credential to ChainAware's remote scoring service.

Mitigation: Install only where that data sharing is acceptable, and perform any required data protection review for wallets linked to identified users.

Risk: Some web integrations place the API key in the MCP URL, where it may be visible in browser or network tooling.

Mitigation: Prefer integrations that pass the key in a header; for URL-based setups use restricted-scope or low-limit keys and rotate them if exposed.

Risk: x402 pay-per-call behavior can create payment or quota exposure if used without limits.

Mitigation: Set payment, quota, or rate limits before relying on x402-based access.

Risk: Fraud, credit, and compliance-oriented outputs may influence high-impact onboarding, lending, or blocking decisions.

Mitigation: Use the scores as decision-support signals, surface the cited wallet or contract evidence, and require human review for consequential actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chainaware/skills/chainaware-behavioral-prediction)
- [ChainAware profile](https://clawhub.ai/user/chainaware)
- [ChainAware Behavioral Prediction MCP repository](https://github.com/ChainAware/behavioral-prediction-mcp)
- [ChainAware MCP endpoint](https://prediction.mcp.chainaware.ai/sse)
- [ChainAware website](https://chainaware.ai)
- [Pricing and API key access](https://chainaware.ai/pricing)
- [Fraud detection backtesting](https://chainaware.ai/scam-db)
- [Rug pull detection backtesting](https://chainaware.ai/resources/rugpull-verification)
- [ChainAware privacy policy](https://chainaware.ai/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional JSON, code blocks, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet or contract risk scores, behavioral profiles, batch job IDs, network support notes, and integration snippets.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
