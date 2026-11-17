## Description:

Use this skill when the user asks to manage Binance assets, check account security, scan for arbitrage opportunities, or perform automated dust sweeps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyy2099](https://clawhub.ai/user/hyy2099)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Binance account security, scan idle balances and dust assets, monitor funding-rate arbitrage opportunities, execute dust conversion, and generate account activity reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for live Binance API credentials.

Mitigation: Use a dedicated Binance sub-account with small balances, no withdrawal permission, IP allowlisting, and testnet or read-only credentials before considering live use.

Risk: The `/aegisclaw dust` command can perform immediate asset conversion.

Mitigation: Treat dust conversion as a real trading action and review target assets, account permissions, and expected value before running it.

Risk: The release security verdict is suspicious because the skill can automate financial account actions while overstating safety.

Mitigation: Review the code and configuration carefully before installing, keep funds limited, and monitor account activity after use.

Risk: Remote installer commands can execute code from the network.

Mitigation: Avoid remote `curl | sh` installation paths unless independently verified; prefer inspecting the artifact and installing dependencies locally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyy2099/skills/aegisclaw)
- [Publisher profile](https://clawhub.ai/user/hyy2099)
- [Repository homepage from release metadata](https://github.com/hyy2099/aegisclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown reports with CLI or OpenClaw command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Binance account status, balance summaries, arbitrage opportunity summaries, dust conversion status, and weekly report text.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
