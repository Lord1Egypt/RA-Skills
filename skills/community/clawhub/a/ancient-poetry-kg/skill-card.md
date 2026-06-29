## Description: <br>
Provides a knowledge graph for Chinese ancient poetry, including poem titles, authors, dynasties, and classic phrases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-graph users can use this skill to inspect the Chinese ancient poetry graph schema and run read-only Cypher queries for poetry, author, dynasty, and classic-phrase information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends API keys and graph queries to xiaobenyang.com. <br>
Mitigation: Install only if you trust xiaobenyang.com with those credentials and query contents. <br>
Risk: The skill persists the API key in a local .env file. <br>
Mitigation: Keep the .env file out of source control and shared workspaces. <br>
Risk: Some documentation labels are stale and may not accurately describe the implemented graph-query tools. <br>
Mitigation: Review the implemented tool behavior before relying on the documentation labels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/ancient-poetry-kg) <br>
- [Publisher profile](https://clawhub.ai/user/alinklab) <br>
- [XiaoBenYang API key site](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration instructions, Guidance, Markdown, Text] <br>
**Output Format:** [Markdown or text summaries derived from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value before querying the external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
