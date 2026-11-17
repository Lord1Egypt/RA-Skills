## Description:

用 Cue 跑「涉外法律」场景的深度研究：定向检索目标司法辖区的法律法规原文与核心条款，核查跨境主体的制裁与出口管制暴露（OFAC/欧盟/新加坡/BIS 等），多源公开数据交叉、结论带来源，为出海企业、跨境投资与合规团队提供可回查的涉外法律底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, developers, and compliance analysts use this skill to run Cue-powered cross-border legal research, including litigation database checks, cross-jurisdiction regulation review, sanctions and export-control exposure screening, and comparative legal analysis with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install or update and run mutable remote Cue runner code under ~/.cue/cue-skills.

Mitigation: Install only if you trust the Cue runner repository; review or pin the runner before enabling the skill.

Risk: The skill uses a local Cue API key and can consume credits during deep research runs.

Mitigation: Confirm the selected research subject, buddy, and credit-consuming run with the user before execution.

Risk: Legal research output may be incomplete or unsuitable as final legal, underwriting, or due-diligence advice.

Mitigation: Treat reports as sourced research workpapers and route material legal conclusions through qualified review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-cross-border-legal)
- [Cue runner repository](https://github.com/sensedeal/cue-skills)
- [Cue runner Gitee mirror](https://gitee.com/sensedeal/cue-skills)
- [Cue playbook API](https://cuecue.cn/api/playbook)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, text]

**Output Format:** [Markdown report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Cue API key and credit-consuming research run; final reports should preserve source links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
