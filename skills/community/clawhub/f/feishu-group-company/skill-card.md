## Description:

Configures a Feishu multi-bot company group so one coordinator bot handles ordinary messages while specialist bots reply only when explicitly mentioned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-shen1121](https://clawhub.ai/user/alex-shen1121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to configure or repair OpenClaw Feishu company groups where a default coordinator bot should answer normal group messages and specialist bots should answer only direct mentions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included script can persistently set the target Feishu group policy to open in OpenClaw.

Mitigation: Review the policy change before use, run the script with --dry-run first, create a backup, and confirm that groupPolicy: open is intended for the target group.

## Reference(s):

- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/alex-shen1121/skills/feishu-group-company)
- [Publisher profile](https://clawhub.ai/user/alex-shen1121)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with Python script usage and JSON configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a reusable script that can dry-run or persist changes to an OpenClaw configuration file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
