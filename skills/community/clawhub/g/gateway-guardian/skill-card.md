## Description:

Gateway Guardian provides a Bash watchdog for checking an OpenClaw gateway, attempting restart or backup recovery, and logging gateway recovery events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to monitor a local OpenClaw gateway, restart it when health checks fail, and recover from invalid configuration using a backup file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the script as-is may disclose gateway status through alerts sent to a fixed Telegram recipient.

Mitigation: Remove or replace the hard-coded Telegram recipient and make notifications opt-in before running the watchdog.

Risk: The recovery path can overwrite the active OpenClaw configuration with a backup file without clear user control.

Mitigation: Require validation or confirmation before replacing the active configuration, and keep a separate backup of the current configuration.

Risk: The watchdog can restart local OpenClaw gateway services during health-check failure handling.

Mitigation: Review the script and run it only in an environment where automated gateway restarts are expected.

## Reference(s):

- [Gateway Guardian on ClawHub](https://clawhub.ai/dagangtj/skills/gateway-guardian)
- [dagangtj publisher profile](https://clawhub.ai/user/dagangtj)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill centers on a Bash watchdog script that can restart OpenClaw gateway services and modify local OpenClaw configuration during recovery.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
