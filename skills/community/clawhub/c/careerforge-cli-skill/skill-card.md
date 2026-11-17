## Description:

Job-Hunter helps users set up CareerForge CLI to automate job-search filtering, create or update a master resume, and generate tailored CVs for specific job postings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alon-mini](https://clawhub.ai/user/alon-mini)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure automated job searches, maintain a master resume, and generate tailored CV documents from job details with CareerForge CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned external CareerForge CLI code.

Mitigation: Review the external repository and pin a trusted version before installation or execution.

Risk: Resume files, generated CVs, API keys, scheduled jobs, and Telegram delivery can expose sensitive job-search or personal data.

Mitigation: Keep resume artifacts in a private workspace, keep API keys out of chat and committed files, verify cron behavior before enabling it, and send Telegram notifications only to trusted recipients.

## Reference(s):

- [Master Resume Template](references/master_resume_template.md)
- [Job Search Configuration](references/job_search_config.md)
- [CareerForge CLI Usage Guide](references/cli_usage.md)
- [CareerForge CLI Repository](https://github.com/alon-mini/CareerForge-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and generated resume/CV file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of resume markdown, job-search JSON configuration, scheduled automation, and generated HTML/PDF CV outputs through the external CareerForge CLI.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
