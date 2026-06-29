## Description: <br>
高考志愿填报智能规划技能，面向中国高考考生提供分数定位、院校专业匹配、冲稳保方案和信息差机会分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yibeixiaobai](https://clawhub.ai/user/yibeixiaobai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, especially Chinese Gaokao students and families, use this skill to build a data-driven college application plan, compare schools and majors, and identify special admissions or lower-visibility opportunities that may affect application strategy. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Admissions recommendations can be wrong or outdated because score lines, deadlines, eligibility rules, tuition, and special-program policies change by province and school. <br>
Mitigation: Treat the output as planning guidance and verify final choices with the provincial exam authority and official university admissions offices before submitting applications. <br>
Risk: The skill may request sensitive planning details such as score, province, subject track, preferences, eligibility status, and budget. <br>
Mitigation: Share only details needed for admissions planning and avoid unnecessary identity documents or unrelated personal information. <br>
Risk: Special-program, transfer-major, early-batch, and cooperative-program opportunities may carry eligibility, compatibility, tuition, or enrollment restrictions. <br>
Mitigation: Confirm program eligibility, batch conflicts, transfer rules, fees, and approved program status through official sources before relying on them. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/yibeixiaobai/college-admission-planner) <br>
- [ClawHub skill page](https://clawhub.ai/yibeixiaobai/skills/college-admission-plan) <br>
- [院校专业匹配策略参考手册](references/matching-strategy.md) <br>
- [特殊招生通道参考手册](references/special-programs.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown report with tables, stepwise planning notes, action checklists, and risk reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided province, subject track, score, major interests, location preferences, eligibility details, and budget to shape the plan.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
