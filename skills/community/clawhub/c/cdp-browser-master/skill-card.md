## Description:

CDP浏览器大师 guides agents through Chrome DevTools Protocol workflows for controlling logged-in Edge or Chrome browser sessions, navigating SPA pages, probing DOM selectors, waiting for network idle, taking screenshots, and extracting page data or cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation teams use this skill to operate existing logged-in local Chrome or Edge sessions for JS-rendered page inspection, data extraction, clicks and forms, screenshots, SPA navigation, and cookie retrieval when simpler fetch-based access is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in browser control can expose authenticated sessions or perform actions on behalf of the user.

Mitigation: Use a dedicated temporary browser profile and restrict remote debugging to local trusted use.

Risk: The skill can retrieve raw cookies, including HttpOnly cookies through CDP, which may disclose session credentials.

Mitigation: Avoid exporting raw cookies and do not use the skill on accounts or sites where session disclosure could cause financial, business, or privacy harm.

Risk: The artifact under-discloses or contradicts security implications of browser control and cookie extraction.

Mitigation: Review the skill before installation and follow the server security guidance rather than relying on the artifact's generic safety claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cdp-browser-master)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline PowerShell, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce extracted DOM data, cookie strings, screenshots as base64, execution logs, and error messages.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
