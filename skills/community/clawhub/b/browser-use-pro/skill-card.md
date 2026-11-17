## Description:

AI-powered browser automation for complex multi-step web workflows using the Browser-Use framework when OpenClaw's built-in browser tool cannot handle login flows, anti-bot sites, or longer action sequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abczsl520](https://clawhub.ai/user/abczsl520)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to automate complex multi-step browser workflows, including login-backed navigation, form filling, batch operations, and workflows that need Playwright or a user-launched Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control logged-in browser sessions and may act on sensitive websites.

Mitigation: Use it only in a trusted local environment, prefer isolated Playwright or browser profiles, restrict allowed domains, and review proposed actions before running them.

Risk: Browsing context may be sent to an external AI service for step-by-step reasoning.

Mitigation: Avoid using real secrets in prompts or saved scripts, disable vision when secrets are involved, and use Browser-Use sensitive-data placeholders for credentials.

Risk: CDP mode exposes a debug-enabled Chrome session that could include user cookies and logged-in state.

Mitigation: Launch CDP only when explicitly needed, require user initiation, close the debug-enabled Chrome session immediately after use, and avoid using a primary browser profile.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local setup steps, browser-mode selection, generated automation scripts, and troubleshooting guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
