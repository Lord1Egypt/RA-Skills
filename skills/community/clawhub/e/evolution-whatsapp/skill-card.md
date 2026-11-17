## Description:

Evolution WhatsApp helps an agent control WhatsApp through Evolution API v2, including sending messages and media, managing groups, fetching chats and contacts, and summarizing conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kareemadelawwad](https://clawhub.ai/user/kareemadelawwad)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent interact with WhatsApp accounts through a configured Evolution API instance for messaging, chat retrieval, contact lookup, group administration, and conversation summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and summarize sensitive chats, contacts, group data, and locations.

Mitigation: Use it only with accounts and conversations where you have authorization and consent, and avoid processing data that should not be exposed to an agent.

Risk: The skill depends on an Evolution API endpoint and token that can control WhatsApp actions.

Mitigation: Use a trusted HTTPS endpoint, store a limited and rotatable token outside shared artifacts, and rotate credentials if exposure is suspected.

Risk: The shell wrapper loads a local artifact .env file if present, which could execute shell content.

Mitigation: Do not place executable content in artifact/.env; review local configuration files before running the wrapper.

## Reference(s):

- [Evolution API v2](https://github.com/Atelier23/evolution-api-v2)
- [ClawHub Skill Page](https://clawhub.ai/kareemadelawwad/skills/evolution-whatsapp)
- [Publisher Profile](https://clawhub.ai/user/kareemadelawwad)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EVO_BASE_URL, EVO_INSTANCE_TOKEN, and EVO_INSTANCE_NAME to be configured before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
