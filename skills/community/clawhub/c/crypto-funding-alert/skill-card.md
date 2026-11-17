## Description:

Real-time crypto funding rate scanner with smart alerts. Finds negative funding rates for profitable long positions. Supports Binance futures. No API key needed for scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

Developers and crypto market analysts use this skill to scan Binance futures funding rates, classify negative-funding opportunities, and generate command-line alerts and local scan history for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents informational crypto market scans, but its financial safety claims are stronger than what the code enforces.

Mitigation: Treat outputs as market scanner signals only, review the code and recommendations before acting, and avoid relying on the skill as automated trading advice.

Risk: Unsafe leverage or stop-loss values can be passed through command-line options.

Mitigation: Use conservative parameters, validate configuration before running, and avoid increasing leverage or weakening stop-loss thresholds without independent review.

Risk: The skill saves scan history locally by default and webhook examples can forward scan output to external services.

Mitigation: Review the local output path and enable Telegram, Discord, or other webhook integrations only when sending this data to those services is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/crypto-funding-alert)
- [Publisher profile](https://clawhub.ai/user/dagangtj)
- [Binance Futures premium index endpoint](https://fapi.binance.com/fapi/v1/premiumIndex?symbol=${coin}USDT)
- [Binance Futures 24hr ticker endpoint](https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=${coin}USDT)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with JSONL scan-history records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and internet access; writes scan history locally by default.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
