## Description: <br>
Assists with proactive CV-driven job searches by analyzing a candidate profile, suggesting salary bands, scanning job boards and career pages, scoring matches, preparing application materials, and tracking follow-ups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askenaz](https://clawhub.ai/user/askenaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and their agents use this skill to turn a CV into a structured job-search workflow: profile analysis, market and salary calibration, targeted opportunity scanning, match scoring, tailored CV and cover-letter drafts, and application follow-up tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal CV, profile, application, and seen-job data locally. <br>
Mitigation: Install it only in a private workspace or agent profile, keep the data directory out of version control and shared sync folders, and review stored data before sharing the workspace. <br>
Risk: Job boards may receive search queries derived from configured roles, skills, markets, and salary preferences. <br>
Mitigation: Review configuration before scans and keep query-driving preferences limited to information you are comfortable exposing to external job boards. <br>
Risk: Credentials or tokens placed in config files could be exposed through local files or logs. <br>
Mitigation: Avoid putting tokens or credentials in config.json; use environment variables or the agent platform's secret store when credentials are required. <br>
Risk: Application materials and salary guidance can be inaccurate if the parsed CV profile or benchmarks are stale. <br>
Mitigation: Review the generated profile and drafts before use, refresh the profile when the CV changes, and periodically recalibrate salary references. <br>
Risk: The skill supports application preparation and tracking but should not submit applications automatically. <br>
Mitigation: Keep final submission under user control and review every tailored CV, cover letter, and job match before applying. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/askenaz/cv-driven-job-hunter) <br>
- [Job Boards Reference](artifact/references/job-boards.md) <br>
- [Salary Benchmarks Reference](artifact/references/salary-benchmarks.md) <br>
- [World-Class Companies Reference](artifact/references/world-class-companies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON files, Markdown drafts, and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local CV profiles, job records, application drafts, seen-job state, and notification summaries in the skill data directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
