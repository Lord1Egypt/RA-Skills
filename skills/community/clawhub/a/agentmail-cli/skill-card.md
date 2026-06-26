## Description: <br>
Manage email inboxes and messages via AgentMail API. Create disposable inboxes, send/receive emails, and list messages. Use when the agent needs to send or receive email, create temporary inboxes, or check for incoming messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stepandel](https://clawhub.ai/user/stepandel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to configure the AgentMail CLI, create disposable inboxes, send messages, list and read incoming messages, and delete inboxes or message threads through the AgentMail API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an AgentMail API key, which can authorize email operations. <br>
Mitigation: Prefer AGENTMAIL_API_KEY for short-lived sessions and protect or remove ~/.agentmail/config.json when using persistent setup. <br>
Risk: The skill can send email and read incoming messages through the AgentMail CLI. <br>
Mitigation: Review recipients, message contents, and inbox identifiers before executing email commands. <br>
Risk: Deleting an inbox or message can remove inbox data or an entire message thread. <br>
Mitigation: Require explicit confirmation before deleting inboxes or messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stepandel/agentmail-cli) <br>
- [AgentMail](https://agentmail.to) <br>
- [agentmail-cli homepage](https://github.com/stepandel/agentmail-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands generally use --json for machine-readable output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
