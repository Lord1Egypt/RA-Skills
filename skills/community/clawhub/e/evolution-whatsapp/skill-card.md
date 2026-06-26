## Description: <br>
Manage WhatsApp through a configured Evolution API v2 instance by sending messages and media, reading chats and contacts, and administering groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KareemAdelAwwad](https://clawhub.ai/user/KareemAdelAwwad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent interact with WhatsApp through a trusted Evolution API instance for messaging, chat retrieval, contact lookup, and group administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured agent can send messages, read chats and contacts, and change WhatsApp groups through the Evolution API instance. <br>
Mitigation: Install only for a trusted, controlled API instance and require human confirmation before sending messages or changing groups. <br>
Risk: The Evolution instance token grants access to the WhatsApp integration, and the script loads a local .env file when present. <br>
Mitigation: Treat EVO_INSTANCE_TOKEN as a secret, keep any local .env file trusted and uncommitted, and rotate the token if it is exposed. <br>
Risk: Fetching or summarizing chats, contacts, and group data can expose private communications. <br>
Mitigation: Limit agent access to necessary conversations and confirm privacy, consent, and compliance requirements before reading or summarizing chat data. <br>


## Reference(s): <br>
- [Evolution API v2](https://github.com/Atelier23/evolution-api-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and Evolution API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVO_BASE_URL, EVO_INSTANCE_TOKEN, and EVO_INSTANCE_NAME; commands may send, read, and modify WhatsApp data through the configured API instance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
