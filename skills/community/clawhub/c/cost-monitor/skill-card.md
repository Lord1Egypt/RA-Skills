## Description:

Real-time token usage and cost tracking for OpenClaw agents, supporting MiMo Token Plan credits and DeepSeek pay-as-you-go RMB balances with per-turn consumption and remaining balance summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengkezhou](https://clawhub.ai/user/chengkezhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor per-turn token usage, estimate model costs, and keep local balance records visible during agent conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled balance-setting helper is flagged as unsafe in the server security guidance.

Mitigation: Avoid using set-balance until its argument handling is fixed; edit or back up balance.json before changing tracked balances.

Risk: DeepSeek calibration can read a local OpenClaw DeepSeek credential and contact the DeepSeek balance API.

Mitigation: Run DeepSeek calibration only after confirming that local credential access and the outbound provider API request are acceptable.

Risk: The skill updates local balance tracking data during cost calculations.

Mitigation: Back up balance.json if its values are important, and review the displayed balance after calibration or model changes.

## Reference(s):

- [ClawHub Cost Monitor skill page](https://clawhub.ai/chengkezhou/skills/cost-monitor)
- [Publisher profile](https://clawhub.ai/user/chengkezhou)
- [Cost Monitor detailed guide](references/detailed-guide.md)
- [MiMo pricing documentation](https://platform.xiaomimimo.com/docs/zh-CN/price/)
- [DeepSeek balance API](https://api.deepseek.com/user/balance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Concise text status line with markdown documentation and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates local balance configuration and may read local OpenClaw transcript and provider credential files during calibration.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
