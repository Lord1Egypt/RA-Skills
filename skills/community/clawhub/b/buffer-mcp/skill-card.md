## Description:

Safely draft, review, inspect, and explicitly approved schedule/publish workflows through Buffer's official MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rayhollister](https://clawhub.ai/user/rayhollister)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and social media teams use this skill to configure Buffer MCP and follow an approval-first workflow for drafting, queuing, scheduling, publishing, updating, or deleting Buffer social content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Buffer credentials can grant delegated access to social publishing workflows.

Mitigation: Store credentials in a secret store or SecretRef, do not paste them into chat or plaintext configuration, and rotate them if exposed.

Risk: Buffer write tools can create, schedule, publish, update, or delete public or scheduled social content.

Mitigation: Require explicit current-conversation approval for the exact account, channel, action, content, timing, and immediate-publication status before any write.

Risk: Buffer API rate limits can be consumed quickly by agent-driven workflows.

Mitigation: Use read/list calls deliberately and verify target accounts, organizations, and channels before performing write workflows.

## Reference(s):

- [Buffer MCP ClawHub Skill Page](https://clawhub.ai/rayhollister/skills/buffer-mcp)
- [Buffer MCP Source Homepage](https://forge.rayhollister.com/rayhollister/buffer-mcp)
- [Buffer MCP Endpoint](https://mcp.buffer.com/mcp)
- [Buffer MCP Integrations Settings](https://publish.buffer.com/settings/integrations/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with configuration values and approval checklist text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable helper scripts, install-time code, network clients, credential writers, or background automation are included.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
