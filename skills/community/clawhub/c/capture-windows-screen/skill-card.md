## Description:

Capture the current Windows desktop from this WSL/OpenClaw environment and return the PNG path for inspection or delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansheng-li](https://clawhub.ai/user/hansheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support agents use this skill to capture the visible Windows desktop from a WSL/OpenClaw session, inspect the resulting PNG, or stage it for delivery when a user asks to see the current screen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill captures the full Windows desktop, which may include secrets, private messages, tokens, or unrelated open windows.

Mitigation: Use it only on explicit request and avoid running it while sensitive or unrelated information is visible.

Risk: The capture depends on a local C:\OpenClaw\capture-screen.ps1 helper outside the reviewed package.

Mitigation: Review and protect that helper before deployment, and confirm it writes only the expected screenshot output.

Risk: Screenshot staging directories can expose captured desktop images if they are broadly accessible.

Mitigation: Restrict access to the staging directories and use the managed outbound media path only when delivery is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hansheng-li/skills/capture-windows-screen)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Markdown with inline bash commands and plain text PNG paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a staged screenshot path after copying the captured PNG into a workspace or outbound media directory.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
