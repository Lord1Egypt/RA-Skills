## Description: <br>
Forecast Analysis Claw helps agents forecast SKU sales from historical CSV or Excel data, calculate replenishment quantities, account for promotion effects, and flag stockout risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operations, ecommerce, and inventory planning teams use this skill to clean sales history, run SKU-level or batch demand forecasts, generate replenishment plans, and prepare for major promotions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecasts and replenishment recommendations may be inaccurate when historical data is sparse, noisy, or affected by unmarked promotions. <br>
Mitigation: Review recommendations with business context, label promotion periods, and compare forecasts against actual sales before making stocking decisions. <br>
Risk: Sales and inventory files can contain sensitive business data, and the security evidence notes the release is low-risk but not deeply verified. <br>
Mitigation: Review the skill files and requested permissions before use, and run it only in approved environments for private or sensitive datasets. <br>


## Reference(s): <br>
- [Forecast Models](references/forecast-models.md) <br>
- [Promotion Coefficients](references/promo-coefficients.md) <br>
- [Replenishment Parameters](references/replenishment-params.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated CSV-style forecast fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sales forecasts, replenishment quantities, outlier reports, and inventory-risk summaries from user-provided sales and inventory data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
