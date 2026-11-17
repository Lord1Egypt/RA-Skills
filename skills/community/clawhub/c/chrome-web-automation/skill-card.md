## Description:

Use when the user wants browser automation in an existing Chrome session: click, fill, inspect tabs, capture screenshots, or debug web flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect a live Chrome session, automate browser interactions, reproduce web flow issues, and capture screenshots or notes from the resulting page state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may interact with sensitive tabs or logged-in sites in the user's existing Chrome session.

Mitigation: Before use, close or move away from sensitive tabs and give precise instructions for any clicking, typing, or form submission.

Risk: Actions can target stale or changed page elements after navigation or dynamic updates.

Mitigation: Inspect the current tab, capture page state before interaction, and re-snapshot after navigation or significant DOM changes.

## Reference(s):

- [Chrome Web Automation release page](https://clawhub.ai/wimi321/skills/chrome-web-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with browser action steps, screenshots or evidence references, and reproduction notes when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser interaction transcripts and captured artifacts when the user requests evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
