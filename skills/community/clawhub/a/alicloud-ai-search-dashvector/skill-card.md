## Description: <br>
Build vector retrieval with Alibaba Cloud DashVector using the Python SDK for collection creation, document upserts, and filtered similarity search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure DashVector access, create vector collections, upsert documents, and run scoped similarity searches from Claude Code or Codex workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DashVector operations can create collections and upsert documents in the configured cluster. <br>
Mitigation: Confirm the endpoint, collection name, and intended scope before running mutating actions, and test first against a non-production or intended collection. <br>
Risk: Credentials and uploaded vectors or document fields may expose sensitive data if handled carelessly. <br>
Mitigation: Use a scoped DashVector API key and upload only data approved for storage in the target DashVector cluster. <br>
Risk: Unpinned SDK installation can change behavior across environments. <br>
Mitigation: Consider pinning the dashvector package version for production use. <br>


## Reference(s): <br>
- [Source list](artifact/references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-search-dashvector) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHVECTOR_API_KEY and DASHVECTOR_ENDPOINT; operations can create collections, upsert documents, and query DashVector.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
