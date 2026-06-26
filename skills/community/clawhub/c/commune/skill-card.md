## Description: <br>
Creates and manages a persistent agent-only email inbox for sending, receiving, searching, tagging, webhook handling, and structured extraction of email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanjairaj7](https://clawhub.ai/user/shanjairaj7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to give an agent a dedicated email inbox, automate outbound and inbound email workflows, search prior conversations, and triage threads across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent persistent authority to read, send, search, and process email. <br>
Mitigation: Use a dedicated low-privilege API key and inbox, restrict API scopes where possible, and require human approval for outbound messages and attachments. <br>
Risk: Email contents, attachments, and extracted data may include sensitive or regulated information. <br>
Mitigation: Avoid routing sensitive or regulated email unless Commune processing, retention, and access controls have been reviewed for the intended environment. <br>
Risk: Credential files can expose API keys if stored in shared or plaintext locations. <br>
Mitigation: Prefer environment-managed secrets or protected credential files with restrictive permissions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shanjairaj7/commune) <br>
- [Publisher profile](https://clawhub.ai/user/shanjairaj7) <br>
- [Commune documentation](https://commune.email/docs) <br>
- [Commune website](https://commune.email) <br>
- [API reference](references/api.md) <br>
- [Installation guide](INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Commune API key and may call external Commune email APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
