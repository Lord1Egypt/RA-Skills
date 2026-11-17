## Description:

ClawSync backs up and restores OpenClaw configuration, including skills, memory, settings, credentials, history, and workspace files, for migration and disaster recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaosusu](https://clawhub.ai/user/zaosusu)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to create backups, migrate setups between machines, restore prior configurations, and share selected configuration components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain credentials or other sensitive OpenClaw data, and the security evidence says advertised encryption does not match the implementation.

Mitigation: Do not rely on the --encrypt option; separately protect backup archives before storing, uploading, or sharing them.

Risk: Restoring an untrusted archive can affect local files because the security evidence flags restore safety as mismatched with the implementation.

Mitigation: Restore only archives from fully trusted sources and update the restore code to validate archive paths and extract only inside the OpenClaw directory.

Risk: The security verdict is suspicious, with a coherent backup purpose but real risk to credentials and local files.

Mitigation: Review and scan the skill before installation or deployment, and treat backup and restore operations as sensitive file-system actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaosusu/skills/clawsync-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/zaosusu)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples and backup archive outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create ZIP backup archives containing OpenClaw configuration data in the user's chosen backup location.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
