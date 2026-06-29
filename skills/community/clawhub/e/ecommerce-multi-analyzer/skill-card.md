## Description: <br>
输入主流电商平台商品链接后，该技能会抓取和搜索商品信息，比较多平台价格、评分、评价和店铺信息，并生成本地交互式 HTML 分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Shoppers, sourcing teams, and ecommerce analysts use this skill to compare one product across Chinese ecommerce platforms and create a buying-advice report from available product page and search data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches product pages and search results from external ecommerce sites. <br>
Mitigation: Run it only in contexts where external product lookups are acceptable, and avoid submitting sensitive or private product links. <br>
Risk: Third-party page text can be inserted into the generated local HTML report. <br>
Mitigation: Open generated reports only for trusted product links and review report content before sharing it. <br>
Risk: Prices, ratings, and availability may be stale, incomplete, or affected by ecommerce anti-scraping controls. <br>
Mitigation: Treat the report as decision support, verify important values on the source platforms, and include the retrieval time in the analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/ecommerce-multi-analyzer) <br>
- [Project homepage](https://github.com/bettermen/ecommerce-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Agent guidance plus structured JSON data and a generated interactive HTML report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes product-analysis data and the generated report locally under /tmp using the included Python report generator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
