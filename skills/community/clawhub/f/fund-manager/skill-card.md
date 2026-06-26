## Description: <br>
Fund Manager is a finance research assistant for monitoring a small fund portfolio, analyzing market conditions, producing investment reports, and suggesting risk-aware portfolio adjustments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amateur6](https://clawhub.ai/user/amateur6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill as a fund and market research assistant to review holdings, monitor daily fund performance, analyze macro and technical signals, and draft portfolio reports or rebalancing suggestions. Its financial outputs should be treated as research support rather than personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides actionable fund allocations, buy or sell signals, and named fund suggestions that may be unsuitable or inaccurate for a user's financial situation. <br>
Mitigation: Treat outputs as unverified research, review recommendations independently, and consult qualified financial guidance before acting on investment decisions. <br>
Risk: The skill may read local portfolio-memory files and write financial reports that could expose sensitive balances or account details. <br>
Mitigation: Keep sensitive account information out of persistent memory unless intentionally stored, and review generated reports before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/amateur6/fund-manager) <br>
- [Buffett Core Reference](references/buffett-core.md) <br>
- [Financial Metrics Reference](references/financial-metrics.md) <br>
- [Fund Framework Reference](references/fund-framework.md) <br>
- [Macro Indicators Reference](references/macro-indicators.md) <br>
- [Technical Analysis Reference](references/technical-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with tables, concise recommendations, and optional shell commands for related data tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local portfolio-memory files and write financial report files when the user authorizes those actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
