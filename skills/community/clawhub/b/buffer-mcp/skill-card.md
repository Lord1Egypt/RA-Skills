## Description: <br>
Safely draft, review, inspect, and explicitly approved schedule/publish workflows through Buffer's official MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayhollister](https://clawhub.ai/user/rayhollister) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and social media teams use this skill to configure Buffer MCP and run approval-first workflows for reviewing, drafting, queueing, scheduling, publishing, updating, or deleting Buffer social content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buffer credentials grant delegated access to configured Buffer accounts and channels. <br>
Mitigation: Store credentials in a trusted secret manager or OpenClaw SecretRef, avoid pasting them into chat or plaintext config, and rotate them if exposed. <br>
Risk: Approved Buffer write actions can create, schedule, publish, update, or delete social content. <br>
Mitigation: Require precise approval in the current conversation for the exact account, channel, content, action, and timing before any write action. <br>
Risk: Using an unexpected MCP endpoint could send social content or credentials to an untrusted service. <br>
Mitigation: Use Buffer's official MCP endpoint unless the operator intentionally trusts another server. <br>


## Reference(s): <br>
- [Buffer MCP ClawHub Page](https://clawhub.ai/rayhollister/buffer-mcp) <br>
- [Buffer MCP Homepage](https://forge.rayhollister.com/rayhollister/buffer-mcp) <br>
- [Buffer MCP Server Endpoint](https://mcp.buffer.com/mcp) <br>
- [Buffer MCP Integrations Settings](https://publish.buffer.com/settings/integrations/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with configuration snippets and approval checklist text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instructions-only skill; it does not include executable helper scripts, install-time code, network clients, credential writers, or background automation.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
