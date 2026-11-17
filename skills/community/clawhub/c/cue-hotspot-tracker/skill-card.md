## Description:

用 Cue 通常 5-10 分钟（最长约 15 分钟）实时扫描今日 A 股热点板块与近 24h 催化资讯，拆解盘中催化逻辑与受益方向；跑完自动生成「看板图」与「报告长图」，报告全文以 Cue 链接交付。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

面向关注中国 A 股盘中行情的交易者与市场研究人员，用于追踪热点板块、梳理催化逻辑和受益方向，并查看生成的报告与图表。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious and cites a request to share an API key in chat.

Mitigation: Do not send a live API key in chat; have the user configure it through a secure local mechanism.

Risk: The security guidance flags recurring scheduling instructions and asks users to understand what jobs may be created.

Mitigation: Review any proposed schedule before enabling it and confirm how to disable the recurring job.

Risk: The security analysis is partial because a referenced local path was missing, leaving some setup behavior unexamined.

Mitigation: Review the complete setup behavior before installation, including any remote-fetch step noted in the security guidance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/panting09266-ai/skills/cue-hotspot-tracker)
- [SOP schema](references/sop-schema.md)
- [Cue platform](https://cuecue.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Images, Links]

**Output Format:** [Markdown report, dashboard image, long-form report image, and Cue report link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [盘中 A 股热点与催化分析；不构成投资建议。]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
