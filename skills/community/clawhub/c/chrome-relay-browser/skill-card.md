## Description:

Controls a user-attached Chrome tab through a local Chrome Extension relay so an agent can navigate, inspect, click, fill, evaluate JavaScript, and capture screenshots while the user can see the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaviwayne](https://clawhub.ai/user/zaviwayne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an agent needs to reuse a visible Chrome tab that the user has already opened and attached, including browsing, screenshots, form filling, clicking, and page inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act inside an attached Chrome tab, including pages that may contain sensitive account data.

Mitigation: Attach non-sensitive tabs when possible and avoid banking, admin, or private account pages unless browser control is explicitly needed.

Risk: The relay token grants local browser-control access.

Mitigation: Treat RELAY_TOKEN like a password and keep it in the configured secrets file rather than exposing it in prompts, logs, or shared output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaviwayne/skills/chrome-relay-browser)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write browser screenshots to local PNG files when the screenshot command is used.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
