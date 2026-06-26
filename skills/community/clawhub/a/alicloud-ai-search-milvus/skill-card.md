## Description: <br>
Use AliCloud Milvus (serverless) with PyMilvus to create collections, insert vectors, and run filtered similarity search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent workflow to Alibaba Cloud Milvus, create vector collections, insert embeddings, and run filtered similarity searches for retrieval tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use credentials to create collections, insert vectors, and query a Milvus instance. <br>
Mitigation: Use a least-privilege token, confirm the target database and collection, and test against a non-production collection before production use. <br>
Risk: Saved evidence or command output may include sensitive search results or operational details. <br>
Mitigation: Avoid saving secrets or sensitive results in the output evidence directory, and redact outputs before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-search-milvus) <br>
- [Source list](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Milvus API responses and local evidence files when the user runs the quickstart or validation workflow.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
