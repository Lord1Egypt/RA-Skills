## Description: <br>
Use when managing Alibaba Cloud ApsaraVideo for Media Processing (MPS/MTS) resources and workflows via OpenAPI/SDK, including media ingest and metadata tasks, transcoding/snapshot jobs, pipeline/template/workflow operations, and MPS job troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to discover Alibaba Cloud MPS OpenAPI operations, validate media-processing configuration, and manage pipelines, templates, workflows, jobs, snapshots, and media resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide operations that change Alibaba Cloud MPS resources, including submit, cancel, update, delete, and bucket-binding actions. <br>
Mitigation: Use scoped or short-lived STS credentials, verify target region and resource IDs, and require explicit approval before write actions. <br>
Risk: Generated operation evidence may contain regions, bucket names, media IDs, pipeline IDs, template IDs, workflow IDs, request parameters, or other operational details. <br>
Mitigation: Keep output/aliyun-mps-manage private or redact sensitive operational details before sharing. <br>


## Reference(s): <br>
- [Source list](references/sources.md) <br>
- [Task templates](references/templates.md) <br>
- [Alibaba Cloud MPS OpenAPI product page](https://api.aliyun.com/product/mts) <br>
- [Alibaba Cloud MPS API metadata](https://api.aliyun.com/meta/v1/products/Mts/versions/2014-06-18/api-docs.json) <br>
- [Alibaba Cloud MPS API definition template](https://api.aliyun.com/meta/v1/products/Mts/versions/2014-06-18/apis/{ApiName}/api.json) <br>
- [ApsaraVideo for Media Processing documentation](https://www.alibabacloud.com/help/en/mts) <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-mps-manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated JSON evidence files, and API inventory Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated API inventories and operation evidence under output/aliyun-mps-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
