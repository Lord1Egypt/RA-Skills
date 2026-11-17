## Description:

用 Cue 跑「出海企业线索」场景的深度研究：锁定指定区域内有 ODI 备案、实际出海动作的跨境企业，按开户、结算、发债、并购等需求精准匹配商机，并产出可回查、可派单的出海商机清单与合规底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking business development, compliance, and research users use this skill to run Cue deep research for overseas expansion leads, corporate due diligence, regulatory review, and cross-border compliance screening. It helps agents select a live Cue research template, confirm credit use, run the Cue runner, and return sourced research without fabricating missing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Cue and an external cue-skills runner repository.

Mitigation: Install only when the user is comfortable using Cue and trusting the external runner repository.

Risk: Research subjects are sent to Cue and deep research may spend credits after confirmation.

Mitigation: Confirm the selected Cue template, research subject, and credit use with the user before running the research command.

Risk: The skill is written for Chinese-speaking users and does not provide an English flow.

Mitigation: Use it for Chinese-language workflows or provide separate language support before deploying it to English-only users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-overseas-expansion)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [Cue API key page](https://cuecue.cn/hub/api-key)
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills)
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills)
- [Cue homepage](https://cuecue.cn/)
- [Cue credits payment page](https://cuecue.cn/pay)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and sourced research report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include source links from Cue reports; the skill instructs agents to preserve sources and report empty results without fabrication.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
