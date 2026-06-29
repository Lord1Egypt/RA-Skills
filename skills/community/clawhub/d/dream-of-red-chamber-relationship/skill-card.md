## Description: <br>
关于《红楼梦》人物之间关系的知识图谱。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, researchers, and developers can ask an agent to inspect the Dream of the Red Chamber character relationship graph, retrieve the database schema, and run read-only Cypher queries against the configured service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves the XiaoBenYang API key in a local .env file. <br>
Mitigation: Use it only in workspaces where .env files are not committed or shared, and remove the saved key when it is no longer needed. <br>
Risk: Graph queries are sent to the remote MCP service. <br>
Mitigation: Submit only queries and context you are comfortable sending to the configured external service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/dream-of-red-chamber-relationship) <br>
- [XiaoBenYang API key portal](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown or plain text summaries with JSON-backed results and Cypher query strings when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a XiaoBenYang API key; graph queries are sent to the remote MCP service and the API key may be saved in a local .env file.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
