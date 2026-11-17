## Description:

Use when managing Alibaba Cloud Backup and Disaster Recovery Center (BDRC) via OpenAPI/SDK, including the user needs backup/disaster-recovery resource operations, including inventory, policy/configuration changes, status checks, and troubleshooting BDRC workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to manage Alibaba Cloud Backup and Disaster Recovery Center resources, including inventory, policy or configuration changes, status checks, and troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Alibaba Cloud backup configuration changes.

Mitigation: Use least-privilege BDRC credentials, require explicit human approval for Create, Update, Modify, and Set operations, and record rollback steps before applying changes.

Risk: The helper script has an output-path validation flaw when product code or version overrides are untrusted.

Mitigation: Avoid untrusted product-code or version overrides until filenames are validated and writes are constrained to output/aliyun-bdrc-backup/.

## Reference(s):

- [Alibaba Cloud BDRC OpenAPI product page](https://api.aliyun.com/product/BDRC)
- [BDRC 2023-08-08 API metadata list](https://api.aliyun.com/meta/v1/products/BDRC/versions/2023-08-08/api-docs.json)
- [BDRC single API metadata template](https://api.aliyun.com/meta/v1/products/BDRC/versions/2023-08-08/apis/{ApiName}/api.json)
- [Artifact sources](references/sources.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write API inventory artifacts under output/aliyun-bdrc-backup/ when the helper script is run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
