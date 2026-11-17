## Description:

Browser Automation Core provides reusable browser navigation, interaction, capture, form, and session utilities for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add browser navigation, interaction, screenshot capture, JavaScript evaluation, form-filling patterns, and session utilities to OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive browser sessions, capture page contents, submit forms, and write screenshots locally.

Mitigation: Run it in a constrained environment, avoid authenticated or sensitive sites unless necessary, and require review before form submission or page capture workflows.

Risk: The security evidence reports broad browser and session authority with unsafe network and file-write behaviors.

Mitigation: Pin install versions, restrict CDP access to localhost, and validate URLs and screenshot filenames before use.

Risk: Browser screenshots and captured content may contain sensitive page data.

Mitigation: Use a dedicated screenshot directory, limit retention, and review captured files before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stefanferreira/skills/browser-automation-core)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Puppeteer Documentation](https://pptr.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Selenium Documentation](https://www.selenium.dev/)
- [OpenClaw Browser Integration](/docs/browser-integration)
- [WebSocket Client Examples](/examples/websocket)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python, shell, and JSON examples; runtime outputs may include text, JSON command results, and PNG screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshot and session outputs are written to configured local paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
