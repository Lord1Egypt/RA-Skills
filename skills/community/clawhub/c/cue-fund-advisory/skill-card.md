## Description:

用 Cue 跑「基金投顾」场景的深度研究：穿透公募基金底仓，深度透视基金经理真实管理能力与风格漂移，量化评估选股与择时能力，覆盖大类资产配置月报、公募基金全维尽调、固收+与纯债基金排雷优选、基金业绩归因与能力评估、基金组合穿透与重复配置排雷等核心搭子，产出基金遴选与投后跟踪可用的归因评估与配置建议底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run Cue-based fund advisory research, including fund due diligence, manager ability analysis, asset allocation reports, fixed-income fund screening, attribution, and portfolio look-through checks. The skill returns source-linked research drafts that support fund selection and post-investment monitoring, but they do not replace formal due diligence, legal review, or underwriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to fetch and run changing external Cue runner code that automatically uses a local Cue API key.

Mitigation: Install only if the Cue runner repository is trusted; review or pin the runner before first use.

Risk: Deep research runs consume Cue credits.

Mitigation: Confirm the selected research buddy, subject, and credit cost with the user before execution.

Risk: Fund research outputs may be incomplete or unsuitable as the sole basis for investment decisions.

Mitigation: Preserve source links and review outputs against formal due diligence, legal review, and underwriting requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-fund-advisory)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Cue API key, Cue credits, and a trusted local Cue runner.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
