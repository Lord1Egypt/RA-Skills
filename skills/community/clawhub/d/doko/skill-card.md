## Description:

Reads, searches, and extracts content from JavaScript-rendered and dynamic web pages through a real Chrome browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dokobot](https://clawhub.ai/user/dokobot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external agents use this skill to read, search, and extract rendered web content when ordinary headless fetchers cannot capture JavaScript-heavy, dynamic, or logged-in pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access pages visible in a logged-in Chrome session, including sensitive or private content.

Mitigation: Use a dedicated browser profile for sensitive work and avoid email, finance, healthcare, admin, or internal sites unless that content is intended to be read.

Risk: Remote mode may route rendered private page content through Dokobot's remote service by default.

Mitigation: Prefer explicit local mode when possible and enable remote mode only when the user intends to use the remote service.

Risk: The workflow depends on an npm CLI package and Chrome extension with broad browser-reading access.

Mitigation: Verify or pin the Dokobot package before installing and only use the extension where its page access is acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dokobot/skills/doko)
- [Dokobot homepage](https://dokobot.ai)
- [Dokobot API keys dashboard](https://dokobot.ai/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell command examples and extracted web-page text from CLI calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session identifiers for continued reads and downloaded image files when image extraction is requested.]

## Skill Version(s):

2.3.4 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
