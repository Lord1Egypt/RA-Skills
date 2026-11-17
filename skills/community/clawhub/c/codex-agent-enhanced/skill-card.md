## Description:

Codex Agent Enhanced helps OpenClaw users delegate Codex CLI development work by preparing prompts, launching Codex, monitoring progress, handling approvals, checking results, and reporting completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geq1fan](https://clawhub.ai/user/geq1fan)

### License/Terms of Use:


## Use Case:

Developers and project leads using OpenClaw use this skill to coordinate Codex CLI coding tasks, including prompt preparation, task execution, review, iteration, status tracking, and completion reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Codex hooks can send full task output to Telegram, including sensitive project information.

Mitigation: Replace default chat settings with a verified recipient, avoid sending sensitive project output to external chat, and review notification content before using the skill on confidential work.

Risk: Installation can modify ~/.codex/config.toml and add persistent notification behavior.

Mitigation: Back up and review the Codex configuration before adding hooks, and verify the hook path and sender account before enabling the skill.

Risk: Untrusted environment files, long session retention, and cron wakeups can affect cross-session behavior.

Mitigation: Avoid sourcing untrusted .env files, keep state files project-local, and enable cron or long session retention only after reviewing the operational impact.

## Reference(s):

- [Codex Agent Enhanced on ClawHub](https://clawhub.ai/geq1fan/skills/codex-agent-enhanced)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenAI Codex CLI](https://github.com/openai/codex)
- [Codex CLI command reference](references/codex-cli-reference.md)
- [Installation guide](INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, task prompts, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local configuration, project state files, and notification routing when installed and executed by the user.]

## Skill Version(s):

1.0.0-enhanced (source: ClawHub release metadata and CHANGELOG, released 2026-03-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
