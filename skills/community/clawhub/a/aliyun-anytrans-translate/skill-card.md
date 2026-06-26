## Description: <br>
Use when managing Alibaba Cloud TongyiTranslate (AnyTrans) via OpenAPI/SDK, including translation service resource operations in Alibaba Cloud such as list/create/update actions, task status checks, and troubleshooting AnyTrans API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover Alibaba Cloud TongyiTranslate AnyTrans APIs, manage translation service resources, check task status, and troubleshoot API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide create, update, modify, or set operations against Alibaba Cloud translation service resources. <br>
Mitigation: Review each mutating action before execution, confirm region and resource identifiers, and use describe/list APIs to verify current state before and after changes. <br>
Risk: The skill relies on Alibaba Cloud credentials and may save API response summaries or artifacts locally. <br>
Mitigation: Use dedicated least-privilege credentials, avoid broad shared profiles, and keep generated files under output/aliyun-anytrans-translate/ free of secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-anytrans-translate) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud AnyTrans OpenAPI product page](https://api.aliyun.com/product/AnyTrans) <br>
- [AnyTrans 2025-07-07 API metadata](https://api.aliyun.com/meta/v1/products/AnyTrans/versions/2025-07-07/api-docs.json) <br>
- [AnyTrans API definition metadata](https://api.aliyun.com/meta/v1/products/AnyTrans/versions/2025-07-07/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes API inventory artifacts and response summaries under output/aliyun-anytrans-translate/ when files are needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
