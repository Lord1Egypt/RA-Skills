## Description:

用 Cue 跑“商机挖掘”场景的深度研究，扫描公开数据中的资金流动、资本动作和企业动态信号，产出带来源链接的商机清单、拜访简报和对公营销底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business development teams use this skill to run Cue research for corporate opportunity mining, including due diligence, industry-chain discovery, public-company events, deposit leads, customer monitoring, and visit briefs. The skill helps an agent select a live Cue template, confirm credit use, run the research, and return a sourced report without fabricating missing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to fetch and run mutable external Cue runner code that can read a local Cue API key and contact Cue services.

Mitigation: Review or pin the Cue runner repository before first use, especially in sensitive environments.

Risk: Running Cue deep research can consume user credits.

Mitigation: Require explicit user confirmation for the selected template, subject, and credit use before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-opportunity-mining)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills)
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Cue API key access and explicit user confirmation before consuming credits; reports empty results without fabricating content.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
