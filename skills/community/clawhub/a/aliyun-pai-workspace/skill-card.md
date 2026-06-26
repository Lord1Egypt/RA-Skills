## Description: <br>
Helps agents manage Alibaba Cloud PAI AIWorkspace resources through official OpenAPI and SDK workflows, including inventory, create or update actions, status checks, permissions, configuration troubleshooting, and lifecycle automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud PAI AIWorkspace resources, discover API metadata, run list or describe workflows, and prepare create, update, modify, or permission-related operations with reproducible output evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide create, update, modify, set, and permission-related cloud operations that may change Alibaba Cloud resources. <br>
Mitigation: Use least-privilege credentials and confirm the account, region, resource identifiers, API name, and parameters before any mutating operation. <br>
Risk: Saved API responses and command outputs may contain operational details that should not be shared broadly. <br>
Mitigation: Review files written under output/aliyun-pai-workspace/ before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-pai-workspace) <br>
- [OpenAPI product page](https://api.aliyun.com/product/AIWorkSpace) <br>
- [AIWorkspace API metadata](https://api.aliyun.com/meta/v1/products/AIWorkSpace/versions/2021-02-04/api-docs.json) <br>
- [AIWorkspace single API definition metadata](https://api.aliyun.com/meta/v1/products/AIWorkSpace/versions/2021-02-04/apis/{ApiName}/api.json) <br>
- [Artifact sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, API calls, markdown, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python script usage, API response summaries, JSON metadata files, and Markdown evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated API inventory, command outputs, and response summaries under output/aliyun-pai-workspace/ when artifacts are saved.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
