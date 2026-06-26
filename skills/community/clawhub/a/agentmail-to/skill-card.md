## Description: <br>
Agentmail To helps agents create, read, send, and manage temporary AgentMail email inboxes through the AgentMail API or web console. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjotrglushkov-byte](https://clawhub.ai/user/pjotrglushkov-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to provision temporary email addresses, inspect incoming messages, reply through AgentMail, and clean up test inboxes during workflows that require email verification or mailbox automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags published AgentMail credential material and a shared inbox. <br>
Mitigation: Use your own AgentMail credentials, rotate the embedded key if it belongs to you, and avoid reusing the shared inbox. <br>
Risk: The release evidence says the skill points agents at unreviewed local scripts for sensitive mail actions. <br>
Mitigation: Inspect any referenced local scripts before running them and require explicit confirmation before sending mail, reading verification codes, or deleting inboxes. <br>
Risk: Temporary inbox workflows can expose sensitive or account-recovery messages. <br>
Mitigation: Do not use temporary inboxes for confidential data or long-lived accounts; delete unused inboxes when workflows finish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pjotrglushkov-byte/agentmail-to) <br>
- [AgentMail](https://agentmail.to) <br>
- [AgentMail quickstart](https://docs.agentmail.to/quickstart) <br>
- [AgentMail documentation](https://agentmail.to/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, curl, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment-variable configuration guidance and API-oriented mailbox commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
