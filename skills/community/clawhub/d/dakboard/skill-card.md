## Description:

Manage DAKboard screens, devices, and push custom display data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisclarkdev](https://clawhub.ai/user/krisclarkdev)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to list DAKboard devices and screens, update a device's assigned screen, and push metric or JSON fetch data to DAKboard displays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The DAKBOARD_API_KEY is sent to DAKboard in request URLs, which can increase exposure through logs or diagnostics.

Mitigation: Use a dedicated, revocable DAKboard API key and rotate it if logs, diagnostics, or shared command history may have exposed it.

Risk: The skill can change DAKboard screen assignments and publish user-provided metric or fetch data to DAKboard displays.

Mitigation: Install only for trusted DAKboard accounts and review requested device, screen, metric, and fetch data before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krisclarkdev/skills/dakboard)
- [DAKboard API endpoint](https://dakboard.com/api/)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DAKBOARD_API_KEY in the environment and sends requested device, screen, metric, and fetch data to DAKboard.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
