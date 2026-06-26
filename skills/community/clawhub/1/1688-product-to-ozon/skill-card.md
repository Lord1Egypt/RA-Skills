## Description: <br>
Converts 1688 product information into Ozon marketplace listing data, uploads listings through Ozon APIs, and checks upload status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operators and commerce developers use this skill to convert 1688 product data into Ozon listing payloads, translate listing text and images into Russian, upload listings, and review upload status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload marketplace listings using seller credentials without a clearly documented final approval step. <br>
Mitigation: Require a manual review of generated product JSON, translated text and images, prices, and target Ozon account before running the upload step. <br>
Risk: The workflow sends product images and listing metadata to AlphaShop and Ozon services. <br>
Mitigation: Use it only for products and seller accounts where sharing that data with those services is intended and authorized. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1688AiInfra/1688-product-to-ozon) <br>
- [Offer description template](references/offer_description.json) <br>
- [Ozon seller portal](https://seller.ozon.ru/) <br>
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON product data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update temporary product JSON before Ozon upload.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
