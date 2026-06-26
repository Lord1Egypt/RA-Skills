## Description: <br>
Integrate AI agents with Bitrix24 REST API to automate CRM, tasks, chats, event processing, auth selection, and API error troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vrtalex](https://clawhub.ai/user/vrtalex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and integration engineers use this skill to design, implement, debug, and harden Bitrix24 REST integrations for CRM, tasks, chats, events, authentication, and API troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent access and modify real Bitrix24 account data. <br>
Mitigation: Install it only for intended Bitrix24 automation, use least-privilege webhook or OAuth scopes, and require review before write or destructive operations. <br>
Risk: Webhook URLs, OAuth tokens, client secrets, and local runtime files can expose account access or operational history if mishandled. <br>
Mitigation: Keep secrets out of chat and source control, leave secret masking enabled, and protect or rotate .runtime audit, retry, idempotency, and DLQ files. <br>
Risk: Using --allow-unlisted or broad packs can permit methods beyond the normal allowlist. <br>
Mitigation: Use --allow-unlisted only for controlled testing, prefer narrow packs, and extend allowlists deliberately after verification. <br>
Risk: The offline event worker clears events after processing, so misconfiguration can cause missed or unrecoverable event handling. <br>
Mitigation: Test the offline worker on a non-production portal first, validate application tokens for inbound events, and review retry and DLQ behavior before production use. <br>


## Reference(s): <br>
- [Bitrix24 Skill on ClawHub](https://clawhub.ai/vrtalex/bitrix24-apiskill) <br>
- [Publisher Profile](https://clawhub.ai/user/vrtalex) <br>
- [Bitrix24 REST for AI Agents](references/bitrix24.md) <br>
- [Capability Packs](references/packs.md) <br>
- [Bitrix24 REST Documentation](https://github.com/bitrix24/b24restdocs) <br>
- [Bitrix24 MCP Documentation](https://github.com/bitrix24/b24restdocs/blob/main/sdk/mcp.md) <br>
- [Bitrix24 External AI Connections](https://helpdesk.bitrix24.com/open/25866707/) <br>
- [Bitrix24 Developer Resources Setup](https://helpdesk.bitrix24.com/open/21133100/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise agent-facing responses; may include Bitrix24 REST method names, pack selections, allowlist choices, and command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
