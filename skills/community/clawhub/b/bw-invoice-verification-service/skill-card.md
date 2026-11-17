## Description:

百望股份智能发票查验，支持发票文本核验、图片核验、批量核验、额度查询、套餐查询和充值下单，并明确披露外部服务与本地配置写入。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidd130](https://clawhub.ai/user/weidd130)

### License/Terms of Use:

MIT-0

## Use Case:

External business, finance, compliance, procurement, and settlement teams use this skill to verify invoice text or images, process invoice image folders in batch, check quota and packages, and create or query recharge orders through the documented remote service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice text, invoice images, and optional same-name .txt sidecar contents can be sent to the documented remote service.

Mitigation: Use the skill only when sending that invoice data to https://51yzt.cn/assetInnovate is acceptable, and confirm batch directories and processing scope before uploading.

Risk: The skill stores appKey, clientInstanceId, and deviceFingerprint in local files under ~/.openclaw/invoice-skill.

Mitigation: Protect that directory as local credential material and delete config.json and identity.json when the skill is no longer needed.

Risk: A configured or overridden API base URL can redirect requests away from the documented service.

Mitigation: Review the configured API base URL before use and avoid custom endpoints unless the user explicitly trusts them.

Risk: Recharge order creation can initiate payment flows.

Mitigation: Require explicit user confirmation of the recharge amount before creating an order and verify order status after payment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidd130/skills/bw-invoice-verification-service)
- [ClawHub install URL from artifact](https://clawhub.ai/weidd130/bw-invoice-verification-service)
- [Remote invoice verification service endpoint](https://51yzt.cn/assetInnovate)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON command output, with JSON result files for batch verification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js. The skill can write local configuration and identity files under ~/.openclaw/invoice-skill and can write batch verification result JSON files in the selected invoice directory.]

## Skill Version(s):

0.6.3 (source: server release evidence and script constant)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
