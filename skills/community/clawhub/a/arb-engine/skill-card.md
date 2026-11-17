## Description:

加密套利引擎 helps agents analyze cryptocurrency arbitrage workflows, including triangular arbitrage, dynamic slippage compensation, structured outputs, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, trading analysts, and automation teams use this skill to structure cryptocurrency arbitrage analysis, trading-workflow guidance, API-key setup notes, and troubleshooting outputs. It should be reviewed carefully before connecting to live trading systems or real funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto-market automation can affect real funds if connected to live exchange accounts.

Mitigation: Prefer simulation or dry-run workflows first and require explicit human confirmation before live trading.

Risk: Exchange API keys or other credentials could enable unintended account access.

Mitigation: Use read-only or low-permission API keys, keep credentials outside prompts and files, and rotate keys regularly.

Risk: The skill discloses command execution and package installation for `arb-engine`.

Mitigation: Review commands before execution and verify any installed `arb-engine` package separately before use.

Risk: The release is broad and under-scoped for automated trading decisions.

Mitigation: Constrain the skill to analysis and operator-reviewed recommendations unless a separate trading-control review approves execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/arb-engine)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON result examples, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require API keys, external crypto-market data, and explicit confirmation before live trading or command execution.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
