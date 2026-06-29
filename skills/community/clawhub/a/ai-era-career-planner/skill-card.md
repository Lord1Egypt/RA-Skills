## Description: <br>
Ai Era Career Planner helps users plan education, career direction, and career transitions in the AI era by collecting personal background, assessing interests and values, rating AI impact risk, and producing a personalized career-planning report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mnetfairy](https://clawhub.ai/user/mnetfairy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and career-planning assistants use this skill to explore suitable career paths, school or major choices, AI-era job risks, salary ranges, learning paths, and immediate next actions. It is especially focused on students, early-career users, and workers considering a transition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for career history, education, goals, preferences, and city to personalize advice. <br>
Mitigation: Share only information needed for the planning task and avoid unnecessary sensitive personal details. <br>
Risk: Salary ranges and insurance-company suggestions are planning references and may be incomplete or outdated. <br>
Mitigation: Verify salary data, company credentials, and contact details independently before making decisions or contacting a company. <br>
Risk: Optional integrations can send email, subscribe users to updates, save memory, track progress, or create report files. <br>
Mitigation: Use those actions only after explicit user authorization, and confirm destination, storage location, and cancellation or deletion expectations. <br>
Risk: Career recommendations and AI impact ratings are probabilistic guidance rather than guarantees. <br>
Mitigation: Treat the report as a planning aid and compare it with current market research, professional advice, and the user's own constraints. <br>


## Reference(s): <br>
- [Skill definition](artifact/SKILL.md) <br>
- [AI career impact reference](artifact/references/ai_career_impact.md) <br>
- [Assessment framework](artifact/references/assessment.md) <br>
- [Career anchor reference](artifact/references/career_anchor.md) <br>
- [MBTI quick reference](artifact/references/mbti.md) <br>
- [Education paths](artifact/references/education_paths.md) <br>
- [Job demand trends](artifact/references/job_demand.md) <br>
- [Industry trends](artifact/references/industry_trends.md) <br>
- [Salary reference](artifact/references/salary_data.md) <br>
- [Salary database](artifact/references/salary_database.json) <br>
- [Salary scrape report](artifact/references/salary_scrape_report.txt) <br>
- [Insurance broker company data](artifact/references/insurance_broker_companies.json) <br>
- [Optional integrations](artifact/references/integrations.md) <br>
- [Career tracking system](artifact/references/tracker_system.md) <br>
- [ClawHub skill page](https://clawhub.ai/mnetfairy/skills/ai-era-career-planner) <br>
- [Publisher profile](https://clawhub.ai/user/mnetfairy) <br>
- [Zhaopin](https://www.zhaopin.com/) <br>
- [Liepin](https://www.liepin.com/) <br>
- [BOSS Zhipin](https://www.zhipin.com/) <br>
- [Indeed salary reference](https://cn.indeed.com/career/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88/salaries/%E5%8C%97%E4%BA%AC%E5%B8%82) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown career-planning report, with optional Markdown file output when explicitly requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces personalized recommendations, AI impact ratings, salary references, learning paths, and action lists; optional scripts can generate report files or salary data when explicitly authorized.] <br>

## Skill Version(s): <br>
2.2.147 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
