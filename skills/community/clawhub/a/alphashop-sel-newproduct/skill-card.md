## Description: <br>
AlphaShop Sel Newproduct helps agents search validated product keywords and generate market analysis and new-product recommendation reports for Amazon and TikTok cross-border ecommerce. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, ecommerce operators, and product-research agents use this skill to run a two-step AlphaShop workflow: first retrieve supported keywords, then generate market ratings, opportunity analysis, product recommendations, and competitor comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AlphaShop credentials and makes outbound AlphaShop API calls, while credential requirements are documented inconsistently. <br>
Mitigation: Use a dedicated, revocable API key, configure it through OpenClaw secret or environment management, and confirm credential requirements before deployment. <br>
Risk: Product-research queries and generated JSON reports may contain sensitive business or market strategy data. <br>
Mitigation: Review saved reports before sharing, avoid committing report output or credential files, and limit access to users who should see the research data. <br>
Risk: The included test script can load values from a local .env file. <br>
Mitigation: Run test.sh only with trusted environment files and prefer managed secrets over plaintext .env files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688AiInfra/alphashop-sel-newproduct) <br>
- [API reference](references/api.md) <br>
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash examples, terminal summaries, and saved JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write keyword-search and new-product report JSON files under output/alphashop-sel-newproduct when the CLI commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
