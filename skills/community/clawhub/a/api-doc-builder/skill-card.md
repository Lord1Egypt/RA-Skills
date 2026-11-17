## Description:

Generate comprehensive API documentation from code with examples, types, and OpenAPI specs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelatamuk](https://clawhub.ai/user/michaelatamuk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API teams use this skill to generate and refresh REST API reference documentation, OpenAPI specifications, examples, and related implementation guidance from local source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional npm or npx integration commands may install or run third-party tooling.

Mitigation: Review commands before execution, pin package versions, and prefer existing project scripts or lockfiles.

Risk: Generated API documentation can be incomplete or misleading if the source code lacks types, validation schemas, or comments.

Mitigation: Review generated docs against the implementation before publishing and add explicit types, validation schemas, or JSDoc where needed.

Risk: Example tokens, API keys, and api.example.com URLs in the documentation could be mistaken for real credentials or endpoints.

Mitigation: Treat these values as placeholders and avoid running examples in environments that contain production credentials.

## Reference(s):

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger Tools](https://swagger.io/tools/)
- [Stoplight](https://stoplight.io/)
- [Google Cloud API Design Guide](https://cloud.google.com/apis/design)
- [REST API Tutorial](https://restfulapi.net/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, OpenAPI YAML or JSON, HTML documentation, Postman collections, and inline command or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documentation should be reviewed against the actual API implementation before publishing.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
