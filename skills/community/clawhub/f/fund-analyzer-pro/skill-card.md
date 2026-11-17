## Description:

Fund Analyzer Pro helps agents analyze funds and advisory strategies through fund reports, comparisons, portfolio and holding diagnosis, fund manager evaluation, fee review, opportunity analysis, and monitoring alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce fund analysis reports, compare funds, diagnose portfolios and holdings, evaluate fund managers, analyze fees, and monitor important fund or strategy signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial data may be processed through external APIs, cached locally, or monitored through a watchlist.

Mitigation: Use the skill only with data-sharing consent, minimize uploaded holdings data, review local storage behavior, and remove cached or watchlist data that is no longer needed.

Risk: Credentials or bundled API keys may be exposed or reused insecurely.

Mitigation: Rotate or replace the bundled Qieman key, keep real secrets out of workspace documentation and shell profiles, and use a controlled secret-management path where possible.

Risk: Plaintext holdings exports can expose private portfolio information.

Mitigation: Avoid plaintext holdings exports in shared workspaces, encrypt holdings files when storage is required, and review storage scripts before processing uploaded portfolio files.

## Reference(s):

- [Data Sources Guide](artifact/references/data-sources-guide.md)
- [Fund Fee Analysis Framework](artifact/references/fund-fee-analysis.md)
- [Fund Manager Evaluation System](artifact/references/fund-manager-evaluation.md)
- [Fund Report Template](artifact/templates/fund-report-template.md)
- [Fund Diagnosis Case](artifact/examples/fund-diagnosis-case.md)
- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/fund-analyzer-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fund analysis tables, risk notices, data-source status, watchlist alerts, and code or configuration examples.]

## Skill Version(s):

2.1.3 (source: server release metadata and artifact clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
