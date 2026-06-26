## Description: <br>
百望股份智能发票查验公开版，支持发票文本核验、图片核验、批量核验、额度查询、套餐查询和充值下单，并明确披露外部服务与本地配置写入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidd130](https://clawhub.ai/user/weidd130) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business, finance, reimbursement, compliance, procurement, supply-chain, and settlement teams use this skill to verify invoice text or images, process local invoice folders in batches, check remaining quota, review packages, and create recharge orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice text, invoice images, and sidecar text files may be sent to the disclosed remote service during verification. <br>
Mitigation: Confirm the files and directories before verification or batch processing, and use the skill only when that data transfer is acceptable. <br>
Risk: The skill stores local configuration and identity files under ~/.openclaw/invoice-skill/. <br>
Mitigation: Delete config.json and identity.json from that directory when the skill is no longer needed. <br>
Risk: Recharge order creation can initiate a paid flow through the remote service. <br>
Mitigation: Confirm recharge amounts explicitly before creating an order. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidd130/bw-invoice-verification-service-safe) <br>
- [Disclosed remote invoice verification service](https://51yzt.cn/assetInnovate) <br>
- [Artifact README](README.md) <br>
- [Artifact skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with structured JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local configuration, identity, and batch result files under the disclosed paths.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release metadata and script constant) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
