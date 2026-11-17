## Description:

Add AI-powered error monitoring and auto-fix generation to any project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hankmint](https://clawhub.ai/user/hankmint)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add AutoHeal error monitoring to JavaScript and TypeScript projects, report runtime errors, and check whether AutoHeal has generated a fix prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser integration examples can expose an AutoHeal API key to client-side users.

Mitigation: Use a backend proxy or restricted public ingestion token instead of placing a privileged AutoHeal API key in frontend code.

Risk: Error messages, stack traces, source URLs, browser details, or user data may be sent to AutoHeal without redaction.

Mitigation: Redact sensitive stack trace, message, URL, and user data fields before sending telemetry.

Risk: Agent-applied monitoring changes can alter production application entry points.

Mitigation: Require explicit human approval and code review before modifying production entry points.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hankmint/skills/autoheal)
- [AutoHeal AI](https://autohealai.com)
- [AutoHeal error ingestion API](https://autohealai.com/api/errors/ingest)
- [AutoHeal error status API](https://autohealai.com/api/errors/{ERROR_ID}/status)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline JavaScript, HTML, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AUTOHEAL_API_KEY environment variable for authenticated API calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
