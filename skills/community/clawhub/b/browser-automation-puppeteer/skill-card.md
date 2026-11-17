## Description:

Web scraping and browser automation using Puppeteer for extracting data from websites, crawling pages, scraping JavaScript-rendered content, taking screenshots, filling forms, and automating browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fasjdas](https://clawhub.ai/user/fasjdas)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to guide browser-based scraping, crawling, screenshot capture, form interaction, and automation for pages that require JavaScript rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation against arbitrary URLs can expose the agent environment to untrusted web content.

Mitigation: Run the skill only in an isolated, unprivileged environment with limited network access and restrict allowed URL targets where possible.

Risk: The browser process could access secrets, credentials, cookies, or internal services if they are available in the execution environment.

Mitigation: Do not expose secrets or internal services to the browser process, and require explicit user confirmation before submitting forms or using credentials or cookies.

Risk: Installing Puppeteer without a reviewed lockfile can introduce unpinned dependency changes.

Mitigation: Pin Puppeteer and related packages with a reviewed lockfile before production use.

## Reference(s):

- [Puppeteer API Reference](references/puppeteer-api.md)
- [ClawHub skill page](https://clawhub.ai/fasjdas/skills/browser-automation-puppeteer)
- [Publisher profile](https://clawhub.ai/user/fasjdas)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; included scripts emit JSON or PNG files when run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots, extracted page data, crawler results, and Puppeteer automation snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
