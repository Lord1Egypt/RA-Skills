## Description:

Guides AI agents in using Chrome Remote Debugging Protocol on port 9222 to automate browser interactions such as navigation, screenshots, page inspection, form input, scrolling, JavaScript execution, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgx-00](https://clawhub.ai/user/lgx-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to guide browser automation on login-gated or JavaScript-rendered pages when lightweight fetch tools are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Chrome sessions can expose private page content, account data, screenshots, and script-readable information to the agent.

Mitigation: Use the skill only on pages the agent is intended to inspect, avoid sensitive account, security, and billing pages unless necessary, and treat screenshots and extracted JavaScript results as private.

Risk: Arbitrary page JavaScript can retrieve data beyond what is visible in a screenshot or accessibility snapshot.

Mitigation: Review JavaScript before execution and prefer targeted, read-only extraction for the specific task.

Risk: Screenshot URLs can disclose private visual information from logged-in pages.

Mitigation: Capture screenshots only when needed and avoid sharing or retaining screenshot links beyond the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgx-00/skills/chrome-remote-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command examples and inline shell/code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces procedural guidance only; it does not run browser actions by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
