## Description: <br>
A Streamlit dashboard for A-share stock screening, sector tracking, northbound capital flow review, and portfolio monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superhhh1992-byte](https://clawhub.ai/user/superhhh1992-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to run a local web dashboard for A-share market review, stock pool screening, single-stock analysis, and portfolio monitoring. Its generated scores and trading suggestions should be treated as informational analysis rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard runs an unreviewed helper script from another local skill path when loading market data. <br>
Mitigation: Inspect and trust the referenced a-share-stock-dossier helper before running the dashboard, or run the skill in a controlled environment. <br>
Risk: Portfolio monitoring inputs can reveal sensitive position details. <br>
Mitigation: Avoid entering sensitive portfolio details unless the dashboard and its helper script are trusted for the intended environment. <br>
Risk: Stock scores, risk alerts, and operation suggestions may be mistaken for financial advice. <br>
Mitigation: Treat generated analysis as informational only and verify market data and decisions independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superhhh1992-byte/a-share-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a Streamlit Python dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local Streamlit dashboard and call an external local market-data helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
