## Description:

Automate Job Application helps an agent find resume-matched jobs, present an approval list, fill approved application forms, draft cover letters, submit applications, and log outcomes through resumex.dev.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atharva-badgujar](https://clawhub.ai/user/atharva-badgujar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and job seekers use this skill to search for current roles that match their resume, review ranked recommendations, and apply to approved jobs with agent-assisted form filling and cover-letter drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit job applications and transmit personal resume data to job application websites.

Mitigation: Require explicit user approval before any application is submitted, review the completed form before submission, and use a low MAX_APPLICATIONS value for testing.

Risk: The ResumeX API key and local preferences can expose sensitive personal data.

Mitigation: Store RESUMEX_API_KEY only as an environment variable, restrict data/user_preferences.json permissions, avoid saving sensitive legal-consent answers for reuse, and delete preferences after use when appropriate.

Risk: Saved or generated screening responses may be inaccurate, outdated, or inappropriate for a specific application.

Mitigation: Confirm sensitive and material screening answers with the user, allow the user to decline optional fields, and review generated cover letters or free-text answers before submitting.

Risk: Some job boards, login pages, CAPTCHA flows, or file upload steps may not be suitable for automation.

Mitigation: Use manual handling for LinkedIn Easy Apply, CAPTCHA, login-gated applications, external redirects, and resume or CV upload fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atharva-badgujar/skills/auto-job-applier)
- [ResumeX](https://resumex.dev)
- [ResumeX API Docs](https://resumex.dev/api-docs)
- [OpenClaw](https://openclaw.dev)
- [Form Field Mappings Reference](references/form_field_mappings.md)
- [Job Boards Reference](references/job_boards.md)
- [Screening Questions Reference](references/screening_questions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a required RESUMEX_API_KEY environment variable, requests>=2.28.0, and local preference files for reusable application details.]

## Skill Version(s):

2.1.0 (source: server release metadata and README changelog, released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
