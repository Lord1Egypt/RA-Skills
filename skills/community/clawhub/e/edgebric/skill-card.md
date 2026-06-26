## Description: <br>
Search and manage your private knowledge base. Find documents, query knowledge, upload files, and manage data sources in Edgebric. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerv](https://clawhub.ai/user/jerv) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and employees use this skill to search, query, cite, upload, and manage documents in an Edgebric private knowledge base through its HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording could cause unintended searches of a private knowledge base. <br>
Mitigation: Use the skill only when the user clearly intends Edgebric or private knowledge-base access, and ask for confirmation when the request is ambiguous. <br>
Risk: Write and delete endpoints can change or remove private knowledge-base content when the API key has elevated scope. <br>
Mitigation: Prefer read-only API keys for search workflows and require explicit user confirmation before uploads, source changes, document deletes, or source deletes. <br>


## Reference(s): <br>
- [Edgebric homepage](https://edgebric.com) <br>
- [ClawHub skill page](https://clawhub.ai/jerv/edgebric) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown, Configuration] <br>
**Output Format:** [Markdown text with cited search or query results and HTTP API request guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EDGEBRIC_URL and EDGEBRIC_API_KEY; write operations depend on API key scope and destructive deletes require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.9.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
