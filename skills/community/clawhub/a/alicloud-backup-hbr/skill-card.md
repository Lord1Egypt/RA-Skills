## Description: <br>
Manage Alibaba Cloud Cloud Backup (HBR) via OpenAPI/SDK for backup lifecycle operations such as resource listing, policy and configuration updates, job status queries, and HBR backup or restore troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect and manage Alibaba Cloud Cloud Backup resources, policies, jobs, and restore workflows through OpenAPI or SDK calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Alibaba Cloud credentials to make real backup and restore configuration changes. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials limited to the needed account, region, and backup actions; confirm resource IDs and region before Create, Update, Modify, Set, restore, or delete-like operations. <br>
Risk: Saved API responses and generated artifacts may contain operational details from the cloud environment. <br>
Mitigation: Review local files under output/alicloud-backup-hbr/ before sharing the workspace or publishing results. <br>


## Reference(s): <br>
- [Artifact Sources](artifact/references/sources.md) <br>
- [Alibaba Cloud HBR OpenAPI Product Page](https://api.aliyun.com/product/hbr) <br>
- [Alibaba Cloud HBR API Metadata](https://api.aliyun.com/meta/v1/products/hbr/versions/2017-09-08/api-docs.json) <br>
- [Alibaba Cloud HBR Single API Definition Metadata](https://api.aliyun.com/meta/v1/products/hbr/versions/2017-09-08/apis/{ApiName}/api.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/alicloud-backup-hbr) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts are written under output/alicloud-backup-hbr/ when responses or API metadata are saved.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
