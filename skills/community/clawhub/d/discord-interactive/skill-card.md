## Description: <br>
Send Discord Components v2 interactive messages (buttons, selects, modals, rich layouts) via the message tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MuseLinn](https://clawhub.ai/user/MuseLinn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send richer Discord interactions when a workflow needs confirmation, option selection, structured status display, or form collection instead of plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interactive controls for sensitive actions can be clicked by the wrong user or treated as authorization without enough confirmation. <br>
Mitigation: Use explicit confirmation flows for sensitive actions and restrict buttons with allowedUsers where appropriate. <br>
Risk: A user may interact with a button, select menu, or modal after the surrounding task context has changed. <br>
Mitigation: Check that the context is still valid before acting on an interaction and update the Discord message when an action expires or completes. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/MuseLinn/discord-interactive) <br>
- [OpenClaw Homepage](https://github.com/openclaw/openclaw) <br>
- [Components v2 Reference](references/components.md) <br>
- [Component Examples](references/examples.md) <br>
- [Handling Component Interactions](references/handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with JSON-style Discord message component examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces message component specifications for the Discord message tool; no shell commands or files are produced.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
