## Description: <br>
General-purpose Coda document manager via REST API v1 for managing docs, tables, rows, pages, automations, and doc structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x7466](https://clawhub.ai/user/0x7466) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to work with Coda workspaces through the REST API, including document discovery, row updates, exports, and automation triggers. It is intended for users who have a Coda API token and appropriate workspace permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Coda API token may expose all docs available to the token holder. <br>
Mitigation: Use a token with only the access you are comfortable delegating, keep it in CODA_API_TOKEN, and do not commit or paste it into shared outputs. <br>
Risk: Delete, publish, or permission-changing actions can modify or expose Coda content. <br>
Mitigation: Review the requested operation and target resource before confirming; use force-style overrides only in controlled automation. <br>
Risk: Exports and row data can contain sensitive workspace information. <br>
Mitigation: Inspect exported JSON, CSV, or table output before sharing it outside the trusted workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0x7466/coda) <br>
- [Coda API Documentation](https://coda.io/developers/apis/v1) <br>
- [Coda OpenAPI Specification](https://coda.io/apis/v1/openapi.yaml) <br>
- [Coda API Rate Limiting](https://coda.io/developers/apis/v1#section/Rate-Limiting) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and CLI output in table, JSON, or CSV form] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CODA_API_TOKEN and network access to the Coda REST API; destructive operations use explicit confirmation unless forced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
