## Description:

Manage Alibaba Cloud PAI AIWorkspace (AIWorkSpace) via OpenAPI/SDK for workspace and project inventory, lifecycle actions, status queries, permission or configuration troubleshooting, and related automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud PAI AIWorkspace resources through OpenAPI metadata discovery, SDK or OpenAPI Explorer calls, and reproducible output artifacts. It is intended for resource inventory, create/update workflows, status checks, troubleshooting, and automation around AIWorkspace lifecycle tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide use of Alibaba Cloud credentials and mutating AIWorkspace APIs.

Mitigation: Use least-privilege Alibaba Cloud credentials and require explicit review of the region, resource identifiers, and API action before any Create, Update, Modify, or Set operation.

Risk: Untrusted product-code, version, or output-dir values passed to the helper script may affect what metadata is fetched or where artifacts are written.

Mitigation: Avoid untrusted override values until path validation is added; keep generated artifacts under output/alicloud-ai-pai-aiworkspace/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-pai-aiworkspace)
- [Artifact sources reference](references/sources.md)
- [Alibaba Cloud OpenAPI AIWorkSpace product page](https://api.aliyun.com/product/AIWorkSpace)
- [AIWorkSpace 2021-02-04 API metadata list](https://api.aliyun.com/meta/v1/products/AIWorkSpace/versions/2021-02-04/api-docs.json)
- [AIWorkSpace single API metadata definition](https://api.aliyun.com/meta/v1/products/AIWorkSpace/versions/2021-02-04/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown with inline shell commands, API parameter summaries, and optional generated JSON or Markdown artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts should be written under output/alicloud-ai-pai-aiworkspace/ when saved.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
