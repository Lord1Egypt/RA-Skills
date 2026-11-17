## Description:

Captures the visible screen with PowerShell, copies the screenshot into the workspace, and sends it to Feishu when the user requests a screenshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tootw](https://clawhub.ai/user/tootw)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill to capture the currently visible screen and send the resulting image to Feishu from direct screenshot requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may capture everything visible on the primary screen, including sensitive windows or notifications.

Mitigation: Close or hide sensitive content before use and prefer a preview or confirmation step before transmission.

Risk: Broad screenshot requests can lead to sending a screenshot to Feishu without clear confirmation.

Mitigation: Use the skill only when the user explicitly requests both screenshot capture and Feishu delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tootw/skills/feishu-screenshot)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a screenshot file path and a Feishu send action for the agent to execute.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
