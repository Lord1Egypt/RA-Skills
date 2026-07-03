## Description: <br>
Context7 MCP 是一款为开发者提供最新代码文档和示例的服务，通过集成到开发环境中，确保LLM生成的代码基于最新的库文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to resolve library IDs and fetch current Context7-style library documentation and examples before answering coding questions or generating code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The XiaoBenYang API key is stored in a local plaintext .env file. <br>
Mitigation: Keep .env private and gitignored, avoid shared workspaces for unmanaged secrets, or use environment-level secret management. <br>
Risk: API keys and query parameters are sent to the XiaoBenYang service for documentation requests. <br>
Mitigation: Use the skill only when that service is acceptable for the intended documentation queries and avoid sending sensitive project details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/code-document-update) <br>
- [XiaoBenYang API key and service](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown summaries derived from API JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a XiaoBenYang API key; may include library identifiers, documentation excerpts, and code examples returned by the upstream service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
