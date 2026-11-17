## Description:

Envy is a non-custodial crypto perpetual futures trading agent that provides indicator data, signal scoring, backtesting, strategy assembly, portfolio optimization, live monitoring, position management, and paper or Hyperliquid trade routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manolovni](https://clawhub.ai/user/manolovni)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze crypto market indicators, build and backtest signal strategies, manage paper trading, and optionally route live perpetual futures trades through Hyperliquid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet secrets may be stored unencrypted in local files.

Mitigation: Treat wallet.json and config.json as sensitive secret files, restrict access to the skill workspace, and avoid exposing wallet export output in chat or logs.

Risk: The skill can automatically sign payments or place live trades with weak safeguards.

Mitigation: Use paper mode unless live-trading risk is deliberately accepted, review controller risk settings before use, and require explicit user confirmation before switching to Hyperliquid.

Risk: The Hyperliquid integration may pass a raw private key to another local skill process.

Mitigation: Review the installed Hyperliquid skill before live trading, isolate the wallet used for this workflow, and avoid funding it with more than the user can lose.

## Reference(s):

- [ClawHub Envy skill page](https://clawhub.ai/manolovni/skills/envy)
- [OpenClaw install documentation](https://docs.openclaw.ai/install)
- [Envy API discovery endpoint](https://arena.nvprotocol.com/api/claw/discover)
- [Envy API pricing endpoint](https://arena.nvprotocol.com/api/claw/pricing)
- [Hyperliquid application](https://app.hyperliquid.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON event lines, YAML configuration, and generated signal or strategy files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local wallet, signal, strategy, controller, state, and trade-log files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
