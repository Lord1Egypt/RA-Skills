## Description:

TypeScript (Node.js 20+) AI news-driven BNB strategy trading bot for BSC, used for event/news sentiment signals, strict risk controls, and automated WBNB<->stablecoin swaps with dry-run safety, panic mode, status, and approval revoke tooling.

This skill is for research and development only.

## Publisher:

[happyrstudent](https://clawhub.ai/user/happyrstudent)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to run or evaluate a news-driven BSC trading bot that turns REST or WebSocket news signals into WBNB and stablecoin swap decisions. It is most appropriate for controlled review, dry-run testing, and research-style assessment before any live wallet use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can sign high-impact blockchain transactions with weak validation.

Mitigation: Keep DRY_RUN=true until the transaction-building path is audited, validate token and DEX addresses, and use a dedicated low-balance wallet.

Risk: External API origins and swap responses can influence transaction construction.

Mitigation: Pin and validate ONEINCH_API_BASE and other external API origins, and rotate any API key used with an untrusted endpoint.

Risk: The panic command may not stop an already-running bot or already-submitted transaction.

Mitigation: Treat panic as a state flag rather than a guaranteed emergency stop, monitor running processes, and revoke approvals where appropriate.

## Reference(s):

- [AI News BNB Trader ClawHub page](https://clawhub.ai/happyrstudent/skills/ai-news-bnb-trader)
- [1inch BSC swap API endpoint](https://api.1inch.dev/swap/v6.0/56)
- [OpenAI chat completions API endpoint](https://api.openai.com/v1/chat/completions)
- [BSC public RPC endpoint](https://bsc-dataseed.binance.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown command guidance, TypeScript code, environment configuration, JSON status output, and runtime logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live mode can submit signed BSC transactions; dry run is the default and should remain enabled until the transaction path is audited.]

## Skill Version(s):

0.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
