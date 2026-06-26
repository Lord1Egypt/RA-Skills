## Description: <br>
Agent Mailbox lets agents, handlers, and users send, receive, and manage asynchronous messages using local file-based storage with optional sync patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoizceEra](https://clawhub.ai/user/NoizceEra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate asynchronous agent work, delegate tasks, manage replies, and track message history through a local mailbox and CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox messages can trigger automated task handling or outbound callbacks when heartbeat processing is enabled. <br>
Mitigation: Enable cron or heartbeat processing only for trusted mailboxes, review urgent task handling, and remove or allowlist callback URLs before use. <br>
Risk: Mailbox contents may include sensitive operational details and can be exported or synced outside the local machine. <br>
Mitigation: Do not put secrets in messages, review exports before sharing, and treat any cloud sync configuration as data export. <br>
Risk: Agent names are used in local mailbox paths. <br>
Mitigation: Validate or allowlist agent names before accepting them from users or other agents. <br>


## Reference(s): <br>
- [Agent Mailbox ClawHub listing](https://clawhub.ai/NoizceEra/agent-mailbox) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, TypeScript examples, and local message files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local mailbox state and may export mailbox summaries as JSON through the CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
