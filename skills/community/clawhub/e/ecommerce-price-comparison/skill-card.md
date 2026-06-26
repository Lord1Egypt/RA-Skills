## Description: <br>
从京东、淘宝、天猫、拼多多等中国电商平台抓取商品价格并进行比较分析。当用户需要比较不同电商平台的商品价格、寻找最佳性价比、或监控商品价格变化时使用。支持关键词搜索、商品链接分析、价格历史追踪和购买建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[birdme007](https://clawhub.ai/user/birdme007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and purchasing analysts use this skill to compare prices, promotions, shipping costs, reviews, and seller reputation across major Chinese e-commerce platforms before buying or monitoring products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact shopping platforms and its documentation discusses anti-bot workarounds. <br>
Mitigation: Use only user-approved, low-rate checks and review each target platform's terms before running scraping workflows. <br>
Risk: Logged-in scraping, cookies, browser sessions, proxies, or CAPTCHA-solving workflows could create consent, account, or compliance risk. <br>
Mitigation: Do not provide credentials, cookies, browser sessions, proxy pools, or CAPTCHA-solving steps unless explicit authorization and terms review are in place. <br>
Risk: Price and inventory results can be incomplete, stale, account-specific, or region-specific. <br>
Mitigation: Treat generated comparisons as decision support and verify final price, stock, shipping, and seller details on the platform before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/birdme007/ecommerce-price-comparison) <br>
- [平台API文档](references/platform_apis.md) <br>
- [价格比较逻辑](references/comparison_logic.md) <br>
- [报告模板](assets/template_report.md) <br>
- [抓取脚本说明](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include price comparisons, scoring, purchase recommendations, risk notes, and scraper setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
