## Description:

Cdp Browser Pilot guides agents through CDP-based browser automation for JavaScript-rendered pages, SPA navigation, screenshots, tab management, connection handling, anti-detection patterns, and cookie handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation-focused teams use this skill to drive browser workflows that require page interaction, logged-in browser state, JavaScript execution, screenshots, SPA routing, or multi-tab coordination. Use should be limited to authorized automation where browser-session access and site policies have been reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may access local browser sessions and authenticated page content.

Mitigation: Install and run only for authorized workflows, and use a dedicated browser profile when possible.

Risk: Cookie handling can expose session cookies that may function like account credentials.

Mitigation: Do not read, export, log, or share cookies unless explicitly authorized; treat any captured cookies as secrets.

Risk: Anti-bot evasion guidance can be misused to bypass site protections or terms.

Mitigation: Use automation only where permitted by the site owner, contract, policy, or applicable law, and complete human review before installation.

## Reference(s):

- [Cdp Browser Pilot on ClawHub](https://clawhub.ai/thcjp/skills/cdp-browser-pilot-pro)
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, PowerShell snippets, JavaScript examples, and structured browser-automation instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser automation steps that access local browser sessions, cookies, tabs, screenshots, and JavaScript-rendered page content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
