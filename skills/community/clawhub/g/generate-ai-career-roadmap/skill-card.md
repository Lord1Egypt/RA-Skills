## Description:

根据使用者的简历或引导式问答，生成基于最新证据的 AI 与泛 AI 职业机会报告和个性化学习路线。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxndenyme](https://clawhub.ai/user/yxndenyme)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn a resume or guided intake into a Chinese-first AI career opportunity report, role fit analysis, portfolio direction, and personalized learning roadmap. It is intended for career planning across AI, adjacent AI roles, and industry-specific transition paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume and career inputs may contain unnecessary personal, salary, employer, or confidential information.

Mitigation: Remove phone numbers, addresses, IDs, salary details, confidential employer information, and other nonessential personal data before using the skill.

Risk: AI labor-market recommendations can become stale or overstate emerging roles if current evidence is weak.

Mitigation: Use the skill's current web research requirement, prefer official and primary sources, separate verified current opportunities from predictions, and include evidence dates in the report.

Risk: A generated learning plan may assume the wrong region, language, schedule, or file-saving preference.

Mitigation: Specify the target region, preferred language, plan length, weekly time budget, hard constraints, and whether output files may be saved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxndenyme/skills/generate-ai-career-roadmap)
- [Intake profile reference](references/intake-profile.md)
- [Research policy reference](references/research-policy.md)
- [Role taxonomy reference](references/role-taxonomy.md)
- [Learning plan framework reference](references/learning-plan-framework.md)
- [Report contract reference](references/report-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown career report with tables, source links, role scoring, learning roadmap, and optional local file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output; uses current web research for market-sensitive conclusions and validates report structure when Python is available]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
