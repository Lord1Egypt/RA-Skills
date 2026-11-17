## Description:

Crypto DRT Scalping provides Dealing Range Theory guidance for 12 crypto pairs, with historical backtest claims, play-money risk rules, and optional paid live signal calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review a crypto scalping plan, follow risk-management guidance, and optionally run scripts that fetch paid live DRT signals. The skill is for trading workflow support and should not be treated as financial advice or a guarantee of results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running scripts/signals.py makes a paid external request using X402_API_KEY.

Mitigation: Run the script only after confirming the charge model, use a limited and revocable API key, and avoid unattended execution.

Risk: The live signal client can be redirected through X402_BASE or allowed to use HTTP with X402_ALLOW_HTTP.

Mitigation: Keep the default HTTPS endpoint unless you control and trust the replacement endpoint, and do not enable HTTP transport for spending-capable keys.

Risk: Trading outputs and backtest claims may be misleading if treated as guaranteed results.

Mitigation: Treat the content as workflow guidance, review signals independently, and follow the documented play-money and drawdown controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/crypto-drt-scalping)
- [Default live signals endpoint](https://186.240.156.169:8791)
- [x402 API key purchase information](https://github.com/MohamedAbdisamed/x402-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples; optional JSON returned by the live signals script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid live signal calls require X402_API_KEY, Python 3, and network access to the configured x402 endpoint.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
