## Description:

提供中医体质辨识服务，问题简洁专业，针对体型、体力、皮肤面色、寒热出汗、情绪睡眠、胃肠道状况等提问，进行体质辨识并给出适合的食物推荐；当用户需要进行体质辨识、体质调理方案或健康状况评估时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jettli85](https://clawhub.ai/user/jettli85)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language skill to complete a structured TCM constitution questionnaire, receive a concise pattern summary, and get 3-5 food recommendations from the included food list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects health-related questionnaire responses without explicit consent, privacy expectations, or opt-out language.

Mitigation: Add clear consent, privacy, and skip or stop language before the questionnaire begins.

Risk: The skill provides TCM-style medicinal-food recommendations without safety boundaries.

Mitigation: Add a medical disclaimer and red-flag guidance directing users, special populations, and users with concerning symptoms to qualified healthcare professionals.

## Reference(s):

- [Food List Reference](artifact/references/food-list.md)
- [ClawHub Skill Page](https://clawhub.ai/jettli85/skills/constitution-inquiry)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese-language prompts, questionnaire summaries, constitution analysis, and food recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive 9-question flow with conditional follow-up questions for insomnia and constipation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
