## Description: <br>
Interact with Coda.io docs, tables, rows, pages, and automations via the Coda REST API v1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonfunk](https://clawhub.ai/user/simonfunk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to read, create, update, delete, share, and inspect Coda docs, tables, rows, pages, permissions, automations, and analytics through the Coda REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Coda through the user's API token. <br>
Mitigation: Use the least-privileged token available, keep it out of files, logs, and chat, and rotate it if exposed. <br>
Risk: The helper can change, delete, share, or trigger actions in Coda content. <br>
Mitigation: Manually confirm doc IDs, table IDs, recipient emails, access levels, deletes, and automation triggers before execution. <br>
Risk: Some helper commands build JSON from command arguments. <br>
Mitigation: Avoid untrusted or quote-containing text in those arguments; use stdin JSON or properly encoded curl payloads for complex input. <br>


## Reference(s): <br>
- [Coda API v1 Endpoint Reference](references/api-endpoints.md) <br>
- [Coda REST API v1](https://coda.io/apis/v1) <br>
- [Coda OpenAPI YAML](https://coda.io/apis/v1/openapi.yaml) <br>
- [Coda OpenAPI JSON](https://coda.io/apis/v1/openapi.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/simonfunk/coda-io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CODA_API_TOKEN for authenticated Coda API access.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
