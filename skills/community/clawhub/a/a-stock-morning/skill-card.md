## Description:

Sends a daily 9:45 AM A-share market open summary with index performance, fund-flow context, top sectors, volume, and trading suggestions via Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrislzg](https://clawhub.ai/user/chrislzg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-monitoring users use this skill to generate or schedule a morning A-share market report and optionally send it to Feishu. It is intended for recurring market awareness, not as independently verified financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separate local Tavily search skill at a hardcoded path and runs it through a shell command.

Mitigation: Review and trust the external Tavily script before installation, or replace the dependency with a reviewed local search integration.

Risk: A scheduled run can repeatedly send generated market summaries to Feishu.

Mitigation: Confirm the Feishu target, webhook configuration, and cron schedule before enabling automatic sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrislzg/skills/a-stock-morning)
- [Tencent stock API endpoint](https://qt.gtimg.cn/q=sh000001)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands]

**Output Format:** [Markdown report with optional Feishu message delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can be run as a scheduled weekday task; --send posts through Feishu/OpenClaw when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
