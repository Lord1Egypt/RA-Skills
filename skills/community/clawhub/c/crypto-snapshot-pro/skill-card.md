## Description:

Crypto Snapshot Pro provides AI-powered crypto trading signals with LONG/SHORT/HOLD recommendations, entry levels, target prices, stop-loss levels, and market commentary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matros777](https://clawhub.ai/user/matros777)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request paid crypto market snapshots for a specified symbol and receive trading-signal guidance with entry, target, stop-loss, conviction, and commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party paid crypto-signal endpoint whose LONG/SHORT/HOLD outputs may be incorrect or unsuitable for a trade.

Mitigation: Treat outputs as informational rather than financial advice, and independently verify any trade before risking funds.

Risk: The skill requires USDC payment on the Base network before returning a signal.

Mitigation: Confirm the amount, network, and payment recipient before authorizing a request.

## Reference(s):

- [Crypto Snapshot Pro on ClawHub](https://clawhub.ai/matros777/skills/crypto-snapshot-pro)
- [Crypto Snapshot Pro endpoint](https://crypto-snapshot-pro.onrender.com/)
- [Crypto Snapshot Pro OpenClaw manifest](https://crypto-snapshot-pro-manifest.onrender.com/.well-known/openclaw.json)
- [OpenX402 project](https://openx402.ai/projects/0x5b7efd37546d6bb02463339ceaddd80997ac97b3)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON response containing a textual trading analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a paid USDC request on the Base network before receiving the signal.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
