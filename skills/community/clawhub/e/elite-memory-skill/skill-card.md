## Description:

Elite Memory is an OpenClaw memory-management skill for daily and long-term Markdown memory, GitHub synchronization, and optional Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renguanjie](https://clawhub.ai/user/renguanjie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep structured daily and long-term memory files, archive prior-day notes, and synchronize memory state to an external Git remote with optional Feishu status notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive conversations, decisions, and project context in local memory files.

Mitigation: Review memory contents before use, avoid storing secrets or sensitive conversations, and remove entries that should not be retained.

Risk: Automatic Git synchronization can upload more workspace data than users reasonably expect.

Mitigation: Do not enable the cron sync until synchronization is narrowed to explicit memory paths; keep the remote private and verify the remote URL before pushing.

Risk: Optional Feishu notifications and external Git remotes can disclose memory status or content outside the local workspace.

Mitigation: Configure `FEISHU_USER_ID` only when notifications are needed, and review the notification and Git remote configuration before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renguanjie/skills/elite-memory-skill)
- [Skill-provided project homepage](https://github.com/renguanjie/ai-memory)
- [Skill-provided OpenClaw memory documentation](https://docs.openclaw.ai/memory)
- [Daily memory template](artifact/templates/daily-memory.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates workspace memory files, logs synchronization status, and may send Feishu notifications when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
