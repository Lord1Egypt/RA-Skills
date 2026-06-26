## Description: <br>
Generates evidence-backed after-market A-share review reports from Tushare daily market data, including market trend, concentration, money effect, abnormal declines, feature groups, and resilient-stock analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinfi-codex](https://clawhub.ai/user/chinfi-codex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to build daily or historical A-share market reviews from deterministic evidence packages and module-specific methodology. It is intended for market-report writing and quantitative observation, not investment advice, automated trading, or portfolio optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a Tushare API token and outbound market-data requests, including JRJ data for the early-limit-up feature. <br>
Mitigation: Install only in environments where those credentials and outbound requests are acceptable, and manage the API token according to local secret-handling policy. <br>
Risk: The skill creates and updates local cache, evidence, context, and report files, and its documented cleanup step can remove temporary evidence files. <br>
Mitigation: Review generated files before relying on the report and keep evidence files when auditability or later review is required. <br>
Risk: Generated reports may be mistaken for trading recommendations if the no-advice discipline is not followed. <br>
Mitigation: Keep outputs framed as market research and evidence review, and avoid buy, sell, stop-loss, target-price, or portfolio-allocation instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinfi-codex/a-stock-daily-market-sense) <br>
- [Skill instructions](SKILL.md) <br>
- [Report template](reference/report_template.md) <br>
- [Output discipline](reference/methodology/output_discipline.md) <br>
- [Market trend methodology](reference/methodology/module1_trend.md) <br>
- [Money effect methodology](reference/methodology/module3_money_effect.md) <br>
- [Feature groups methodology](reference/methodology/module5_feature_groups.md) <br>
- [JRJ limit-up data endpoint](https://gateway.jrj.com/quot-dc/zdt/v1/record) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports with JSON evidence and module context files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses deterministic market-data evidence before model-authored report sections; does not call an LLM from the bundled scripts.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
