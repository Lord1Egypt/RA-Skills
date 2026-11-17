## Description:

沟通偏好工具箱(专业版) helps teams manage shared communication preferences with baselines, version history, cross-device sync, analysis reports, scene switching, and agent-to-agent migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, team leads, and enterprise users use this skill to define, synchronize, analyze, roll back, and migrate communication preferences across teams, devices, scenes, and agent platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage persistent communication preference files and optionally sync them to Git or object-storage remotes.

Mitigation: Review the sync remote, exported files, cleanup actions, and rollback commands before running them.

Risk: Sync and notification features may require credentials or tokens.

Mitigation: Keep tokens in a credential manager or environment variables and do not store secrets in project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/chat-toolkit-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON or YAML configuration examples, and structured status responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose preference file edits, sync or export commands, and configuration changes for review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
