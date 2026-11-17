## Description:

用 Cue 运行信贷尽调深度研究，针对企业工商、股权、财务与经营基本面交叉公开数据并产出带来源的预尽调报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Financial services, risk, and diligence users can run Cue workflows for company credit diligence, public-disclosure review, financial diligence, preliminary borrower screening, and source-linked research reports. The skill is intended to support review workflows and does not replace legal, underwriting, or formal due-diligence judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can clone, update, and run an external Cue runner from the user's home directory.

Mitigation: Review the upstream runner source, pin or mirror a vetted version where possible, and run it in a restricted environment before using it with sensitive work.

Risk: The workflow uses a Cue account and consumes credits after user confirmation.

Mitigation: Confirm the selected buddy, subject, and credit use before execution, and use an account approved for the intended workflow.

Risk: The available Cue workflows include high-net-worth prospect mining beyond credit diligence.

Mitigation: Avoid the prospect-mining workflow unless it fits applicable compliance, privacy, and business-use obligations.

Risk: The generated reports rely on public data and do not replace formal diligence, legal review, or underwriting judgment.

Mitigation: Have qualified reviewers verify source-linked findings before using outputs in credit, legal, or risk decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-credit-diligence)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key](https://cuecue.cn/hub/api-key)
- [Cue skills runner source](https://github.com/sensedeal/cue-skills)
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run a Cue research runner, consume credits after confirmation, and return empty results without fabricating content.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
