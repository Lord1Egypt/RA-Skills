## Description:

Control a Mac through natural language - open apps, click buttons, read the screen, type text, manage windows, and automate multi-step tasks via Airpoint's AI computer-use agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marioandf](https://clawhub.ai/user/marioandf)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent to operate a macOS desktop through the Airpoint CLI for screen reading, app control, typing, window management, and multi-step automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls the Mac through broad Accessibility and Screen Recording permissions.

Mitigation: Install only when that level of local screen and input access is acceptable, and review granted macOS permissions before use.

Risk: Screen content may include secrets, private messages, regulated data, payments, or account settings.

Mitigation: Avoid running tasks while sensitive information is visible unless the user explicitly intends Airpoint and configured model providers to process that context.

Risk: Broad or fire-and-forget tasks can continue acting on the desktop without close supervision.

Mitigation: Use narrow task prompts, review results and screenshots, and run `airpoint stop` if the task is stuck or behaving unexpectedly.

## Reference(s):

- [Airpoint homepage](https://airpoint.app)
- [ClawHub skill listing](https://clawhub.ai/marioandf/skills/airpoint)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to screenshot file paths produced by the Airpoint CLI; macOS only.]

## Skill Version(s):

1.3.16 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
