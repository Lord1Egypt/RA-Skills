## Description:

Browser CDP lets an agent control a local Chrome session to open pages, interact with elements, evaluate page JavaScript, extract rendered content, and capture screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent needs to operate a user-authorized local Chrome session for login-gated, JavaScript-rendered, search-results, or otherwise blocked browsing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in Chrome session through a local proxy.

Mitigation: Use a dedicated Chrome profile with minimal accounts and avoid sensitive sites while the proxy is running.

Risk: Browser actions can include state-changing operations such as clicks, form interactions, navigation, JavaScript evaluation, and file input handling.

Mitigation: Permit uploads or state-changing actions only when explicitly requested and review the target page and action before execution.

Risk: Leaving the proxy running extends the window in which an agent can control the connected browser session.

Mitigation: Stop the proxy when the task is complete and restart it only for intentional browser-control work.

## Reference(s):

- [browser-cdp ClawHub skill page](https://clawhub.ai/0xcjl/skills/browser-cdp)
- [Usage Log](references/usage-log.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide browser actions that return JSON responses or save screenshots through the local proxy API.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
