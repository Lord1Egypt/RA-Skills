## Description: <br>
Financial Audit Domain provides a financial statement risk-screening reference library for non-financial A-share listed companies, covering six audit domains, 50 core indicators, and five fraud red-line checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to structure financial statement risk-screening workflows for non-financial A-share listed companies, including solvency, asset quality, profitability, cash-flow quality, and fraud red-line checks. It can guide report generation when its required execution dependency is available, or serve as read-only audit reference material otherwise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports automatic dependency installation and broader execution behavior without a clear approval step. <br>
Mitigation: Review the skill before installation, prefer a version that asks before installing Universal Task OS, and run it in an environment where dependency installation is explicitly controlled. <br>
Risk: The skill can run local scripts that fetch public financial data and write analysis reports. <br>
Mitigation: Inspect script inputs and outputs before execution, use trusted public-data sources, and review generated reports before relying on them for decisions. <br>
Risk: The skill is scoped to non-financial A-share listed companies and may produce misleading analysis outside that scope. <br>
Mitigation: Use it only for supported non-financial A-share issuers and apply separate domain-specific review for banks, insurers, securities firms, or other unsupported entities. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/financial-audit-domain) <br>
- [Audit Catalog](references/audit-catalog.md) <br>
- [Audit Requirements](references/audit-requirements.md) <br>
- [Exemplars](references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with optional script-generated JSON, Markdown, and HTML report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for consolidated-statement, four-period analysis of non-financial A-share listed companies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
