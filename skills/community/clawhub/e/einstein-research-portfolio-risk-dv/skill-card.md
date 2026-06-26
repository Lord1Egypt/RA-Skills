## Description: <br>
Performs a comprehensive, portfolio-level risk analysis by calculating Value at Risk, max drawdown, correlation, historical stress tests, and concentration risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate equity portfolio risk from holdings data, including VaR, CVaR, drawdown, beta, stress-test, correlation, and concentration analysis. The outputs are intended as educational risk flags and portfolio review support, not trade recommendations or financial planning advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes private portfolio holdings and saves portfolio-derived reports locally. <br>
Mitigation: Run it in a trusted environment, choose a secure output directory, and delete generated reports when they are no longer needed. <br>
Risk: The skill depends on unpinned Python packages and queries Yahoo Finance for market data. <br>
Mitigation: Install dependencies in an isolated environment that is acceptable for unpinned packages, and review downloaded data before relying on the analysis. <br>
Risk: Generated action items could be mistaken for trade instructions. <br>
Mitigation: Treat action items as educational risk flags and review them against the user's own investment policy or qualified financial advice before taking action. <br>


## Reference(s): <br>
- [Risk Methodologies Reference](references/risk_methodologies.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/einstein-research-portfolio-risk-dv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Natural language summary with generated Markdown and JSON portfolio risk reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided portfolio holdings and local Python dependencies; saves reports locally by default.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
