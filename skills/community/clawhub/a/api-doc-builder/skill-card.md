## Description: <br>
Generate comprehensive API documentation from code with examples, types, and OpenAPI specs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelatamuk](https://clawhub.ai/user/michaelatamuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft REST API reference documentation, OpenAPI specifications, request and response examples, authentication notes, and client usage snippets from local source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example authentication patterns could be confused with a request for real API keys or OAuth tokens. <br>
Mitigation: Do not provide real credentials; use placeholders or sanitized examples when asking the skill to document authentication. <br>
Risk: Generated API documentation or OpenAPI specs may omit behavior or describe code inaccurately. <br>
Mitigation: Review generated Markdown and OpenAPI output against the actual implementation before publishing or using it for SDK generation, contract tests, or gateway configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/michaelatamuk/api-doc-builder) <br>
- [OpenAPI Specification](https://swagger.io/specification/) <br>
- [Swagger Tools](https://swagger.io/tools/) <br>
- [Stoplight](https://stoplight.io/) <br>
- [Google Cloud API Design Guide](https://cloud.google.com/apis/design) <br>
- [REST API Tutorial](https://restfulapi.net/) <br>
- [Redoc](https://github.com/Redocly/redoc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and OpenAPI YAML or JSON with code blocks and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint tables, schemas, request and response examples, authentication notes, rate limit guidance, client snippets, and tool integration commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
