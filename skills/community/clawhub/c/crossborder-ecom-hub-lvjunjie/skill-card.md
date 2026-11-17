## Description:

Crossborder Ecom Hub helps cross-border e-commerce sellers manage product sync, orders, inventory, pricing, reports, and Feishu Bitable updates across TikTok Shop, Amazon, Shopee, and Lazada.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and operations teams use this skill to coordinate catalog, order, inventory, pricing, and reporting workflows across multiple marketplace platforms. It is intended for commercial marketplace operations where API credentials, business records, and external data uploads are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles marketplace API credentials and Feishu app credentials.

Mitigation: Use least-privilege API keys, avoid passing secrets through command-line flags, and restrict permissions on ~/.crossborder-ecom/config.json.

Risk: Bulk sync, inventory sync, and pricing apply commands can change platform records at operational scale.

Mitigation: Run only after a dry-run, backup, and approval process confirms the target platforms, products, inventory records, and pricing strategy.

Risk: Feishu upload and export commands can share or persist business data outside the source platforms.

Mitigation: Confirm the destination Bitable, export path, access controls, and data classification before uploading or exporting records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/crossborder-ecom-hub-lvjunjie)
- [TikTok Shop Open Platform](https://partner.tiktokshop.com/)
- [Amazon Selling Partner API](https://developer.amazon.com/sp-api)
- [Shopee Open Platform](https://open.shopee.com/)
- [Lazada Open Platform](https://open.lazada.com/)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV or JSON exports and upload selected business data to Feishu when the corresponding commands are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
