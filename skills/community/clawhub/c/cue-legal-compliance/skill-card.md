## Description:

用 Cue 跑「法律合规」场景的深度研究：快速检索国内法律法规与行政令原文，梳理立法背景与合规要点，覆盖企业合规风险体检、监管问询答复案例库、疑难法律实操案例库、国内法规调研、法律实务问题研判、监管处罚雷达、诉讼文书起草等核心搭子，产出带法条与类案依据、可逐条回查的合规体检与法律实务底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Legal and compliance practitioners, analysts, and developers use this skill to run Cue research for China-focused legal compliance checks, regulatory inquiry examples, legal practice questions, enforcement monitoring, and draft litigation documents with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Legal or compliance queries may be sent to Cue's service through an external runner.

Mitigation: Avoid submitting confidential legal or business materials unless the user has approved that third-party data flow.

Risk: The skill may clone or update Cue's external runner and consume Cue credits.

Mitigation: Confirm execution and credit use with the user before running the research command.

Risk: Generated legal research can be incomplete or unsuitable as legal advice.

Mitigation: Preserve source links and have qualified reviewers verify conclusions before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-legal-compliance)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills)
- [Cue API key page](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with source links and inline shell commands when setup or execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May consume Cue credits after user confirmation; preserves source links and reports empty results without fabrication.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
