## Description: <br>
Professional personal finance advisor specializing in plain-text accounting with Beancount and Fava. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y1feng200156](https://clawhub.ai/user/y1feng200156) <br>

### License/Terms of Use: <br>
GNU General Public License v3.0 <br>


## Use Case: <br>
External users and finance-focused operators use this skill to analyze Beancount ledgers, interpret Fava reports, create Beancount entries and queries, and receive financial education for budgeting, planning, and investment concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt an agent to read sensitive personal finance ledger files selected by the user. <br>
Mitigation: Install only if comfortable sharing selected Beancount data with the agent, and prefer sanitized or narrowed ledger excerpts for sensitive questions. <br>
Risk: Financial, investment, or tax guidance may be incomplete or unsuitable for major decisions. <br>
Mitigation: Treat outputs as education and analysis, and verify major financial or tax decisions with a qualified professional. <br>
Risk: The analysis workflow may require local command execution and Python dependencies. <br>
Mitigation: Review local commands before running them and install Python dependencies only from trusted sources. <br>


## Reference(s): <br>
- [Skill README](artifact/README.md) <br>
- [Beancount Syntax Reference](artifact/references/beancount_syntax.md) <br>
- [Beancount Query Language Reference](artifact/references/beancount_query.md) <br>
- [Fava Reference](artifact/references/fava_features.md) <br>
- [Fava Dashboards Reference](artifact/references/fava_dashboards.md) <br>
- [Financial Analysis Reference](artifact/references/financial_analysis.md) <br>
- [Beancount Documentation](https://beancount.github.io/docs/index.html) <br>
- [Fava Documentation](https://beancount.github.io/fava/) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Beancount, BQL, Python, and shell command examples when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May analyze user-selected local Beancount files through the included Python helper script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
