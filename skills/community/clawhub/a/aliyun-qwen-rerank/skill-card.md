## Description: <br>
Use when reranking search candidates is needed with Alibaba Cloud Model Studio rerank models, including hybrid retrieval, top-k refinement, and multilingual relevance sorting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Alibaba Cloud Model Studio rerank request payloads for search workflows, including hybrid retrieval, top-k refinement, and multilingual relevance sorting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated rerank request payloads may contain queries or documents that a later client sends to Alibaba Cloud. <br>
Mitigation: Review request.json before using it with any separate client and avoid including sensitive content unless the deployment policy permits transmission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-qwen-rerank) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud Model Studio embeddings and rerank documentation](https://help.aliyun.com/zh/model-studio/embedding) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request payload files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local request.json payload; no network call or credential use is performed by the bundled helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
