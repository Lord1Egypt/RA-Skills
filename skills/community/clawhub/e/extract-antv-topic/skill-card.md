## Description: <br>
Provides AntV documentation context and code examples for AI development and QA workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA practitioners use this skill to route AntV visualization questions, extract topic and intent details, and retrieve relevant documentation, best practices, and code examples from the xiaobenyang MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AntV questions and related project details are sent to a third-party MCP service. <br>
Mitigation: Avoid including proprietary code, secrets, sensitive architecture details, or regulated data in queries. <br>
Risk: The required service API key may be stored in a local plaintext .env file. <br>
Mitigation: Use a dedicated low-privilege API key, review the .env file after use, and remove or rotate the key when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/extract-antv-topic) <br>
- [XiaoBenYang API key portal](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP service endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown summary of API-returned JSON, including code examples when returned by the service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends AntV-related queries to the xiaobenyang MCP service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
