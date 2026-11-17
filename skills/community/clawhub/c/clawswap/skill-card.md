## Description:

Run and iterate a self-hosted ClawSwap AI trading agent with Python. Use when the user wants to start runtime trading (paper/live gateway runtime protocol), backtest strategies locally, download market data, or test strategy behavior before deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawperp](https://clawhub.ai/user/clawperp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to run ClawSwap paper or runtime trading agents, test strategies locally, download market data, and compare strategy behavior before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends bearer credentials to a configurable gateway.

Mitigation: Use the default gateway unless the destination is fully trusted, and review gateway settings before running the runtime client.

Risk: The skill stores API and runtime credentials in local plaintext files.

Mitigation: Keep .env, .runtime_token, and .clawswap_api_key out of version control and restrict local file permissions.

Risk: Custom strategy Python runs with full local privileges.

Mitigation: Avoid untrusted strategy files and review strategy code before backtesting or runtime use.

Risk: Trading behavior can produce unintended orders or losses.

Mitigation: Use paper mode first and review strategy behavior before live deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawperp/skills/clawswap)
- [ClawSwap homepage](https://clawswap.trade)
- [ClawSwap settings](https://clawswap.trade/settings)
- [ClawSwap support Discord](https://discord.gg/clawswap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code references, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for running local Python scripts, configuring credentials, selecting strategies, backtesting, and operating the runtime client.]

## Skill Version(s):

0.2.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
