## Description:

AI-powered job search assistant with RAG-based resume-JD matching, automated application pipeline, and status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meteoryf](https://clawhub.ai/user/meteoryf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and job seekers use this skill to match resumes against job descriptions, draft tailored application materials, track job-search progress, and review proposed applications before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive profile, resume, feedback, and application history data locally.

Mitigation: Treat local profile, vector database, feedback, and tracker files as sensitive and restrict filesystem access to trusted users.

Risk: Generated cover letters, resume highlights, or application records may contain incorrect or misleading claims.

Mitigation: Use dry-run mode, inspect every generated application artifact, and require explicit user confirmation before submission.

Risk: Dashboard or job data handling may expose users to unsafe URLs or untrusted job JSON.

Mitigation: Avoid opening the dashboard with untrusted job data until URL handling and third-party script loading have been reviewed.

Risk: Dependency and scraping behavior may change across job platforms or local environments.

Mitigation: Install dependencies in a locked environment, respect platform rate limits, and fall back to manual review when a platform blocks or errors.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/meteoryf/skills/ai-job-hunter-pro)
- [Platform integration notes](references/platform_notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, generated application text, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate cover letters, resume highlights, job match explanations, tracker reports, and local configuration guidance.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
