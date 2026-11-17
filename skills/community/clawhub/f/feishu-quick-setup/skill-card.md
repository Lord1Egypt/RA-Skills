## Description:

Creates a new Feishu bot through the Feishu App Registration Device Flow and saves its app ID and app secret to the OpenClaw configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hashstacs-hk](https://clawhub.ai/user/hashstacs-hk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create a Feishu or Lark bot, guide the user through authorization, and store the resulting credentials for Feishu channel setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores long-lived Feishu app secrets locally, which can expose credentials on shared or weakly protected machines.

Mitigation: Use it only on a trusted single-user machine or tighten local file permissions before setup.

Risk: App secrets may be exposed if copied into command history, terminal logs, or shared support output.

Mitigation: Avoid sharing command logs that contain credentials and rotate the Feishu app secret if exposure is possible.

Risk: Granting broad Feishu document, drive, calendar, or contact permissions can expand access beyond the user's need.

Mitigation: After setup, verify Feishu permissions manually and enable only the scopes required for the intended OpenClaw workflows.

## Reference(s):

- [Feishu permissions guide](references/feishu-permissions.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Feishu Open Platform](https://open.feishu.cn)
- [ClawHub skill page](https://clawhub.ai/hashstacs-hk/skills/feishu-quick-setup)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and single-line JSON script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenClaw Feishu configuration and a local backup file.]

## Skill Version(s):

1.0.2 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
