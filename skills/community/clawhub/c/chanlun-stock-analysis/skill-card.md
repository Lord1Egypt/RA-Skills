## Description:

Generates comprehensive stock research reports using Chan theory technical analysis, fundamentals, financial statements, and valuation analysis, with Markdown and PDF report outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywwzzsgit](https://clawhub.ai/user/ywwzzsgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to generate structured stock research reports from a provided ticker or company name. It is intended for research-oriented technical, fundamental, and valuation analysis across supported A-share, Hong Kong, and U.S. stocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install the unpinned Python package reportlab.

Mitigation: Install and run the skill in an isolated environment where automatic Python package installation is acceptable.

Risk: The skill relies on a mutable external finance-data skill that may handle a Tushare token.

Mitigation: Limit exposure of TUSHARE_TOKEN, scope it to the analysis environment, and review the external finance-data skill before use.

Risk: Generated buy, sell, target-price, and position-size guidance can be incorrect or misleading.

Mitigation: Treat reports as informational research output only and require qualified human review before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ywwzzsgit/skills/chanlun-stock-analysis)
- [Chan theory reference](references/chan-theory.md)
- [Financial analysis reference](references/financial-analysis.md)
- [Valuation reference](references/valuation.md)
- [Tushare data provider](https://tushare.pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown report plus generated PDF file, with supporting Python and shell snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include stock ratings, technical indicators, valuation ranges, risk notes, and an informational disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
