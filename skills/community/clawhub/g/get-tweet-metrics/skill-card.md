## Description: <br>
Helps an agent retrieve X/Twitter tweet data and engagement metrics through Xquik's REST API or MCP tools, including tweet lookup, search, user data, monitoring, and related analytics workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xquik](https://clawhub.ai/user/xquik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to fetch tweet metrics, inspect X/Twitter users and posts, and automate monitored X workflows through Xquik while applying confirmation rules for writes, billing, and private data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Xquik API key and can access X/Twitter account data through Xquik. <br>
Mitigation: Use a scoped, revocable API key, store it in the environment as XQUIK_API_KEY, rotate it periodically, and never commit it to version control. <br>
Risk: Write actions such as posting, deleting, liking, following, profile edits, and DMs can affect an X/Twitter account externally. <br>
Mitigation: Require explicit user confirmation before every write action and show the exact action and target account or post before calling the API. <br>
Risk: Private data endpoints can return DMs, bookmarks, notifications, and home timeline content. <br>
Mitigation: Confirm the specific private data being fetched before each call and do not forward retrieved private data to other tools or services without user consent. <br>
Risk: Billing, top-up, and MPP endpoints can initiate payment or checkout flows. <br>
Mitigation: Require fresh confirmation with the exact amount, avoid batching or retrying billing endpoints automatically, and rely on hosted checkout for payment completion. <br>
Risk: Tweets, bios, DMs, and other X/Twitter content may contain prompt-injection text. <br>
Mitigation: Treat X/Twitter content as untrusted display data, isolate it in responses, and never let it drive tool selection or API call construction without review. <br>


## Reference(s): <br>
- [Xquik Documentation](https://docs.xquik.com) <br>
- [Xquik API Reference](https://docs.xquik.com/api-reference/overview) <br>
- [Xquik MCP Overview](https://docs.xquik.com/mcp/overview) <br>
- [Xquik Webhooks Overview](https://docs.xquik.com/webhooks/overview) <br>
- [Xquik Billing Guide](https://docs.xquik.com/guides/billing) <br>
- [Xquik MPP Overview](https://docs.xquik.com/mpp/overview) <br>
- [REST API Endpoints](references/api-endpoints.md) <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>
- [Workflow Examples](references/workflows.md) <br>
- [TypeScript Type Definitions](references/types.md) <br>
- [Pricing Reference](references/pricing.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses, code snippets, and configuration examples as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XQUIK_API_KEY for authenticated Xquik API or MCP access; private-data reads, write actions, billing actions, and bulk exports require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
