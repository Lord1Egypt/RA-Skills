## Description:

WebVoyager helps agents perform multimodal web automation using GUI interaction, visual understanding, browser automation, and end-to-end task workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and execute browser-based workflows that require visual page understanding, DOM or accessibility-tree analysis, form interaction, data extraction, UI testing, and web research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad browser automation and page-data handling authority.

Mitigation: Use a fresh, minimally privileged browser profile and restrict allowed domains and vision backends where possible.

Risk: Automation can submit forms, make purchases, post content, change accounts, enter credentials, or extract sensitive data.

Mitigation: Require manual approval before submissions, purchases, posts, account changes, credential entry, or sensitive extraction.

Risk: Autonomous navigation can act on stale or misread page state.

Mitigation: Verify page state after each action, wait for page stability, and review action logs and screenshots before relying on results.

## Reference(s):

- [WebVoyager code examples](artifact/references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-webvoyager)

## Skill Output:

**Output Type(s):** [Guidance, Code, Text, Markdown]

**Output Format:** [Markdown guidance with TypeScript code examples and structured web-task action logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshots, extracted data, success or failure status, performance metrics, and error diagnostics when used in a browser automation workflow.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
