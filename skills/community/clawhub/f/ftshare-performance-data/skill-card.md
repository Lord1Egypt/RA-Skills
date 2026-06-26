## Description: <br>
Looks up A-share earnings express reports, earnings forecasts, cash flow statements, income statements, and balance sheets for single stocks or full-market reporting periods using market.ft.tech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn92](https://clawhub.ai/user/shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Chinese A-share financial performance and statement data for a single stock or for all stocks in a selected reporting period. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Python scripts and makes HTTPS GET requests to market.ft.tech for financial market data. <br>
Mitigation: Install and run it only in environments where outbound requests to market.ft.tech and execution of the bundled scripts are acceptable. <br>
Risk: Market and financial statement data can be incomplete, delayed, or unsuitable as sole investment advice. <br>
Mitigation: Treat results as lookup data and verify important financial decisions against authoritative filings or other trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawn92/ftshare-performance-data) <br>
- [market.ft.tech](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON from Python handlers, typically summarized by the agent as Markdown tables or bullet points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial data responses may include paginated result sets for full-market reporting-period queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
