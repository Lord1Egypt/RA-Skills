## Description:

一键部署Freqtrade量化交易机器人。支持现货交易策略，自动安装依赖、配置策略、设置WebUI监控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[namogu](https://clawhub.ai/user/namogu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to deploy and configure a Freqtrade cryptocurrency trading bot with exchange API credentials, strategy selection, and WebUI monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe installation steps may execute remote or mutable code during deployment.

Mitigation: Use a pinned, inspectable Freqtrade release in an isolated environment and review installation commands before execution.

Risk: The trading bot can expose real funds if started with live exchange credentials and aggressive balance settings.

Mitigation: Keep dry_run enabled until testing is complete, restrict exchange API keys to trading-only with withdrawals disabled, and avoid allocating most account balance to the bot.

Risk: The WebUI/API can expose trading controls if bound beyond localhost or left with placeholder secrets.

Mitigation: Bind the WebUI/API to localhost unless explicitly secured, replace all placeholder secrets, and restrict network access to trusted operators.

## Reference(s):

- [Freqtrade documentation](https://www.freqtrade.io)
- [Freqtrade Chinese documentation](https://www.itrade.icu/zh/freqtrade/freqtrade)
- [Freqtrade strategy customization](https://www.freqtrade.io/en/stable/strategy-customization/)
- [Usage guide](references/usage.md)
- [ClawHub skill page](https://clawhub.ai/namogu/skills/freqtrade-deploy)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Freqtrade install, API credential configuration, startup, WebUI, and operations guidance.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
