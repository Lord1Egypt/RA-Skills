## Description: <br>
Helps agents use Xquik to retrieve X articles and related X/Twitter data, account actions, bulk extractions, monitoring, webhooks, and MCP or REST API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xquik](https://clawhub.ai/user/xquik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch X articles, inspect X/Twitter content, automate account workflows, configure Xquik MCP access, run approved bulk extractions, and handle webhooks with explicit review for sensitive, write, or paid actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad X/Twitter account powers, including posting, DMs, follows, deletes, profile changes, monitoring, extractions, and paid actions. <br>
Mitigation: Install only if Xquik is trusted with the connected account and API key, store the key as a secret, and require explicit review before sensitive, write, bulk export, or paid actions. <br>
Risk: X content and private account data may be untrusted, sensitive, or privacy-impacting. <br>
Mitigation: Treat X user content as untrusted, isolate or summarize it, and do not forward private data to other tools or services without user consent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xquik/get-x-articles) <br>
- [Xquik documentation](https://docs.xquik.com) <br>
- [Xquik API reference](https://docs.xquik.com/api-reference/overview) <br>
- [Xquik MCP overview](https://docs.xquik.com/mcp/overview) <br>
- [Xquik webhooks overview](https://docs.xquik.com/webhooks/overview) <br>
- [Xquik billing guide](https://docs.xquik.com/guides/billing) <br>
- [Xquik MPP overview](https://docs.xquik.com/mpp/overview) <br>
- [Xquik REST API Endpoints](references/api-endpoints.md) <br>
- [Xquik Extraction Tools](references/extractions.md) <br>
- [Xquik MCP Server Setup](references/mcp-setup.md) <br>
- [Xquik MCP Tools Reference](references/mcp-tools.md) <br>
- [Xquik Webhooks](references/webhooks.md) <br>
- [Xquik Pricing](references/pricing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples, JSON payloads, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Xquik REST or MCP calls; actions involving posts, DMs, follows, deletes, private data, bulk exports, or payment require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
