## Description:

用 Cue 跑「私募尽调」场景的深度研究：一次拉齐私募管理人的协会登记、管理规模、核心团队、产品运作、股权结构与处罚涉诉，产出带疑点清单、可上会尽调的私募底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and investment diligence teams use this skill to run Cue private-fund due diligence research over public sources for managers, products, ownership links, filings, and risk signals. The resulting report supports review workflows but does not replace legal, underwriting, or formal due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update mutable third-party runner code before execution.

Mitigation: Review the cue-skills repository before running, prefer a trusted packaged runner or pinned commit, and run it in a least-privilege environment.

Risk: The skill may use a local Cue API key and spend credits after confirmation.

Mitigation: Require explicit user confirmation before each paid research run and monitor Cue account usage.

Risk: The research uses public data and can miss private, stale, or legally material information.

Mitigation: Treat the generated report as decision support and require formal legal, underwriting, or diligence review before relying on conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-private-fund-dd)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills)
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills)
- [Cue API key page](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May consume Cue credits after user confirmation and may return an empty result if the live research run produces no content.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
