## Description: <br>
Query 28M+ Eurostat COMEXT trade records for EU bilateral flows, HS2-CN8 product codes, and 1988-2025 trade analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, developers, and agent users use this skill to query EU trade data, compare bilateral flows, inspect product-level trends, and research partners, prices, seasonality, and market concentration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends EU trade research queries to a third-party SputnikX service. <br>
Mitigation: Confirm the user is comfortable sharing those queries with SputnikX before using the API or MCP endpoint. <br>
Risk: Some endpoints are marked as paid x402 requests. <br>
Mitigation: Check agent and wallet payment controls before calling endpoints marked as $0.10 x402. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drivenbymyai-max/eu-trade-analytics) <br>
- [SputnikX homepage](https://sputnikx.xyz) <br>
- [SputnikX agent API base URL](https://sputnikx.xyz/api/v1/agent) <br>
- [SputnikX MCP endpoint](https://mcp.sputnikx.xyz/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, text] <br>
**Output Format:** [Markdown with curl examples and endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes free and paid endpoint examples for querying EU trade analytics through SputnikX APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
