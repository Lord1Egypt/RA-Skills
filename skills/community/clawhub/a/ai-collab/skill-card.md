## Description:

Ai Collab helps two OpenClaw agents coordinate parallel work through a shared chat log, daemon inbox, message protocol, and optional Telegram routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremysommerfeld8910-cpu](https://clawhub.ai/user/jeremysommerfeld8910-cpu)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure multi-agent collaboration, including daemon setup, filesystem message passing, shared logs, task handoffs, and optional chat-to-agent routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables persistent multi-agent automation with broad autonomous execution.

Mitigation: Install only when a persistent automation setup is intended; review daemon behavior, cron or watchdog entries, and auto-approval settings before running it.

Risk: Remote chat routing can pass untrusted or unintended messages into the agent inbox.

Mitigation: Restrict Telegram routing to explicit user and group allowlists, keep group privacy and bot permissions under review, and avoid routing untrusted chat content.

Risk: Credential-backed workflows can expose secrets through environment files or logs.

Mitigation: Store credentials with restrictive permissions, avoid logging secrets, and audit chat logs and inbox files for sensitive content.

Risk: Terminal approval through tmux send-keys can approve the wrong prompt or session if misconfigured.

Mitigation: Review the approval script and session targeting before use, avoid blind scheduled keypresses, and require explicit operator confirmation for sensitive actions.

Risk: Financial-action rules allow lower-value actions with limited approval gates.

Mitigation: Tighten financial thresholds and require explicit authorization for any transaction or irreversible financial action before enabling those workflows.

## Reference(s):

- [ai-collab Message Protocol Reference](artifact/references/protocol.md)
- [Telegram Bridge Setup](artifact/references/telegram-bridge.md)
- [Claude to Claude Example](artifact/examples/claude-claude.md)
- [Claude to GPT Example](artifact/examples/claude-gpt.md)
- [Jim Workflow System Prompt Injection](artifact/examples/jim-workflow-prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/jeremysommerfeld8910-cpu/skills/ai-collab)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with bash snippets, protocol examples, configuration values, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs assume a local OpenClaw workspace, shell access, tmux, shared filesystem paths, and configured model or API credentials.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
