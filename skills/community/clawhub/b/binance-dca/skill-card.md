## Description:

Professional Binance Dollar-Cost Averaging (DCA) tool for automated and manual recurring crypto purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fpsjago](https://clawhub.ai/user/fpsjago)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to plan DCA strategies, check Binance spot prices and balances, place market or limit buy orders, review trade history, and configure recurring purchases through shell commands or OpenClaw cron workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Binance spot orders can spend real funds if production API keys are configured.

Mitigation: Use Binance testnet first, start with small amounts, and require explicit approval and spending limits before unattended cron purchases.

Risk: Binance API keys can authorize unwanted trading if over-permissioned or stored insecurely.

Mitigation: Use a dedicated API key without withdrawal permissions, restrict it to the narrowest spot permissions possible, enable IP allowlisting where available, and avoid storing secrets in shell startup files.

Risk: The authoritative security summary identifies unsafe code execution and credential-persistence risks, including untrusted values in the plan command.

Mitigation: Review the shell script before installation, do not pass untrusted values into plan, and install only if local script access to Binance trading keys is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fpsjago/skills/binance-dca)
- [Binance](https://www.binance.com)
- [Binance Spot Testnet](https://testnet.binance.vision)
- [Binance Support Announcements](https://www.binance.com/en/support/announcement)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Binance API endpoints through a local shell script when the user executes or authorizes commands.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact changelog, released 2026-02-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
