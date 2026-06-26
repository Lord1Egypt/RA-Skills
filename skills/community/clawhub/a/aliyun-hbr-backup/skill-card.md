## Description: <br>
Use when managing Alibaba Cloud Cloud Backup (HBR) via OpenAPI/SDK, including backup lifecycle operations such as resource listing, policy or configuration updates, job status queries, and troubleshooting backup or restore workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and backup administrators use this skill to discover Alibaba Cloud HBR APIs, inspect backup resources, update backup policies or configuration, query job status, and troubleshoot backup or restore workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Alibaba Cloud credentials and may perform mutating Cloud Backup operations when directed. <br>
Mitigation: Use temporary or least-privilege Alibaba Cloud credentials and confirm the account, region, resource IDs, and whether the requested action is read-only or mutating before execution. <br>
Risk: Saved API responses and generated artifacts may include operational details from the cloud environment. <br>
Mitigation: Review files under output/aliyun-hbr-backup/ before sharing, publishing, or committing them. <br>


## Reference(s): <br>
- [Alibaba Cloud HBR OpenAPI Product Page](https://api.aliyun.com/product/hbr) <br>
- [Alibaba Cloud HBR API List Metadata](https://api.aliyun.com/meta/v1/products/hbr/versions/2017-09-08/api-docs.json) <br>
- [Alibaba Cloud HBR Single API Definition Metadata](https://api.aliyun.com/meta/v1/products/hbr/versions/2017-09-08/apis/{ApiName}/api.json) <br>
- [Skill Source References](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON API metadata, and saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API inventory, command outputs, and response summaries under output/aliyun-hbr-backup/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
