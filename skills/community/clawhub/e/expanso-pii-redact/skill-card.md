## Description: <br>
Redacts personally identifiable information from text by replacing sensitive data with configurable placeholders using Expanso Edge pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to redact PII from logs, analytics data, and text prepared for public sharing or compliance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unredacted sensitive text may be sent to OpenAI when the remote backend is used. <br>
Mitigation: Install only when policy allows this processing, or configure a local backend for sensitive or regulated data. <br>
Risk: MCP mode can expose a network redaction service using the user's API key. <br>
Mitigation: Bind the service to localhost or add authentication before exposure, and stop the background server after use. <br>
Risk: Deploying the pipeline to a remote Expanso Cloud endpoint can move sensitive processing outside the local environment. <br>
Mitigation: Verify the deployment URL and data-handling policy before deploying remote jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-pii-redact) <br>
- [Publisher profile](https://clawhub.ai/user/aronchick) <br>
- [README.md](README.md) <br>
- [skill.yaml](skill.yaml) <br>
- [pipeline-cli.yaml](pipeline-cli.yaml) <br>
- [pipeline-mcp.yaml](pipeline-mcp.yaml) <br>
- [Expanso](https://expanso.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object with redacted text, redaction count, redacted PII types, and metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports a configurable replacement placeholder and can return results through CLI stdout or an MCP HTTP response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
