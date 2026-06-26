## Description: <br>
Baserow API integration with managed API key authentication for managing database rows, fields, and tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to read, create, update, delete, filter, sort, batch-process, and upload files for Baserow data through Maton's managed API-key proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, change, delete, batch-process, and upload data in the connected Baserow account through Maton's proxy. <br>
Mitigation: Use a least-privileged Baserow token and approve writes, deletes, batch operations, and file uploads only after checking the exact target and effect. <br>
Risk: The skill requires MATON_API_KEY and relies on Maton to proxy Baserow requests and manage the connected Baserow credential. <br>
Mitigation: Install only if you trust Maton for this integration, keep MATON_API_KEY secret, and rotate credentials if exposure is suspected. <br>
Risk: Multiple Baserow connections can cause requests to affect the wrong account or workspace. <br>
Mitigation: Specify the intended connection with the Maton-Connection header when relevant and verify the target table, row, or file before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/baserow-api) <br>
- [Maton homepage](https://maton.ai) <br>
- [Baserow API documentation](https://baserow.io/api-docs) <br>
- [Baserow Database API](https://baserow.io/user-docs/database-api) <br>
- [Baserow API spec](https://api.baserow.io/api/redoc/) <br>
- [Baserow database tokens](https://baserow.io/user-docs/personal-api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, API paths, Python snippets, JavaScript snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Maton-managed Baserow connection.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
