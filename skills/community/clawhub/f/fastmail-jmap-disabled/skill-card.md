## Description: <br>
Give your AI agent email superpowers via Fastmail JMAP: read, search, send, move, and trash messages with a zero-dependency Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TassieDaddy](https://clawhub.ai/user/TassieDaddy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to connect an AI agent to Fastmail for inbox checks, email search and reading, message sending, mailbox moves, read-state changes, trashing, and mailbox listing. It is suited to agent email workflows that can be governed with explicit consent around mailbox access and message-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox API tokens can expose sensitive email content and allow message-changing actions. <br>
Mitigation: Use the narrowest Fastmail token scopes that support the intended workflow, store tokens outside prompts and logs, and rotate or revoke tokens when access is no longer needed. <br>
Risk: Send, move, mark-read, mark-unread, and trash commands can alter mailbox state or send messages on behalf of the user. <br>
Mitigation: Require explicit user confirmation before executing message-changing commands, especially sending or deleting email. <br>
Risk: The bundled contacts script can access address-book data if the token includes Contacts scope. <br>
Mitigation: Do not grant Contacts scope unless contact lookup is explicitly required for the deployment. <br>
Risk: Autonomous inbox checks may surface private communications as background monitoring. <br>
Mitigation: Enable background checks only with clear consent, limited query scope, and defined privacy boundaries for summaries and alerts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TassieDaddy/fastmail-jmap-disabled) <br>
- [The Agent Wire](https://theagentwire.ai) <br>
- [Fastmail API Tokens](https://app.fastmail.com/settings/security/tokens) <br>
- [JMAP](https://jmap.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, API Calls, Configuration] <br>
**Output Format:** [CLI text output with optional JSON output for email search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FASTMAIL_TOKEN and optional FASTMAIL_IDENTITY environment variables; scripts call Fastmail JMAP endpoints directly with Python standard library HTTP requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
