## Description: <br>
Reviews earnings quality before valuation when structured financial statements are available; optional notes improve confidence. Requires supplied data only and performs no direct data fetching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance analysts, valuation reviewers, and agents use this skill to assess whether user-supplied earnings are cash-backed, identify accrual and working-capital risks, and package confidence-impact signals for downstream valuation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be invoked automatically in finance-related conversations and its analysis depends on the completeness and freshness of supplied financial statements. <br>
Mitigation: Confirm that input statements and notes are current and complete before relying on the output; preserve listed data gaps and confidence caps in downstream valuation work. <br>
Risk: The output could be mistaken for investment advice if used without context. <br>
Mitigation: Treat the report as analytical support for valuation review, not as a buy, sell, or hold recommendation. <br>
Risk: Missing financial statement notes can hide accounting-policy changes, related-party transactions, contingencies, or debt maturity concerns. <br>
Mitigation: Cap confidence when relevant notes are absent and explicitly carry note gaps into the handoff bundle. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ndtchan/earnings-quality-reviewer) <br>
- [Publisher profile](https://clawhub.ai/user/ndtchan) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown report with structured sections and handoff markers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses supplied financial statements and optional notes only; no direct data fetching, tool calls, code execution, network access, or persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
