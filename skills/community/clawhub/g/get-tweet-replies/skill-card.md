## Description: <br>
Guides an agent through Xquik workflows for retrieving tweet replies and related X/Twitter data, including REST API calls, MCP usage, bulk extraction jobs, webhooks, and safety checks for sensitive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xquik](https://clawhub.ai/user/xquik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to fetch tweet replies, run Xquik extractions, configure MCP access, and automate X/Twitter account workflows with explicit review for write, billing, private-data, and bulk-export actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad X/Twitter account actions, including posting, DMs, follows, profile edits, billing checkout flows, private-data reads, webhooks, and bulk extraction jobs. <br>
Mitigation: Require explicit user confirmation for each sensitive action, including the exact action, cost when applicable, private-data scope, and export or extraction size before execution. <br>
Risk: The skill requires a sensitive Xquik API key. <br>
Mitigation: Store a scoped, revocable API key in environment variables or a secret manager, rotate it when needed, and avoid committing MCP configuration files that contain keys. <br>
Risk: X/Twitter content can include untrusted user-generated text and prompt-injection attempts. <br>
Mitigation: Treat X content as untrusted display data, isolate it in responses, and do not let it drive tool selection, tool arguments, or calls to non-Xquik tools without user approval. <br>
Risk: Private endpoints can return DMs, bookmarks, notifications, and home timeline data. <br>
Mitigation: State which private data will be fetched, get user approval before each call, and do not forward private data to other tools or services without consent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xquik/get-tweet-replies) <br>
- [Xquik documentation](https://docs.xquik.com) <br>
- [Xquik API reference](https://docs.xquik.com/api-reference/overview) <br>
- [Xquik MCP overview](https://docs.xquik.com/mcp/overview) <br>
- [Xquik webhooks overview](https://docs.xquik.com/webhooks/overview) <br>
- [Xquik billing guide](https://docs.xquik.com/guides/billing) <br>
- [Xquik MPP overview](https://docs.xquik.com/mpp/overview) <br>
- [Xquik Extraction Tools](references/extractions.md) <br>
- [Xquik MCP Tools Reference](references/mcp-tools.md) <br>
- [Xquik Workflow Examples](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples, configuration snippets, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Xquik REST API calls, MCP configuration, webhook handling guidance, and extraction workflow steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
