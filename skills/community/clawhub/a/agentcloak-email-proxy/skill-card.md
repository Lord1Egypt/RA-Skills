## Description: <br>
Secure email proxy for AI agents that supports searching, reading, and drafting email through MCP while keeping credentials server-side and filtering PII, prompt injection, 2FA, and password-reset content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanfren](https://clawhub.ai/user/ryanfren) <br>

### License/Terms of Use: <br>
BSL 1.1 <br>


## Use Case: <br>
Developers and agent users use this skill to give an AI agent constrained email access for searching, reading threads, listing labels or drafts, and creating draft replies without sending mail automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an AI agent to mailbox content through AgentCloak or a self-hosted instance. <br>
Mitigation: Use a limited or dedicated mailbox where possible, confirm email access can be revoked, and install only when you are comfortable trusting the selected AgentCloak deployment with mailbox access. <br>
Risk: The hosted service path requires trusting server-side handling of email credentials and content. <br>
Mitigation: Self-host when full control is required, or use the hosted service only after accepting its trust boundary. <br>
Risk: Drafted replies may contain mistakes or unintended sensitive content. <br>
Mitigation: Manually review all drafts before sending; the documented workflow creates drafts rather than sending messages automatically. <br>
Risk: The API key grants access to the configured AgentCloak mailbox proxy. <br>
Mitigation: Protect the API key, rotate it if exposed, and remove or revoke access when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanfren/agentcloak-email-proxy) <br>
- [AgentCloak homepage](https://agentcloak.up.railway.app) <br>
- [AgentCloak GitHub link from skill documentation](https://github.com/ryanfren/AgentCloak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash setup snippets; MCP tool calls return email text, thread data, labels, draft metadata, and draft content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read and draft only; the skill documentation states that agents cannot send, delete, or modify email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
