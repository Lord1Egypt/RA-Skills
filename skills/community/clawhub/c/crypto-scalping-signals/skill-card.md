## Description:

Provides real-time crypto futures scalping signals using multiple strategy filters with risk management, market structure, order flow, and session timing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avidjunior](https://clawhub.ai/user/avidjunior)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-focused agent users use this skill to have an agent analyze crypto futures scalping setups, calculate risk constraints, and provide non-executing signal guidance for pairs and trading sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading strategy win-rate claims and signal references may be unaudited or unreliable.

Mitigation: Treat outputs as decision support, validate signals independently, and paper trade before using real funds.

Risk: Pairing the skill with external exchange tooling could expose credentials or enable trades beyond the skill's stated analysis-only behavior.

Mitigation: Avoid giving exchange credentials unless separate trusted tooling is reviewed, constrained, and intentionally configured.

Risk: Leverage, fees, slippage, and rapid market movement can turn scalping guidance into financial loss.

Mitigation: Use conservative leverage, position sizing, daily loss limits, and fee/slippage checks before acting on any signal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avidjunior/skills/crypto-scalping-signals)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text trading-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analysis and signals only; no bundled code, persistence, credential use, or automatic trade execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
