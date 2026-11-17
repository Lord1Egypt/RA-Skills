## Description:

Plan and execute repeatable browser-based workflows such as opening sites, logging in, navigating dashboards, filling forms, exporting data, taking screenshots, and extracting page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benboby](https://clawhub.ai/user/benboby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other agent users use this skill to plan and run repeatable browser workflows for public pages, logged-in dashboards, reports, forms, screenshots, exports, and visible page data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may interact with logged-in accounts or sensitive account-changing actions.

Mitigation: Confirm the target and outcome before execution, ask for approval before destructive or account-changing actions, and keep manual control for payment, settings, MFA, CAPTCHA, or similarly sensitive steps.

Risk: Browser workflows can fail on CAPTCHA, MFA prompts, anti-bot protections, unpredictable popups, drag-and-drop heavy interfaces, or missing browser automation tooling.

Mitigation: Use read-only web access where possible, prefer existing local automation tools when available, and report where manual takeover or a narrower workflow is needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown report with optional automation commands or scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the goal, automation path, successful steps, likely failure points, and next improvements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
