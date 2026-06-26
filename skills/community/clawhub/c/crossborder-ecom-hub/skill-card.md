## Description: <br>
Crossborder Ecom Hub helps cross-border ecommerce sellers manage product synchronization, orders, inventory, pricing, reports, and Feishu Bitable updates across TikTok Shop, Amazon, Shopee, and Lazada. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers and operators use this skill to coordinate marketplace listings, order views, inventory checks, pricing suggestions, reports, and optional Feishu Bitable synchronization from one CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles marketplace credentials and business data. <br>
Mitigation: Use environment variables or a secrets manager, grant least-privilege marketplace and Feishu credentials, and review deployment before using it in a real seller environment. <br>
Risk: Sync and pricing actions can have high business impact. <br>
Mitigation: Avoid --apply and broad sync commands unless an external preview and approval process is in place. <br>
Risk: This version mixes mocked marketplace API behavior with real Feishu synchronization. <br>
Mitigation: Treat the release as a prototype and verify marketplace behavior separately before relying on synchronized Feishu records. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lvjunjie-byte/crossborder-ecom-hub) <br>
- [Publisher profile](https://clawhub.ai/user/lvjunjie-byte) <br>
- [TikTok Shop Open Platform](https://partner.tiktokshop.com/) <br>
- [Amazon Selling Partner API](https://developer.amazon.com/sp-api) <br>
- [Shopee Open Platform](https://open.shopee.com/) <br>
- [Lazada Open Platform](https://open.lazada.com/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Files] <br>
**Output Format:** [CLI output in table, JSON, or CSV formats, plus configuration JSON and exported report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local configuration file and optional report exports when the corresponding commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
