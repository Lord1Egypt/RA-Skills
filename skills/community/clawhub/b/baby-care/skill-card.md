## Description:

育儿助手为 0-6 岁儿童照护场景提供中文育儿指导，覆盖喂养、睡眠、健康、安全、早期教育、疫苗时间表和发育里程碑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjlew](https://clawhub.ai/user/jjlew)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use this skill in Chinese to ask age-specific questions about feeding, sleep, common symptoms, home safety, early education, vaccines, and developmental milestones. It can also calculate follow-up vaccine timing and prepare local calendar and reminder actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically create vaccine calendar entries and persistent reminders containing child health details.

Mitigation: Require explicit user confirmation before creating any calendar event or reminder, and show the exact title, date, notes, and reminder text before execution.

Risk: Vaccine names, doses, or dates may be incomplete or ambiguous.

Mitigation: Validate vaccine fields against the referenced schedule and ask the user to confirm uncertain or uncommon vaccine timing with a vaccination clinic.

Risk: Health guidance may be mistaken for professional medical advice.

Mitigation: Keep responses informational, preserve the medical disclaimer, and direct urgent symptoms or uncertain cases to qualified medical care.

## Reference(s):

- [宝宝常见疾病护理](references/common_illnesses.md)
- [辅食食谱参考](references/feeding_recipes.md)
- [0-6岁发育里程碑](references/growth_milestones.md)
- [0-6岁疫苗接种时间表](references/vaccine_schedule.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown or plain text, with shell commands when preparing calendar and reminder actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health-related guidance should remain informational and should not replace professional medical advice.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
