## Description: <br>
AI-powered CV generator for job applications that sets up automated job search with CareerForge CLI, manages master resume creation, configures filtering criteria, and generates tailored CVs on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alon-mini](https://clawhub.ai/user/alon-mini) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Job seekers use this skill to create or update a master resume, configure job-search filters, automate job listing discovery, and generate tailored CVs for specific postings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs an external CareerForge CLI with npm, and the security evidence notes that this external code is unpinned. <br>
Mitigation: Review the CareerForge CLI repository and pin a trusted revision before running npm install or generated commands. <br>
Risk: The skill handles sensitive resume data, job preferences, generated CVs, and application configuration. <br>
Mitigation: Keep the workspace private, avoid committing generated resumes or configuration files, and delete local resume/CV artifacts when no longer needed. <br>
Risk: The workflow uses a Gemini API key and may store it in the environment or a .env file. <br>
Mitigation: Treat the API key like a password, keep .env files out of version control, and rotate the key if it may have been exposed. <br>
Risk: Scheduled job-search automation can send job details or generated CVs through Telegram. <br>
Mitigation: Confirm Telegram recipients and group membership before enabling automation, and review generated CVs before sending them. <br>


## Reference(s): <br>
- [CareerForge CLI repository](https://github.com/alon-mini/CareerForge-cli) <br>
- [Master Resume Template](references/master_resume_template.md) <br>
- [Job Search Configuration](references/job_search_config.md) <br>
- [CareerForge CLI Usage Guide](references/cli_usage.md) <br>
- [ClawHub release page](https://clawhub.ai/alon-mini/careerforge-cli-skill) <br>
- [Publisher profile](https://clawhub.ai/user/alon-mini) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and resume/CV file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local resume and CV files through helper scripts or CareerForge CLI commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
