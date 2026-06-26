## Description: <br>
AlphaShop Text provides API-backed text translation and multilingual product selling-point and title generation for ecommerce workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce developers use this skill to translate product text, generate multilingual selling points, and create multilingual product titles through AlphaShop APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AlphaShop credentials are required for API calls. <br>
Mitigation: Configure least-privilege AlphaShop keys through OpenClaw settings and avoid placing secrets in prompts, logs, or shared files. <br>
Risk: Text and product data are sent to a third-party AlphaShop API. <br>
Mitigation: Use the skill only for data approved for sharing with AlphaShop. <br>
Risk: API calls may consume AlphaShop account credits or fail when the account has insufficient balance. <br>
Mitigation: Check account credit status before use and pause the workflow if AlphaShop reports insufficient balance. <br>


## Reference(s): <br>
- [AlphaShop Text API Reference](references/api-docs.md) <br>
- [AlphaShop API Key Management](https://www.alphashop.cn/seller-center/apikey-management) <br>
- [ClawHub Release Page](https://clawhub.ai/1688AiInfra/alphashop-text) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON API responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured AlphaShop credentials and may consume AlphaShop account credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
