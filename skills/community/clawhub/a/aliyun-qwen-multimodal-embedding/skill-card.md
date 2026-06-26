## Description: <br>
Use when multimodal embeddings are needed from Alibaba Cloud Model Studio models such as `qwen3-vl-embedding` for image, video, and text retrieval, cross-modal search, clustering, or offline vectorization pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Alibaba Cloud Model Studio multimodal embedding requests for text, image, and video retrieval, similarity search, clustering, and offline vectorization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba/DashScope credentials may be exposed or over-permissioned. <br>
Mitigation: Use a scoped API key, keep it out of generated files, and store it through `DASHSCOPE_API_KEY` or an approved credentials file. <br>
Risk: Embedding inputs and generated request files may contain sensitive prompts, URLs, or local file references. <br>
Mitigation: Only process content approved for the Alibaba Cloud workflow and remove generated request files when they are no longer needed. <br>
Risk: Changing model or vector dimension within one index can create incompatible embeddings. <br>
Mitigation: Pin the model and output dimension before writing vectors and record those settings with each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-qwen-multimodal-embedding) <br>
- [Model Studio embedding documentation](https://help.aliyun.com/zh/model-studio/embedding) <br>
- [Model Studio model list](https://help.aliyun.com/zh/model-studio/models) <br>
- [Model Studio model release updates](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Artifact reference sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with Python CLI commands and generated JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces normalized request payloads and records selected model, modality mix, and vector dimension for reproducibility.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
