## Description:

用 Cue 跑「财富投顾」场景的深度研究：自动汇总隔夜政策与外盘动态，生成即插即用的客户早报与配置建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Investment advisers, wealth managers, and financial-content teams use this skill to run Cue deep research for market recaps, morning briefs, client-ready commentary, allocation discussion points, tax-compliance guidance, and bond-risk monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can clone or update mutable remote runner code under ~/.cue before execution.

Mitigation: Review the Cue/sensedeal runner repository before first use and pin or audit the runner version in controlled environments.

Risk: The runner can access a local Cue API key and consume account credits.

Mitigation: Use a least-privilege Cue account where possible, confirm credit-consuming runs before execution, and never paste or expose ~/.cue/config.json.

Risk: The generated financial research may be incomplete, stale, or unsuitable as professional advice.

Mitigation: Preserve source links, review outputs before sharing with clients, and treat reports as research support rather than a substitute for due diligence, legal review, or suitability assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-wealth-advisory)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key page](https://cuecue.cn/hub/api-key)
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills)
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Analysis]

**Output Format:** [Markdown guidance with inline shell commands and sourced research reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve source links and avoid fabricated findings when Cue returns no content.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
