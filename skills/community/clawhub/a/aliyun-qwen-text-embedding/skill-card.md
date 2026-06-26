## Description: <br>
Use when text embeddings are needed from Alibaba Cloud Model Studio models for semantic search, retrieval-augmented generation, clustering, or offline vectorization pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Alibaba Cloud Model Studio text-embedding requests for semantic search, retrieval-augmented generation, clustering, and offline vectorization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A selected embedding model may not match the Alibaba Cloud API version used by the downstream client. <br>
Mitigation: Confirm the model name against the intended Model Studio API version before sending prepared requests. <br>
Risk: The generated request JSON can contain user-provided text that may be sensitive. <br>
Mitigation: Review the local request file before sharing it or sending it through a separate client. <br>
Risk: Credential handling, endpoint selection, and data-retention behavior are outside this request-preparation skill. <br>
Mitigation: Review the separate client that transmits the request before deployment. <br>


## Reference(s): <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud Model Studio Embedding Documentation](https://help.aliyun.com/zh/model-studio/embedding) <br>
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON file] <br>
**Output Format:** [Markdown guidance with inline shell commands and a generated JSON request payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prepares a local request file and does not send the request to Alibaba Cloud.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
