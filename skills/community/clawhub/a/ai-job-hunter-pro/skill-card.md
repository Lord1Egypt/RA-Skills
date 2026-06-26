## Description: <br>
AI Job Hunter Pro helps agents match resumes to job listings, generate application materials, run dry-run application workflows, and track job-search progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MeteorYF](https://clawhub.ai/user/MeteorYF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and job seekers use this skill to search job listings, compare roles against a resume, generate reviewable cover letters and ATS suggestions, and track application status across a job-search funnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive resume, profile, and application-tracking data in local files and databases. <br>
Mitigation: Run it in a dedicated environment, protect the local Chroma and SQLite data directories, and avoid sharing generated data files. <br>
Risk: Generated cover letters can include hard-coded Disney, Amazon, and UCL claims that may not apply to the user. <br>
Mitigation: Review every generated application material and remove or replace any claim that is not true for the applicant. <br>
Risk: Application automation can submit materials to job platforms if run outside dry-run mode. <br>
Mitigation: Keep dry-run and explicit confirmation enabled, verify each application before submission, and respect platform rate limits. <br>
Risk: Browser-based platform integrations may depend on logged-in sessions and platform anti-automation rules. <br>
Mitigation: Treat browser sessions as sensitive, monitor blocks or errors, pause when platforms object, and use manual fallback when needed. <br>


## Reference(s): <br>
- [AI Job Hunter Pro on ClawHub](https://clawhub.ai/MeteorYF/ai-job-hunter-pro) <br>
- [Platform Integration Notes](references/platform_notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-formatted script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local profile data, a local vector database, a SQLite application tracker, generated cover letters, ATS suggestions, and dashboard data files.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
