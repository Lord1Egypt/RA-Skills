## Description: <br>
百望股份智能发票查验，支持发票文本核验、图片核验、批量核验、额度查询、套餐查询和充值下单，并明确披露外部服务与本地配置写入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidd130](https://clawhub.ai/user/weidd130) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, reimbursement, compliance, procurement, and operations teams use this skill to verify invoice text or images, process invoice folders, check remaining quota, review packages, and create or query recharge orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice text, invoice images, and same-name .txt companion text can be sent to the remote invoice-verification service. <br>
Mitigation: Use the skill only for invoice data approved for that service, and review the data or files before verification. <br>
Risk: Batch verification can process a local directory and send each selected invoice image and companion text file to the remote service. <br>
Mitigation: Use explicit skill-qualified commands, confirm the directory path and processing scope, and avoid directories containing unrelated or sensitive files. <br>
Risk: The skill stores local configuration, app key material, and persistent random identifiers under ~/.openclaw/invoice-skill/. <br>
Mitigation: Delete ~/.openclaw/invoice-skill/config.json and ~/.openclaw/invoice-skill/identity.json when the local key and identifiers are no longer needed. <br>
Risk: Recharge order creation can start a payment flow for a selected amount. <br>
Mitigation: Confirm the recharge amount with the user before creating an order, and query order status or quota after payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidd130/bw-invoice-verification-service) <br>
- [Publisher profile](https://clawhub.ai/user/weidd130) <br>
- [Remote invoice verification service](https://51yzt.cn/assetInnovate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [JSON responses, Markdown-facing guidance, command examples, and local JSON result files for batch verification.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch verification can write per-invoice .verify.json files and summary.json; image verification supports PNG/JPEG content up to 2 MB.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release metadata and script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
