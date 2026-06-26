## Description: <br>
Use when managing Alibaba Cloud Cloud Call Center (CCC) via OpenAPI/SDK, including instance/resource management, configuration updates, status checks, and troubleshooting call-center API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud Cloud Call Center resources and troubleshoot CCC API workflows through Alibaba Cloud OpenAPI, SDK, and metadata-first discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Alibaba Cloud credentials for CCC workflows. <br>
Mitigation: Use a dedicated least-privilege AccessKey and prefer environment variables or the shared Alibaba Cloud credentials file. <br>
Risk: Create, Update, Modify, and Set operations can change live Alibaba Cloud CCC resources. <br>
Mitigation: Verify the region and resource identifiers, then require explicit approval before running any mutating operation. <br>
Risk: Saved outputs may contain operational details from cloud API responses. <br>
Mitigation: Review generated files and response summaries before sharing them outside the intended operational context. <br>


## Reference(s): <br>
- [Alibaba Cloud CCC OpenAPI product page](https://api.aliyun.com/product/CCC) <br>
- [Alibaba Cloud CCC API metadata](https://api.aliyun.com/meta/v1/products/CCC/versions/2020-07-01/api-docs.json) <br>
- [Alibaba Cloud CCC single API definition](https://api.aliyun.com/meta/v1/products/CCC/versions/2020-07-01/apis/{ApiName}/api.json) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-ccc-manage) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Text and Markdown with inline shell commands plus generated JSON or Markdown API inventory artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts and API response summaries are intended to be saved under output/aliyun-ccc-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
