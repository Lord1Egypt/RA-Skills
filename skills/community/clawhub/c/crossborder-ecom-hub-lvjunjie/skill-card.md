## Description: <br>
Crossborder Ecom Hub helps cross-border ecommerce sellers manage product sync, orders, inventory, pricing, reports, and Feishu Bitable updates across TikTok Shop, Amazon, Shopee, and Lazada. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers and operators use this skill through a Node.js CLI to coordinate listings, orders, inventory, pricing recommendations, reports, and Feishu Bitable records across supported marketplaces. Use sandbox or least-privilege accounts before enabling bulk sync, inventory, or pricing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace and Feishu credentials may grant access to valuable seller accounts or workspace data. <br>
Mitigation: Use sandbox or least-privilege accounts first, store credentials with appropriate filesystem permissions, rotate secrets regularly, and restrict Feishu app and workspace sharing. <br>
Risk: Bulk sync, inventory update, and pricing apply commands can change products, stock, or prices across multiple marketplaces. <br>
Mitigation: Run preview or narrow-scope operations first, keep a rollback plan, and avoid production-wide apply commands until behavior is verified. <br>
Risk: The artifact documents broad marketplace support while some platform API adapters are marked as TODO or mock behavior. <br>
Mitigation: Validate each marketplace integration with non-production accounts and small datasets before relying on the skill for live operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/crossborder-ecom-hub-lvjunjie) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Example configuration](artifact/config.example.json) <br>
- [TikTok Shop Open Platform](https://partner.tiktokshop.com/) <br>
- [Amazon Selling Partner API](https://developer.amazon.com/sp-api) <br>
- [Shopee Open Platform](https://open.shopee.com/) <br>
- [Lazada Open Platform](https://open.lazada.com/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, CSV] <br>
**Output Format:** [CLI output, local configuration JSON, and optional exported JSON or CSV reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local marketplace and Feishu credentials, write local configuration under the user's home directory, and export reports to a user-selected path.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release.version and clawhub.json; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
