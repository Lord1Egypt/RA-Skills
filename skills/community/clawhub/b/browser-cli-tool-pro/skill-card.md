## Description:

浏览器CLI工具-专业版 helps agents operate an enterprise browser automation CLI for batch task orchestration, concurrent sessions, retries, scheduling, monitoring, screenshots, and structured result reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, and operations teams use this skill to plan and run browser CLI workflows for batch sign-ins, form submission, data collection, end-to-end testing, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may affect accounts, submit forms, capture screenshots, reuse login state, or trigger scheduled jobs and webhook notifications without enough task scoping.

Mitigation: Use only for explicit browser automation tasks, require confirmation before account actions, screenshots, form submissions, scheduled jobs, or webhook notifications, and keep shared login-state stores behind team access controls.

Risk: The skill depends on an external npm browser automation package.

Mitigation: Verify the npm package source and installation path before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, Python, YAML, and JSON examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose browser CLI actions, session and state configuration, screenshots and log archival, metrics export, and webhook notification setup.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
