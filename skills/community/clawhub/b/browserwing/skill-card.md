## Description:

Control browser automation through HTTP API. Supports page navigation, element interaction (click, type, select), data extraction, accessibility snapshot analysis, screenshot, JavaScript execution, and batch operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenhg5](https://clawhub.ai/user/chenhg5)

### License/Terms of Use:


## Use Case:

Developers and automation-focused agents use this skill to control a BrowserWing executor over HTTP for page navigation, element interaction, form filling, page analysis, screenshot capture, JavaScript execution, and data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can expose page content, typed credentials, screenshots, JavaScript execution results, and network activity to the configured executor.

Mitigation: Use only trusted executors, prefer a local executor, review the active tab before actions, and avoid sensitive sites unless that exposure is intended.

Risk: Automated interactions may perform unintended clicks, form submissions, or data extraction if the target page or element reference is wrong.

Mitigation: Call the accessibility snapshot after navigation or page changes, prefer current RefIDs, wait for dynamic content, and review actions before running them on important pages.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the BROWSERWING_EXECUTOR_URL environment variable when available, with a documented local default executor URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
