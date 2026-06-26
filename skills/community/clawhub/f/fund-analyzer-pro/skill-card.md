## Description: <br>
Fund Analyzer Pro helps agents analyze Chinese funds and advisory strategies across single-fund analysis, comparisons, diagnostics, holdings review, manager evaluation, opportunity analysis, investment-method guidance, and monitoring alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce fund analysis reports, compare funds, diagnose portfolio holdings, evaluate fund managers, inspect fees, and monitor fund-related signals. It is suited for finance-analysis workflows where outputs must cite data availability and remain non-binding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release handles sensitive portfolio and holdings data and may store cache or holdings files locally. <br>
Mitigation: Use encrypted storage where available, avoid plaintext holdings export for real portfolios, and review or clear local OpenClaw data files after analysis. <br>
Risk: The release contacts external fund services and evidence notes live-looking API credentials. <br>
Mitigation: Rotate or replace bundled keys, provide secrets through environment variables or a secure secret manager, and limit network/API access to approved services. <br>
Risk: Generated reports can affect investment decisions and may depend on unavailable, stale, or estimated data. <br>
Mitigation: Require source and timestamp disclosure, preserve the non-investment-advice disclaimer, and have users verify data before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/fund-analyzer-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lj22503) <br>
- [Data Sources Guide](references/data-sources-guide.md) <br>
- [Fund Fee Analysis](references/fund-fee-analysis.md) <br>
- [Fund Manager Evaluation](references/fund-manager-evaluation.md) <br>
- [Fund Report Template](templates/fund-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, alerts, configuration snippets, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external fund-service results, local cache state, and user-supplied holdings data when configured.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release evidence and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
