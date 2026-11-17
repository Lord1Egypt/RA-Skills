## Description:

Browser automation with human-like behavior for JavaScript-rendered sites, login sessions, form filling, clicking, scrolling, screenshots, downloads, and complex interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lesliepie](https://clawhub.ai/user/lesliepie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and generate Playwright-based browser automation for dynamic websites, authenticated workflows, forms, screenshots, downloads, and data extraction tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes bot-detection evasion and stealth guidance that can create policy, terms-of-service, or authorization risk.

Mitigation: Use stealth or bot-detection bypass techniques only for explicitly authorized testing and respect site terms, robots policies, and rate limits.

Risk: Browser session state files, screenshots, recordings, and downloads may contain sensitive data.

Mitigation: Store these artifacts securely, minimize retention, and avoid sharing them unless they have been reviewed for secrets and personal data.

Risk: Commands may install global dependencies or run browser launch options that weaken isolation, including disabling the Chromium sandbox.

Mitigation: Prefer project-local, pinned Playwright dependencies and do not disable the browser sandbox unless a reviewed environment requires it.

## Reference(s):

- [Playwright documentation](https://playwright.dev)
- [ClawHub skill page](https://clawhub.ai/lesliepie/skills/browseragent)
- [Publisher profile](https://clawhub.ai/user/lesliepie)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may produce browser automation snippets that require Node.js, npx, and Playwright.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
