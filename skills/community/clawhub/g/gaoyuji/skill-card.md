## Description: <br>
Search products across 8 Chinese e-commerce platforms, retrieve product details by URL or ID, and compare prices using the Shopme unified product database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoyuji12138](https://clawhub.ai/user/gaoyuji12138) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Chinese e-commerce platforms, inspect product details from links or IDs, compare prices, and find Chinese suppliers across Taobao, Tmall, JD, PDD, 1688, AliExpress, Douyin, and XHS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product keywords and product links may be sent to Shopme's external service. <br>
Mitigation: Avoid submitting sensitive product queries or private supplier URLs unless that external service use is acceptable. <br>
Risk: The executable MCP server is fetched from npm through npx. <br>
Mitigation: Review or pin the @shopmeagent/cn-ecommerce-search-mcp package version before installation in higher-assurance environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaoyuji12138/gaoyuji) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP configuration snippets and structured product-search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the @shopmeagent/cn-ecommerce-search-mcp server via npx; no API keys are required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
