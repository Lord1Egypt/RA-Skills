## Description:

Automates a real Chrome browser through Chrome DevTools Protocol for navigation, clicking, form filling, data extraction, screenshots, and multi-step web workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottliu007](https://clawhub.ai/user/scottliu007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to drive a logged-in local Chrome session for browser tasks such as navigating sites, collecting page data, filling forms, and capturing screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real logged-in browser session, read page data, fill forms, and execute JavaScript on pages.

Mitigation: Review the skill before installation, require explicit approval before accessing logged-in sites or taking sensitive actions, and keep the documented confirmation boundary for passwords, payments, deletion, and message sending.

Risk: The setup uses Chrome remote debugging and a persistent local browser profile.

Mitigation: Start remote debugging only when needed, close or clean up the debug browser after each task, and avoid exposing the debugging endpoint beyond localhost.

Risk: The MCP setup references an unpinned @latest package.

Mitigation: Pin the Playwright MCP package version before operational use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots, extracted page summaries, and file paths when page data is too long for a response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
