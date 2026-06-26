## Description: <br>
Query any public GitHub repository using DeepWiki's AI-powered documentation and Q&A service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to ask natural-language questions about public GitHub repositories, list DeepWiki documentation topics, or fetch indexed wiki contents when investigating source code, architecture, configuration, or internals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository names and user questions are sent to DeepWiki's external MCP service. <br>
Mitigation: Avoid sending secrets, private code, internal system details, customer data, or confidential repository names, and invoke the skill only when DeepWiki lookup is intended. <br>
Risk: DeepWiki may lag behind the latest repository commits or return incomplete generated answers. <br>
Mitigation: Use targeted questions, retry or narrow follow-up queries when needed, and verify time-sensitive answers against the repository source before relying on them. <br>
Risk: Fetching full wiki contents can produce large outputs. <br>
Mitigation: Prefer the ask action for targeted questions and use topics before requesting full docs. <br>


## Reference(s): <br>
- [ClawHub DeepWiki MCP release](https://clawhub.ai/chunhualiao/deepwiki-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/chunhualiao) <br>
- [DeepWiki](https://deepwiki.com) <br>
- [DeepWiki MCP endpoint](https://mcp.deepwiki.com/mcp) <br>
- [DeepWiki MCP documentation](https://docs.devin.ai/work-with-devin/deepwiki-mcp) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text answers from DeepWiki, with optional shell command examples for helper-script usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository file references, documentation topic lists, or full wiki contents returned by the external DeepWiki MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release, skill.yml, CHANGELOG released 2026-02-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
