## Description: <br>
Career Planner China helps users with AI-era career planning in China by collecting background information, assessing interests and work values, evaluating AI career impact, and producing personalized career direction guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mnetfairy](https://clawhub.ai/user/mnetfairy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, students, and career changers in China use this skill to explore career paths, education choices, industry transitions, AI exposure, salary expectations, and practical next steps. The skill can also guide optional Markdown report generation when the host environment and user request allow it. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process personal career, education, personality, location, and values information. <br>
Mitigation: Ask users only for information needed for the requested planning task and avoid storing or forwarding personal profiles unless the user explicitly requests it. <br>
Risk: Optional integrations could email reports, subscribe users to updates, call external APIs, or persist memory/profile files. <br>
Mitigation: Use integrations only after explicit user authorization and after showing what information will be sent, stored, or subscribed. <br>
Risk: Insurance-company recommendations may steer users toward specific companies. <br>
Mitigation: Present insurance listings as a directory starting point, disclose that recommendations are for reference only, and encourage users to compare options independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mnetfairy/skills/career-planner-china) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Assessment framework](artifact/references/assessment.md) <br>
- [AI career impact reference](artifact/references/ai_career_impact.md) <br>
- [Career anchor reference](artifact/references/career_anchor.md) <br>
- [Job demand trends](artifact/references/job_demand.md) <br>
- [Industry trends](artifact/references/industry_trends.md) <br>
- [Education paths](artifact/references/education_paths.md) <br>
- [Salary database](artifact/references/salary_database.json) <br>
- [Insurance broker company list](artifact/references/insurance_broker_companies.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Conversational text and structured Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include career profiles, AI-risk ratings, salary ranges, recommended paths, action lists, and optional report-generation commands.] <br>

## Skill Version(s): <br>
2.2.143 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
