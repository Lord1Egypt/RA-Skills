## Description: <br>
Use when managing Alibaba Cloud Intelligent Cloud Editing (ICE) media workflows via OpenAPI/SDK, including media processing jobs, template/workflow orchestration, editing and production pipelines, and job status troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage Alibaba Cloud ICE media workflows, discover OpenAPI metadata, validate prerequisite resources, submit and monitor media processing jobs, and preserve execution evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent use Alibaba Cloud ICE credentials and interact with cloud resources. <br>
Mitigation: Use least-privilege RAM or STS credentials and review any resource-changing operation before execution. <br>
Risk: Generated evidence files may contain workflow IDs, job IDs, regions, object paths, and request details. <br>
Mitigation: Protect or clean output/aliyun-ice-manage/ before sharing logs or artifacts. <br>
Risk: Incorrect region, workflow, job, or OSS parameters could affect the wrong media workflow. <br>
Mitigation: Confirm target region, workflow IDs, job IDs, and input/output OSS locations before write operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-ice-manage) <br>
- [OpenAPI product page](https://api.aliyun.com/product/ice) <br>
- [ICE OpenAPI metadata](https://api.aliyun.com/meta/v1/products/ice/versions/2020-11-09/api-docs.json) <br>
- [ICE single API metadata template](https://api.aliyun.com/meta/v1/products/ice/versions/2020-11-09/apis/{ApiName}/api.json) <br>
- [Alibaba Cloud ICE documentation](https://www.alibabacloud.com/help/en/ice) <br>
- [Source list](references/sources.md) <br>
- [ICE task templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration details, and generated JSON or Markdown evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated evidence is expected under output/aliyun-ice-manage/ and may include API inventories, request payloads, responses, workflow IDs, job IDs, regions, and OSS object paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
