## Description: <br>
Controls user-selected Chrome tabs through Chrome Session Attach, including extension setup, tab attach and detach, screenshots, navigation, form entry, and tab management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meowlegemy-sudo](https://clawhub.ai/user/meowlegemy-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent work in an existing local Chrome tab without requiring a separate OpenClaw-managed browser login. It is suited for browser automation tasks such as page inspection, navigation, clicking, typing, screenshots, and tab management after the user explicitly attaches a tab. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent control of a selected local Chrome tab and relies on a sensitive gateway token. <br>
Mitigation: Keep the gateway token private, keep the gateway bound to 127.0.0.1, attach only the tab needed for the task, avoid highly sensitive tabs unless necessary, and detach when finished. <br>


## Reference(s): <br>
- [Chrome Session Attach on ClawHub](https://clawhub.ai/meowlegemy-sudo/chrome-attach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for installing a Chrome extension, configuring a local gateway connection, attaching or detaching tabs, and invoking OpenClaw browser commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
