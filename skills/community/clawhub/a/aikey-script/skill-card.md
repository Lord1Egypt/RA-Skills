## Description:

协作式口播稿写作技能，帮助知识型创作者选择脚本类型、组装内容单元并逐段共创。

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

知识型创作者使用此技能协作撰写面向镜头的短视频口播稿：确定稿件形式，从创作者提供的素材中组织内容，并逐段完善草稿。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes automatically saving user feedback into shared writing rules, which could add unwanted or inaccurate guidance.

Mitigation: Review proposed rule changes before saving, limit write access to the intended writing vault, and keep backups of shared rules.

Risk: Personal details from recorded conversations or personal stories could be exposed when shared with AI.

Mitigation: Get participants’ consent before recording conversations and remove sensitive details before sharing stories with AI.

Risk: The security guidance identifies companion framework files and Python helpers as missing and unverified.

Mitigation: Inspect the companion files and helpers before use, and restrict access to the intended writing vault.

## Reference(s):

- [协作推进](references/协作推进.md)
- [概念型口播](references/概念型口播.md)
- [规则卡](references/规则卡.md)
- [ClawHub release page](https://clawhub.ai/iamzifei/skills/aikey-script)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [中文口播稿草稿及结构化写作说明（Markdown）]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [逐段协作形成；内容以创作者提供的真实素材为依据。]

## Skill Version(s):

0.4.9 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
