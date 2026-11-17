## Description:

Read, capture, or interact with browser-rendered websites through AdsCrawl. Use when an AI agent needs to extract a page as Markdown, structured article JSON, or HTML; capture a viewport or full-page PNG screenshot; or create a remote CDP browser session for multi-step interaction, JavaScript-heavy applications, login flows, Playwright, Puppeteer, Selenium, or browser debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adscrawl](https://clawhub.ai/user/adscrawl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve rendered web content, capture screenshots, or open a remote browser session through AdsCrawl for browser automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AdsCrawl requests send target URLs and requested browser actions to an external AdsCrawl service.

Mitigation: Install only when AdsCrawl use is intended, and avoid submitting sensitive URLs, personal data, cookies, or authenticated actions unless explicitly authorized.

Risk: API keys, CDP URLs, cookies, or proxy credentials could be exposed through code, logs, or responses.

Mitigation: Keep ADSCRAWL_API_KEY and token-bearing CDP URLs private, avoid logging secrets, and report only safe error details.

Risk: A custom ADSCRAWL_BASE_URL could redirect browser tasks or credentials to an untrusted endpoint.

Mitigation: Use the default AdsCrawl endpoint unless ADSCRAWL_BASE_URL points to a trusted AdsCrawl-compatible HTTPS service.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/AdsCrawl/skills/tree/main/skills)
- [ClawHub skill listing](https://clawhub.ai/adscrawl/skills/adscrawl)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of Markdown, JSON, HTML, PNG screenshot, or CDP session outputs through AdsCrawl API workflows.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
