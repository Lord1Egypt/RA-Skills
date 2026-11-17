## Description:

Find markets where Simmer's AI consensus diverges from the real market price, then trade on the mispriced side using calibration-shrunk Kelly sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boeingchoco](https://clawhub.ai/user/boeingchoco)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan prediction markets for AI-versus-market price divergence, apply configurable trading safeguards, and optionally execute Polymarket trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute real-money prediction-market trades when live trading is enabled.

Mitigation: Start in paper or managed-wallet mode, keep daily and per-trade limits low, and review proposed actions before enabling live execution.

Risk: External-wallet use may expose a wallet private key to the agent runtime.

Mitigation: Prefer managed wallets when possible, avoid sharing high-value wallet keys, and restrict funds and API scopes used with the skill.

Risk: Changing the Simmer API endpoint can route account or trading activity to an untrusted service.

Mitigation: Leave SIMMER_API_URL at the trusted default unless the replacement endpoint is explicitly verified.

Risk: The default scan path may still touch account state until auto-redemption behavior is explicitly gated.

Mitigation: Treat scan runs as requiring review, use isolated credentials, and verify behavior in a low-risk environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boeingchoco/skills/boeingchoco-polymarket-ai-divergence)
- [Publisher profile](https://clawhub.ai/user/boeingchoco)
- [Simmer API](https://api.simmer.markets)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, configuration values, and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce trading scan summaries, skip-reason counts, and live execution status when configured to trade.]

## Skill Version(s):

2.6.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
