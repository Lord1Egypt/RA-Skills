## Description:

Dexter Browser Automation uses Playwright to capture screenshots, scrape rendered HTML, extract structured page data, and interact with JavaScript-rendered pages when simpler web tools are insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylerdotai](https://clawhub.ai/user/tylerdotai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a last-resort browser automation layer for JavaScript-rendered pages, UI interactions, screenshots, and structured extraction after search or static fetch tools are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser navigation and UI interaction can reach untrusted pages or trigger unintended actions.

Mitigation: Run the skill as an unprivileged user in an isolated environment with restricted network access, and confirm target URLs and actions before use.

Risk: Fill commands can handle passwords or other secrets, which may expose sensitive values through command lines or logs.

Mitigation: Avoid passing passwords or secrets on the command line, and do not use authenticated workflows without explicit confirmation and appropriate secret handling.

Risk: Screenshot and browser automation flows can write local files.

Mitigation: Constrain output paths to scratch directories and review generated files before reuse.

Risk: The browser scripts launch Chromium with no-sandbox-style flags.

Mitigation: Use an external sandbox such as a container or VM and pin Playwright and browser versions before deployment.

## Reference(s):

- [Dexter Browser Automation on ClawHub](https://clawhub.ai/tylerdotai/skills/dex-browser)
- [CSS Selectors Reference](references/selectors.md)
- [Common Browser Automation Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts return JSON responses and screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendered HTML is truncated to 50k characters, extraction is capped at 50 elements, and screenshots default to /tmp/screenshot.png.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
