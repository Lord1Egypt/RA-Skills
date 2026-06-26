## Description: <br>
Searches Amazon and TikTok product listings through the AlphaShop REST API by keyword, with filters for price, sales, rating, listing age, platform, and region. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, market researchers, and agent builders use this skill to search and compare products across supported Amazon and TikTok regions. It helps collect product, supplier, price, rating, sales, listing age, and logistics details for selection and market analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product-search terms and request parameters to the external AlphaShop API and uses API-key based authentication. <br>
Mitigation: Use it only when AlphaShop is approved for the intended product-search workflow, keep API keys in the skill environment, and avoid exposing secrets in command lines or shared files. <br>
Risk: The security evidence flags inconsistent scope because bundled image-search documentation does not match the advertised keyword product-search skill. <br>
Mitigation: Treat the image-search reference material as out of scope until the publisher clarifies it, and review the installed artifact before deployment. <br>
Risk: Search queries may reveal confidential market research or product strategy to an external service. <br>
Mitigation: Do not submit confidential keywords or market terms unless external transmission to AlphaShop is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1688AiInfra/alphashop-sel-product-search) <br>
- [Product Search API Reference](artifact/references/api.md) <br>
- [Skill README](artifact/README.md) <br>
- [AlphaShop API Key Management](https://www.alphashop.cn/seller-center/apikey-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and optional JSON response files, with Markdown guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires keyword, platform, and region before execution; optional filters include price, sales, rating, listing age, result count, and user id.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
