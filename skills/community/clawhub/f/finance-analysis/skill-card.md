## Description: <br>
Finance Analysis is a CLI skill for financial statement analysis, stock valuation, and risk assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alsoforever](https://clawhub.ai/user/alsoforever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance analysts, investors, and developers use this skill to run command-line financial statement checks, DCF or relative valuation, and risk scoring for listed stocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Valuation and risk commands may present fixed sample numbers as if they were stock-specific analysis. <br>
Mitigation: Treat valuation and risk output as review material unless the publisher clearly labels sample mode or replaces samples with current, validated financial data. <br>
Risk: The skill uses optional external financial data access through Tushare. <br>
Mitigation: Run it in a virtual environment and use a limited Tushare token when external data access is needed. <br>


## Reference(s): <br>
- [Finance Analysis on ClawHub](https://clawhub.ai/alsoforever/finance-analysis) <br>
- [Project homepage](https://github.com/alsoforever/gungun-life) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [CLI text output and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial data access may use a Tushare token when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
