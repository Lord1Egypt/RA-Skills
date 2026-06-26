## Description: <br>
育儿助手技能。提供 0-6 岁宝宝的喂养、睡眠、健康、安全、早期教育等全方位育儿支持。当用户提到宝宝、婴儿、幼儿、育儿、喂养、断奶、睡眠、疫苗、体检、发育、辅食、早教等关键词时触发。当用户提到已接种某疫苗时，自动计算下一针时间并添加到日历和提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjlew](https://clawhub.ai/user/jjlew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, caregivers, and agents use this skill in Chinese to get practical guidance for feeding, sleep, common health questions, safety, early education, growth milestones, and vaccine schedules for children from birth through age 6. It can also help calculate a follow-up vaccine date and prepare local calendar and reminder actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The vaccine feature can change a calendar and create scheduled reminders, which may surprise users if handled without clear consent. <br>
Mitigation: Before writing anything, require the agent to show the next-dose calculation, calendar title, date, notes, and reminder time, then ask for explicit approval. <br>
Risk: Follow-up vaccine dates may be wrong when dose history, vaccine type, or local schedule details are uncertain. <br>
Mitigation: Have the agent explain the calculation and advise confirming uncertain or uncommon vaccine schedules with the vaccination clinic. <br>
Risk: The calendar flow depends on an external apple-calendar skill and local scheduled reminders. <br>
Mitigation: Verify that the external calendar skill is installed and trusted, and document where reminders are created so users can remove them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jjlew/baby-care) <br>
- [Vaccine Schedule](references/vaccine_schedule.md) <br>
- [Growth Milestones](references/growth_milestones.md) <br>
- [Common Illnesses](references/common_illnesses.md) <br>
- [Feeding Recipes](references/feeding_recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Chinese prose and markdown, with shell commands when creating calendar events or reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute local calendar and scheduled reminder actions for vaccine follow-up when the surrounding agent environment permits it.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
