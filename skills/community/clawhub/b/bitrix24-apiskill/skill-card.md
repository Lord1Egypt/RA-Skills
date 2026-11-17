## Description:

Helps agents design, implement, debug, and harden Bitrix24 REST API integrations for CRM, tasks, chats, events, authentication, batching, limits, and REST 3.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vrtalex](https://clawhub.ai/user/vrtalex)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build and operate Bitrix24 agent integrations that call REST APIs, choose webhook or OAuth authentication, automate CRM, tasks, and chats, and handle events and retries with guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can operate with powerful CRM credentials.

Mitigation: Use a test portal first, grant least-privilege scopes, avoid broad packs unless needed, and require explicit confirmation before writes or destructive operations.

Risk: Destination validation may be too weak for production use.

Mitigation: Pin B24_DOMAIN to an approved HTTPS Bitrix24 tenant before allowing live calls.

Risk: Local runtime state can contain business payloads or tokens.

Mitigation: Treat .runtime files as sensitive, restrict local access, and keep them out of source control.

## Reference(s):

- [Bitrix24 REST documentation](https://github.com/bitrix24/b24restdocs)
- [Bitrix24 MCP documentation](https://github.com/bitrix24/b24restdocs/blob/main/sdk/mcp.md)
- [Bitrix24 external AI setup guide](https://helpdesk.bitrix24.com/open/25866707/)
- [Bitrix24 REST load checks](https://helpdesk.bitrix24.com/open/21001036/)
- [Capability Packs](artifact/references/packs.md)
- [Bitrix24 REST for AI Agents](artifact/references/bitrix24.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline code, JSON parameters, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise by default; selects minimal reference packs and requires confirmations for write and destructive actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
