## Description: <br>
AI Agents Skills - Query product catalog from fore.vip platform via MCP Server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onsoul](https://clawhub.ai/user/onsoul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to browse and search the fore.vip product catalog through MCP-compatible agents. It supports tag filtering, pagination, product detail display, and links back to fore.vip product pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product search terms, tags, and pagination parameters are sent to the fore.vip API. <br>
Mitigation: Keep queries scoped to catalog browsing and avoid sending secrets, personal data, or sensitive business queries. <br>
Risk: The artifact documents a create_activity endpoint in addition to catalog query behavior. <br>
Mitigation: Require explicit user confirmation before allowing create_activity or any other write-capable MCP action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onsoul/fore-vip-product) <br>
- [fore.vip MCP query endpoint](https://api.fore.vip/mcp/query_kl) <br>
- [fore.vip MCP tools endpoint](https://api.fore.vip/mcp/tools/call) <br>
- [fore.vip product URL pattern](https://fore.vip/p?id={product_id}) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, curl commands, and product catalog response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Product results include pagination metadata, product names, descriptions, images, tags, popularity, update timestamps, and product URLs when returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
