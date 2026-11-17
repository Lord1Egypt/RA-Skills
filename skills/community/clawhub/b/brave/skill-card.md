## Description:

Operate, automate, and troubleshoot Brave Browser with profiles, Shields, extensions, and Chromium debugging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and browser operators use this skill to run Brave-specific workflows for launch paths, profile isolation, Shields troubleshooting, extension conflicts, local automation, and recovery without treating Brave as generic Chrome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guidance may affect Brave profiles, Shields settings, extensions, sync, wallet-adjacent settings, or local remote debugging.

Mitigation: Ask for explicit approval before sensitive browser actions and prefer per-site, reversible, single-variable changes before broader settings changes.

Risk: Testing or automation in a daily logged-in profile can expose cookies, sessions, extensions, and personal browser state.

Mitigation: Use a disposable test or automation profile when possible, avoid daily profiles for risky debugging, and turn off remote debugging after the task unless the user requests persistence.

Risk: Persistent notes could accidentally capture sensitive browsing, wallet, sync, or account information.

Mitigation: Store only non-secret operating preferences and incident notes under ~/brave/ after user consent; do not store passwords, seed phrases, full browsing history, or private-session content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/brave)
- [Skill homepage](https://clawic.com/skills/brave)
- [Setup guide](artifact/setup.md)
- [Launch and profiles](artifact/launch-and-profiles.md)
- [Shields and compatibility](artifact/shields-and-compatibility.md)
- [Automation and debugging](artifact/automation-and-debugging.md)
- [Extensions, sync, wallet, and private windows](artifact/extensions-and-wallet.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local browser actions, profile notes, and reversible diagnostic steps; requires user approval for sensitive browser-state changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
