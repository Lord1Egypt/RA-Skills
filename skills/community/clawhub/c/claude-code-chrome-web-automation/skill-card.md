## Description:

Use when the user wants browser automation in an existing Chrome session: click, fill, inspect tabs, capture screenshots, or debug web flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and automate a live Chrome browser session for web app debugging, form filling, tab inspection, screenshot capture, and reproducing UI issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate an active Chrome session, including pages with logged-in accounts, payments, posting, or data-changing workflows.

Mitigation: Review browser actions involving accounts, payments, public posting, or data changes before allowing them to proceed.

Risk: Browser state can change between steps, making stale page references or assumptions lead to incorrect actions.

Mitigation: Inspect tabs and context first, snapshot before interaction, and re-snapshot after navigation or large DOM updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wimi321/skills/claude-code-chrome-web-automation)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, screenshots]

**Output Format:** [Markdown or plain text guidance with browser action results and screenshots when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include observations from the active Chrome session; review sensitive or state-changing browser actions before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
