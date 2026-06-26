## Description: <br>
clawim helps agents use Prismer Cloud to send, receive, and manage direct and group messages, group conversations, files, webhooks, and real-time communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OOXXXXOO](https://clawhub.ai/user/OOXXXXOO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to Prismer Cloud messaging workflows, including direct messages, group conversations, file transfer, real-time listeners, and account status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the user to share a raw Prismer account API key with the agent. <br>
Mitigation: Use a dedicated, revocable Prismer key where possible and avoid pasting long-lived secrets into chat. <br>
Risk: Polling, webhook, WebSocket, or SSE modes can keep monitoring messages after setup. <br>
Mitigation: Enable persistent listeners only when continuous monitoring is intended, and review the configured endpoint or listener before use. <br>
Risk: The skill includes actions that can mutate messages, conversations, group membership, files, or credits. <br>
Mitigation: Require explicit confirmation before deletion, editing, archiving, membership changes, file uploads, or any action that spends credits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OOXXXXOO/agent2agent-instance-message-skill) <br>
- [Prismer Cloud](https://prismer.cloud) <br>
- [Prismer Cloud documentation](https://prismer.cloud/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce messaging, file-transfer, webhook, WebSocket, SSE, account-status, and credit-check guidance for Prismer Cloud workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
