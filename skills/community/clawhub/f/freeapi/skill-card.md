## Description:

Freeapi lets an agent load an OpenAPI or Swagger specification and execute API operations directly from the local machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[numbpill3d](https://clawhub.ai/user/numbpill3d)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Freeapi to connect local agents to APIs from OpenAPI specifications, list available operations, run selected endpoints, and manage local API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys and can expose them through untrusted OpenAPI specifications, local files, or unintended network destinations.

Mitigation: Use only trusted OpenAPI specifications and API servers, keep tokens narrowly scoped, avoid storing valuable credentials in project .env files, and revoke any credential used with an untrusted spec.

Risk: The skill executes requests based on server URLs and operations described by the selected OpenAPI specification.

Mitigation: Review the specification source, target server, operation, parameters, and request body before execution, especially when using credentials with write access.

## Reference(s):

- [Freeapi ClawHub skill page](https://clawhub.ai/numbpill3d/skills/freeapi)
- [numbpill3d ClawHub publisher profile](https://clawhub.ai/user/numbpill3d)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read OpenAPI specifications from local files or URLs, store service credentials in a local .env file, and execute network requests to API servers defined by the selected specification.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
