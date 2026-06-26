## Description: <br>
Use when building vector retrieval with DashVector using the Python SDK, including creating collections, upserting documents, and running similarity search with filters in Claude Code or Codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent workflow to Alibaba Cloud DashVector, create vector collections, upsert records, and run filtered similarity searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform mutating DashVector operations such as creating collections and upserting documents. <br>
Mitigation: Confirm user intent, target collection, region, and operation scope before making changes; run a minimal read-only connectivity check first. <br>
Risk: The workflow depends on DashVector credentials and endpoint configuration. <br>
Mitigation: Use environment variables for credentials, avoid recording secrets in evidence, and save only parameter summaries and non-sensitive API results. <br>
Risk: Similarity search quality depends on matching collection dimensions and embedding model output size. <br>
Mitigation: Validate collection dimension and schema before upsert or query, and handle dimension mismatch errors before continuing. <br>


## Reference(s): <br>
- [Source list](artifact/references/sources.md) <br>
- [Aliyun Dashvector Search on ClawHub](https://clawhub.ai/cinience/aliyun-dashvector-search) <br>
- [cinience publisher profile](https://clawhub.ai/user/cinience) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python examples, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DashVector API response summaries and local evidence files when the workflow is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
