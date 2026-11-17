## Description:

Controls Brave Browser via CDP for web browsing, content extraction, screenshots, JavaScript execution, dynamic content interaction, and browser automation when Brave is running with remote debugging on port 9222.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to attach to a user-managed Brave Browser session for web browsing, extraction, dynamic page interaction, screenshots, JavaScript execution, and SPA publishing diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate against a logged-in daily Brave Browser session, which may expose personal accounts and sensitive page data.

Mitigation: Prefer a separate temporary Brave profile with no personal logins before enabling CDP access.

Risk: JavaScript evaluation, screenshots, clicks, form submissions, and publishing actions can read sensitive content or change page state.

Mitigation: Require manual confirmation before these actions and use an explicit tab or origin allowlist.

Risk: Cookie, local storage, session storage, and form-value extraction examples can capture sensitive authentication or personal data.

Mitigation: Avoid cookie, storage, and form dumps unless the user explicitly requests them for a trusted origin.

Risk: Anti-detection and publishing automation may conflict with site rules or user expectations.

Mitigation: Require user approval before automation on sites with anti-bot controls or before any publishing workflow.

## Reference(s):

- [Common Patterns](references/PATTERNS.md)
- [Site-Specific Patterns](references/site-patterns.md)
- [Framework-Aware Click Strategies](references/framework-publish.md)
- [ClawHub Skill Page](https://clawhub.ai/mayf3/skills/brave-browser-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON command output, extracted text, and optional screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-managed Brave Browser instance with CDP remote debugging on port 9222; browser actions may read or change page state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
