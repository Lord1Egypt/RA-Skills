## Description:

Provides a seven-step emergency workflow for Xianyu account-ban events, covering ban detection, service pausing, administrator notification, backup-account switching, item recovery, appeal preparation, and post-incident analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and automation maintainers use this skill to respond to Xianyu account bans by stopping affected automation, switching to backup accounts, coordinating item recovery and appeals, and recording post-incident analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent operational account changes, including pausing services and switching account mappings.

Mitigation: Require operator approval before switch, publish, and appeal steps, and limit execution to accounts and tenants authorized for emergency recovery.

Risk: Incident logging may include account identifiers and ban reasons, including cross-skill self-growth logging.

Mitigation: Disclose the logging behavior before installation, and disable or scope cross-skill logging when identifiers or ban reasons should remain local to this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/account-ban-emergency)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return structured JSON status objects from helper scripts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
