## Description: <br>
Connects agents to 100+ third-party APIs through Maton-managed OAuth gateway access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyuechuimeng](https://clawhub.ai/user/xiyuechuimeng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to call native endpoints for connected third-party services and manage Maton OAuth connections from agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call many third-party services through brokered access, so connected OAuth scopes may permit broad read or write operations. <br>
Mitigation: Install only if you trust Maton and review each service's OAuth scopes before authorizing a connection. <br>
Risk: Example calls include mutations such as posting messages or creating contacts if placeholders are reused against real services. <br>
Mitigation: Replace placeholders, test against non-production resources when possible, and review requests before running write operations. <br>
Risk: Unused or stale connections can continue to grant access through the gateway. <br>
Mitigation: Delete unused Maton connections and rotate or revoke access when workflows no longer need a service. <br>


## Reference(s): <br>
- [Maton Homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>
- [Slack Gateway Reference](references/slack/README.md) <br>
- [Google Mail Gateway Reference](references/google-mail/README.md) <br>
- [Notion MCP Reference](references/notion-mcp/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, JavaScript, curl, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; requests act only through user-authorized Maton connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
