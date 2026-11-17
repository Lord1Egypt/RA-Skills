## Description:

Converts 1688 product information into Ozon listing data, uploads listings through Ozon APIs, and checks upload status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators use this skill to convert 1688 product data into Ozon-compatible listings, translate product imagery to Russian, upload products, and review upload status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live marketplace listing changes through Ozon APIs.

Mitigation: Review generated product data before upload and require explicit confirmation or a dry run before making live changes.

Risk: Image translation can send product images to AlphaShop and may consume paid API quota.

Mitigation: Use only credentials and product images approved for AlphaShop processing, and guard batch translation so it cannot run unexpectedly.

Risk: The security evidence flags the release for review because batch_translate.py can perform paid requests and write files without clear user control.

Mitigation: Remove the batch script or add explicit user-controlled execution, quota limits, and output path controls before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-product-to-ozon)
- [README](README.md)
- [Offer description template](references/offer_description.json)
- [Ozon Seller Portal](https://seller.ozon.ru/)
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON product data and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary product JSON and report Ozon upload task status.]

## Skill Version(s):

1.2.1 (source: server release metadata and skill metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
