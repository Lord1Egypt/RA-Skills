## Description:

用 Cue 运行全球宏观深度研究，基于公开官方数据追踪并比较主要经济体的通胀、GDP、就业、贸易、央行利率和汇率表现。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, investors, and operators use this skill to run Cue macroeconomic research for cross-country comparison, market monitoring, cross-border allocation, site selection, and macro judgment. It supports sourced research workflows and should not replace due diligence, legal review, underwriting, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to clone or update unpinned external code under ~/.cue and run it locally.

Mitigation: Review or pin the cue-skills repository before execution and run it in an environment where local code execution is acceptable.

Risk: The runner can use a Cue API key from ~/.cue/config.json and consume credits.

Mitigation: Use only an intended Cue account, confirm credit use before running research, and avoid shared environments with unintended credentials.

Risk: The generated report is based on public macroeconomic data and may be incomplete or unsuitable for regulated decisions.

Mitigation: Preserve source links and treat the output as research support rather than due diligence, legal, underwriting, or investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangxiaoxu/skills/cue-global-macro)
- [Cue Playbook API](https://cuecue.cn/api/playbook)
- [Cue Skills Runner Source](https://github.com/sensedeal/cue-skills)
- [Cue API Key Page](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream for several minutes; final reports should preserve source links.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
