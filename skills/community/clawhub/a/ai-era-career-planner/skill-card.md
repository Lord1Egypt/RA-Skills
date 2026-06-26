## Description: <br>
AI-era career planning assistant that gathers a user's career profile, applies Holland interest, MBTI, career-anchor, AI-impact, salary, education-path, and industry-trend references, and returns a personalized career planning report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mnetfairy](https://clawhub.ai/user/mnetfairy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and career advisors use this skill to explore career direction, education choices, professional transitions, and AI-era job risk or opportunity. The skill produces structured recommendations, short-term and long-term action plans, and optional Markdown career reports when export is explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for personal career-profile details such as age or life stage, education background, preferences, work expectations, and career concerns. <br>
Mitigation: Provide only information needed for the planning task, and do not export, email, save, subscribe, or use live data unless the user explicitly requests and confirms that action. <br>
Risk: Career planning, salary ranges, job-demand trends, and AI-impact ratings are informational and may become stale or may not fit a specific local market. <br>
Mitigation: Treat recommendations as planning guidance, verify important salary and labor-market details with current sources before making career or education decisions, and present uncertainty clearly. <br>
Risk: Insurance-company contact recommendations could be mistaken for endorsement or sales advice. <br>
Mitigation: Use those recommendations only when the user has shown interest in insurance roles, keep the wording neutral, and independently verify company qualifications before contacting any company. <br>


## Reference(s): <br>
- [AI career impact reference](references/ai_career_impact.md) <br>
- [Career assessment framework](references/assessment.md) <br>
- [MBTI career personality reference](references/mbti.md) <br>
- [Career anchor reference](references/career_anchor.md) <br>
- [Education paths](references/education_paths.md) <br>
- [Salary data reference](references/salary_data.md) <br>
- [Job demand trends](references/job_demand.md) <br>
- [Industry trends](references/industry_trends.md) <br>
- [Career planning dialogue flow](references/flow_engine.md) <br>
- [Insurance broker company data](references/insurance_broker_companies.json) <br>
- [Optional integrations](references/integrations.md) <br>
- [Skill release page](https://clawhub.ai/mnetfairy/skills/ai-era-career-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational text or Markdown career planning report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional Markdown report export is available only when the host environment allows it and the user explicitly requests it.] <br>

## Skill Version(s): <br>
2.2.139 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
