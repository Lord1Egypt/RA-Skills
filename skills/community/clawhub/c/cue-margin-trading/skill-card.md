## Description:

用 Cue 跑融资融券场景的深度研究，横向比对主要券商的两融政策，识别竞对抢客与风险收缩信号，并支持券商经纪业务的客户持仓沟通与展业。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, brokerage teams, and developers use this skill to run Cue-powered public-data research on margin trading policies, broker comparisons, ETF and technology margin terms, and risk-contraction signals. It helps produce sourced reports for customer communication and competitive monitoring, but it does not replace due diligence, legal review, or underwriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download or update the Cue runner and execute mutable external code locally.

Mitigation: Review or pin the runner version before use and install only when local execution of the Cue runner is acceptable.

Risk: The runner can access a local Cue API key and spend credits.

Mitigation: Confirm the credit-spending prompt carefully before running research and use an appropriately scoped Cue account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-margin-trading)
- [Cue playbook source](https://cuecue.cn/playbook)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key page](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown research report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Cue API key and credits; may fetch or update the external Cue runner before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
