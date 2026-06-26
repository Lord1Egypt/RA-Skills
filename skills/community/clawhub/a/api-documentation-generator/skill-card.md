## Description: <br>
Generate comprehensive API documentation from code, extracting endpoints, parameters, response schemas, and examples from Express, FastAPI, Django, Rails, and similar frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect API source code and produce human-readable API references, OpenAPI specifications, request examples, and documentation coverage summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated API documentation can expose endpoint details, authentication behavior, examples, or other sensitive implementation information. <br>
Mitigation: Install only for repositories where agent source-code access is acceptable, and review generated documentation before publishing. <br>
Risk: Providing API keys, cookies, OAuth tokens, or other credentials to the skill can expose sensitive secrets unnecessarily. <br>
Mitigation: Do not provide sensitive credentials unless a separate trusted workflow explicitly requires them. <br>
Risk: Generated endpoint schemas, examples, or coverage summaries may be incomplete or inaccurate when source code lacks annotations or uses dynamic request handling. <br>
Mitigation: Validate generated OpenAPI and Markdown outputs against the application behavior before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/api-documentation-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API reference sections, OpenAPI YAML, JSON examples, curl examples, and documentation coverage summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose generated files such as docs/api-reference.md, docs/openapi.yaml, and endpoint example directories.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
