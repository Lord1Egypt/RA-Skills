## Description: <br>
Stock Deep Analysis Framework 4.1 produces detailed Markdown analysis reports for A-share, Hong Kong, and U.S. stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghgh2026](https://clawhub.ai/user/ghgh2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request structured stock analysis reports for A-share, Hong Kong, and U.S. equities. It gathers current market, financial, news, and industry signals, then formats a sourced Markdown report with valuation, risk, catalyst, and disclaimer sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad stock-name and ticker triggers may activate the skill unintentionally and may query external finance or search providers. <br>
Mitigation: Use explicit stock-analysis requests and avoid including confidential portfolio details, internal research, account information, or trading instructions in prompts. <br>
Risk: Generated stock analysis may be incomplete, stale, inaccurate, or mistaken for personalized financial advice. <br>
Mitigation: Require current data with source dates, cross-check important claims against independent sources, and preserve the skill's disclaimer that outputs are for reference only and not investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghgh2026/gh-stock-deep-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown stock analysis report with tables, citations, risk notes, and investment disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses current finance and search data where tools are available; generated analysis should be treated as informational and reviewed before decisions.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
