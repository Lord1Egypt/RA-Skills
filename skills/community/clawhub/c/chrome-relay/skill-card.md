## Description:

Control the user's local Chrome browser through the OpenClaw Browser Relay extension to automate selected tabs, read page content, and use existing logged-in browser sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meowlegemy-sudo](https://clawhub.ai/user/meowlegemy-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they want an agent to work with their local Chrome browser, including selected logged-in tabs, page snapshots, navigation, clicks, typing, and screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent read and act on attached Chrome tabs, including pages where the user is already signed in.

Mitigation: Attach only tabs the user explicitly wants the agent to control, avoid sensitive financial, admin, healthcare, or similar pages unless intended, and detach the extension when finished.

Risk: Browser actions may target the wrong element when selectors are stale or unreliable.

Mitigation: Refresh page snapshots before acting and prefer explicit JavaScript evaluation for complex interactions when aria-ref selectors time out.

## Reference(s):

- [Chrome Relay skill page](https://clawhub.ai/meowlegemy-sudo/skills/chrome-relay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and browser tool examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is intended for user-directed control of attached Chrome tabs through the OpenClaw Browser Relay extension.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
