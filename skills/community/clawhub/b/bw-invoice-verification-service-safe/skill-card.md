## Description:

百望股份智能发票查验公开版，支持发票文本核验、图片核验、批量核验、额度查询、套餐查询和充值下单，并明确披露外部服务与本地配置写入。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidd130](https://clawhub.ai/user/weidd130)

### License/Terms of Use:

MIT-0

## Use Case:

External business, finance, reimbursement, risk-control, procurement, supply-chain, and settlement teams use this skill to verify Chinese invoice text or images, process invoice-image folders, check remaining quota and ledger entries, view packages, and create or query recharge orders.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sensitive invoice text, images, and sidecar text may be sent to the external service during text, image, or directory verification.

Mitigation: Use the skill only when the user trusts the publisher and service, avoid highly sensitive invoices, and confirm the target directory and upload scope before batch verification.

Risk: Credentials and persistent identifiers are stored locally under ~/.openclaw/invoice-skill.

Mitigation: Tell users where config.json and identity.json are stored, and remove those files when the skill is no longer needed.

Risk: Recharge order creation can initiate payment flows.

Mitigation: Require explicit confirmation of the recharge amount before invoking order creation, and review returned payment URLs or QR codes before use.

Risk: Custom API endpoints can redirect invoice data and stored credentials away from the default service.

Mitigation: Avoid custom API endpoints unless the endpoint is trusted and approved for the invoice data being processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidd130/skills/bw-invoice-verification-service-safe)
- [Publisher profile](https://clawhub.ai/user/weidd130)
- [Invoice verification service endpoint](https://51yzt.cn/assetInnovate)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files, guidance]

**Output Format:** [JSON responses with human-facing guidance and optional local JSON result files for batch verification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local config and identity files under ~/.openclaw/invoice-skill and batch verification results under the selected invoice-image directory.]

## Skill Version(s):

0.6.3 (source: release evidence and script constant)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
