## Description: <br>
Manage Alibaba Cloud TongyiTranslate (AnyTrans) via OpenAPI/SDK for translation service resource operations, including list/create/update actions, task status checks, and troubleshooting AnyTrans API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to discover Alibaba Cloud AnyTrans APIs, manage translation service resources, check task status, and troubleshoot API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use Alibaba Cloud credentials and call api.aliyun.com when following its workflows. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials, confirm region and resource identifiers before mutating operations, and expect outbound calls to Alibaba Cloud API metadata endpoints. <br>
Risk: Generated API inventory and response artifacts may contain operational details. <br>
Mitigation: Keep generated files under output/alicloud-ai-translation-anytrans/ and review artifacts before sharing them. <br>


## Reference(s): <br>
- [OpenAPI product page](https://api.aliyun.com/product/AnyTrans) <br>
- [AnyTrans API list metadata](https://api.aliyun.com/meta/v1/products/AnyTrans/versions/2025-07-07/api-docs.json) <br>
- [AnyTrans single API metadata](https://api.aliyun.com/meta/v1/products/AnyTrans/versions/2025-07-07/apis/{ApiName}/api.json) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-translation-anytrans) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls, Files] <br>
**Output Format:** [Markdown with inline shell commands and generated JSON or Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts should be written under output/alicloud-ai-translation-anytrans/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
