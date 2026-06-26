## Description: <br>
Multi-agent autonomous collaboration system for two OpenClaw agents working in parallel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremysommerfeld8910-cpu](https://clawhub.ai/user/jeremysommerfeld8910-cpu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up two OpenClaw agents that coordinate work through a shared inbox, chat log, daemon process, and message protocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent daemon agents may continue acting beyond the user's immediate attention. <br>
Mitigation: Run the daemon only when needed, monitor the shared chat log, and stop the tmux session or daemon process after the collaboration task completes. <br>
Risk: Inbox files and chat logs can expose task content, credentials, or other sensitive context. <br>
Mitigation: Restrict filesystem permissions on the collaboration directory, keep secrets out of logs, and store credentials only in protected environment files. <br>
Risk: Blind tmux approval forwarding can approve the wrong prompt or session. <br>
Mitigation: Avoid unattended approval forwarding and confirm the target session and requested action before sending approval input. <br>
Risk: Telegram, OpenAI, and Claude integrations can share local task content with external services. <br>
Mitigation: Enable external bridges only with explicit consent, whitelist authorized users, and review what data is routed to each service. <br>
Risk: The artifact includes a financial action protocol with weak boundaries for low-dollar actions. <br>
Mitigation: Remove or disable financial workflows unless they are explicitly required, and require human authorization for any financial action. <br>


## Reference(s): <br>
- [ai-collab Message Protocol Reference](references/protocol.md) <br>
- [Telegram Bridge Setup](references/telegram-bridge.md) <br>
- [Claude to Claude Example](examples/claude-claude.md) <br>
- [Claude to GPT Example](examples/claude-gpt.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jeremysommerfeld8910-cpu/ai-collab) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Code] <br>
**Output Format:** [Markdown with bash commands, configuration snippets, and protocol examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scripts for daemon messaging, chat log polling, inbox dispatch, and tmux approval forwarding.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
