## Description:

用 Cue 跑贷后监测场景的深度研究，监测授信客户的被执行、诉讼、评级下调、经营异动、股权质押和资产处置等公开风险信号，并生成带来源链接的贷后风险预警底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Credit risk, lending operations, and financial due-diligence teams use this skill to run Cue-backed post-loan monitoring on borrowers or counterparties. It helps produce sourced warning reports for enterprise events, judicial execution, litigation, rating changes, pledged equity, operating anomalies, and asset-disposal leads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to fetch and run mutable external runner code before executing the research workflow.

Mitigation: Review or pin the runner repository before execution, and install only if cuecue.cn and the sensedeal/cue-skills repository are trusted.

Risk: The Cue workflow uses the user's query and local Cue API key and may consume account credits.

Mitigation: Confirm the subject, selected workflow, data-sharing acceptability, and credit use with the user before running the research command.

Risk: The generated monitoring report is based on public-data research and may be incomplete or unsuitable as a sole basis for lending decisions.

Mitigation: Use the report as an evidence-linked screening artifact and route material findings through normal due-diligence, legal, and credit review processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-post-loan-monitoring)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key page](https://cuecue.cn/hub/api-key)
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills)
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with source links plus setup and execution commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs can take several minutes, consume Cue credits, and may return an empty result that should be reported without fabrication.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
