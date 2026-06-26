## Description: <br>
Connect directly to any API using its OpenAPI spec with local API key storage, ensuring private, middleware-free requests from your machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[numbpill3d](https://clawhub.ai/user/numbpill3d) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Freeapi to connect to OpenAPI or Swagger services from localhost, manage API keys locally, list available operations, and execute API requests without a middleware service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad API-client power and can make requests against external services. <br>
Mitigation: Inspect the target server and operation before each run, and manually confirm create, update, delete, billing, publishing, or sensitive-data requests. <br>
Risk: API keys are handled locally through a .env file. <br>
Mitigation: Use least-privilege tokens, keep .env out of source control, and rotate credentials if they are exposed. <br>
Risk: Remote OpenAPI specs can direct the client toward unexpected endpoints or operations. <br>
Mitigation: Use official specs and review the resolved operation and parameters before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/numbpill3d/freeapi) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, shell commands, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads OpenAPI or Swagger specs from local paths or URLs and stores configured API keys in a local .env file.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
