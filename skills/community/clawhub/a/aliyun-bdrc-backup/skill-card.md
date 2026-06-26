## Description: <br>
Use when managing Alibaba Cloud Backup and Disaster Recovery Center (BDRC) via OpenAPI/SDK, including backup and disaster-recovery inventory, policy or configuration changes, status checks, and troubleshooting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud Backup and Disaster Recovery Center resources through OpenAPI or SDK workflows, including inventory, configuration changes, status checks, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use Alibaba Cloud credentials and call BDRC APIs, including mutating operations. <br>
Mitigation: Use a least-privilege RAM user or temporary role and confirm the account, region, resource IDs, and whether each action is read-only or mutating before execution. <br>
Risk: Generated local output files may contain API inventory details or response summaries that should not be shared broadly. <br>
Mitigation: Review files under output/aliyun-bdrc-backup/ before sharing or committing them. <br>


## Reference(s): <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud BDRC OpenAPI product page](https://api.aliyun.com/product/BDRC) <br>
- [BDRC API list metadata](https://api.aliyun.com/meta/v1/products/BDRC/versions/2023-08-08/api-docs.json) <br>
- [BDRC single API metadata template](https://api.aliyun.com/meta/v1/products/BDRC/versions/2023-08-08/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python helper code, and optional JSON or Markdown inventory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated API inventory artifacts are written under output/aliyun-bdrc-backup/ when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
