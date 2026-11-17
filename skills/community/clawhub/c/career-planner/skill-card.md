## Description:

Career Planner 职业规划顾问 conducts a structured career-planning interview and produces a personalized career plan with recommended roles, growth paths, salary benchmarks, and actionable next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzw6](https://clawhub.ai/user/jzw6)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill when they need career direction, role recommendations, career-change planning, side-hustle exploration, or a personalized action roadmap based on their background, skills, interests, constraints, and goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for sensitive career history, income goals, location or work preferences, and personal constraints.

Mitigation: Confirm the user's career-planning intent before collecting details, and avoid requesting information that is not needed for the plan.

Risk: The skill broadly triggers on vague career-change language, which could start a detailed intake before the user expects it.

Mitigation: Begin with a clear explanation of the planning process and let the user opt into the structured interview.

Risk: The skill saves a personalized career report, which may contain sensitive personal and financial context.

Mitigation: Ask for explicit consent before saving the report and remind the user that the file may include personal career details.

## Reference(s):

- [Career Planner Skill](artifact/SKILL.md)
- [Career Plan Report Template](artifact/references/report-template.md)
- [Role Database](artifact/references/role-database.md)
- [Skill-to-Role Mapping Reference](artifact/references/skill-to-role-map.md)
- [ClawHub Skill Page](https://clawhub.ai/jzw6/skills/career-planner)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational text and a downloadable Markdown career plan report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is personalized from a multi-phase intake interview and may include researched salary or market references when web search is used.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
