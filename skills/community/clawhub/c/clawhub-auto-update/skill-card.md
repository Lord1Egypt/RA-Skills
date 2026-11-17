## Description:

自动检查并更新ClawHub已安装技能。有更新时通知用户，支持手动和定时运行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmieting](https://clawhub.ai/user/jimmieting)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to check installed ClawHub skills for updates and run bulk updates manually or on a cron schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update all installed ClawHub skills through an unpinned command.

Mitigation: Review updates before installation, pin the clawhub CLI version where possible, and keep a rollback path for local skill state.

Risk: The documented cron setup can run bulk updates unattended.

Mitigation: Prefer manual runs unless the environment has separate review, backup, logging, and rollback processes.

Risk: Updates may overwrite local skill changes.

Mitigation: Back up local skill modifications and important configuration before running bulk updates.

## Reference(s):

- [ClawHub Auto Update release page](https://clawhub.ai/jimmieting/skills/clawhub-auto-update)
- [jimmieting publisher profile](https://clawhub.ai/user/jimmieting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and shell output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write update logs under ~/.openclaw/logs when the generated shell workflow is run.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
