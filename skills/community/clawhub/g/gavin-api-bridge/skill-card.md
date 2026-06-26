## Description: <br>
Generate API integrations from OpenAPI/Swagger specs by scaffolding MCP servers, API clients, and webhook handlers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn API documentation or OpenAPI/Swagger specs into REST integrations, including MCP servers, Python clients, and webhook handlers with authentication, retry, and rate-limit patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated integrations may use real API credentials or OAuth tokens. <br>
Mitigation: Use least-privilege test credentials first, keep secrets out of prompts and source control, and review generated authentication handling before production use. <br>
Risk: Generated MCP servers, clients, or webhook handlers may expose unnecessary write or delete operations. <br>
Mitigation: Review every exposed endpoint and remove operations that are not required for the intended workflow. <br>
Risk: Generated code may call third-party APIs with sensitive payloads or private API specifications. <br>
Mitigation: Avoid pasting secrets or private API specs unless the execution environment and target service are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/gavin-api-bridge) <br>
- [GitHub OpenAPI specification](https://api.github.com/openapi.json) <br>
- [Stripe OpenAPI specification](https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json) <br>
- [Twilio OpenAPI specification](https://github.com/twilio/twilio-oai/blob/main/spec/yaml/twilio_api_v2010.yaml) <br>
- [OpenAI OpenAPI specification](https://github.com/openai/openai-openapi/blob/main/openapi.yaml) <br>
- [Notion OpenAPI specification](https://github.com/makenotion/notion-sdk-js/blob/main/api-openapi.yml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks and generated integration scaffolds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API calls and generated integration scaffolds that require user-supplied credentials.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
