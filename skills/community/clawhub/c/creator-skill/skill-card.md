## Description: <br>
Creator SKILL helps agents search TikTok, Instagram, and YouTube influencers through the Deinai MCP tools searchInfluencers and get_location_ids. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dachengxiaoai](https://clawhub.ai/user/dachengxiaoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to discover influencers or creators by platform, niche, audience, follower range, language, email availability, and location. It is intended for search and discovery, not creator negotiation, outreach, payments, or campaign management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Deinai MCP token, which is a sensitive credential. <br>
Mitigation: Store the token only in the OpenClaw MCP server configuration, do not place it in skill files or screenshots, and revoke or rotate it if exposed. <br>
Risk: Influencer searches consume Deinai team credits for each influencer record returned. <br>
Mitigation: Use smaller page sizes while testing and confirm the intended platform, query, filters, and location IDs before running broad searches. <br>
Risk: A missing or invalid platform or location can produce irrelevant or failed searches. <br>
Mitigation: Ask the user to choose tiktok, instagram, or youtube when platform is missing, and resolve location names with get_location_ids before calling searchInfluencers. <br>


## Reference(s): <br>
- [Creator SKILL on ClawHub](https://clawhub.ai/dachengxiaoai/creator-skill) <br>
- [Deinai](https://deinai.ai) <br>
- [Deinai MCP endpoint](https://deinai.ai/mcp) <br>
- [MCP token endpoint](https://deinai.ai/api/v1/mcp/tokens) <br>
- [Install and authentication](references/install.md) <br>
- [MCP tools](references/tools.md) <br>
- [Errors and handling](references/errors.md) <br>
- [Tool contract](tool_specs.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, JSON-like tool responses, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results depend on the connected Deinai account, valid MCP token, available team credits, selected platform, query, filters, and page size.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
