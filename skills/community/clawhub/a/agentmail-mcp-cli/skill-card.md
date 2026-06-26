## Description: <br>
Manage AI agent email accounts via AgentMail API, including inbox creation, email send/receive/reply workflows, threads, labels, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FloHiwg](https://clawhub.ai/user/FloHiwg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to AgentMail inboxes, inspect threads, send or reply to messages, update labels, and retrieve attachment details through the AgentMail CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email operations can expose private message bodies, recipient data, and attachment URLs. <br>
Mitigation: Use a dedicated AgentMail API key where possible, avoid logging sensitive email or attachment content, and keep AGENTMAIL_API_KEY in the environment rather than command-line arguments. <br>
Risk: Sending, forwarding, reply-all, auto-reply, and inbox deletion actions can create external side effects. <br>
Mitigation: Require human approval before those actions and review recipients, message content, and destructive inbox operations before execution. <br>


## Reference(s): <br>
- [AgentMail homepage](https://agentmail.to) <br>
- [AgentMail documentation](https://docs.agentmail.to) <br>
- [AgentMail CLI repository](https://github.com/FloHiwg/agentmail-cli) <br>
- [ClawHub skill page](https://clawhub.ai/FloHiwg/agentmail-mcp-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI arguments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, the agentmail CLI, and AGENTMAIL_API_KEY for authenticated AgentMail API access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
