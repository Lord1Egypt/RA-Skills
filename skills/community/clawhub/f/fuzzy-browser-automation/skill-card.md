## Description:

Automate browser tasks with OpenClaw's Playwright browser control for navigation, interaction, screenshots, PDFs, data extraction, form workflows, monitoring, downloads, and attended login automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control a Chromium browser for dynamic scraping, form filling, screenshots, PDF generation, multi-step web flows, content monitoring, downloads, and attended login workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate actions in a real logged-in browser session, including account-changing clicks and credential entry.

Mitigation: Use the sandbox browser for routine automation and allow host or user-profile browser access only for attended, explicitly approved tasks.

Risk: Arbitrary page JavaScript evaluation can expose page data or perform unintended actions in the browser context.

Mitigation: Review each evaluate function before execution and restrict it to narrow read-only extraction unless a trusted operator approves otherwise.

Risk: Form submission and login flows can affect external accounts or services.

Mitigation: Require human presence and explicit confirmation before login automation, credential entry, purchases, submissions, or other state-changing actions.

## Reference(s):

- [Source artifact: skill.md](artifact/skill.md)
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/fuzzy-browser-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON-style browser tool examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser action sequences, locator guidance, screenshots, PDFs, extracted page data, and troubleshooting recommendations.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
