## Description:

Professional personal finance advisor specializing in plain-text accounting with Beancount and Fava.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y1feng200156](https://clawhub.ai/user/y1feng200156)

### License/Terms of Use:

GNU General Public License v3.0

## Use Case:

External users and agents use this skill to analyze Beancount ledgers, interpret Fava reports, write BQL queries, organize accounts, and produce educational personal finance guidance from user-provided data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included analysis script can load Beancount ledgers whose plugin or include directives may trigger unsafe or unexpected behavior.

Mitigation: Run the script only on trusted personal ledgers, or use a sandbox and review plugin/include directives before analysis.

Risk: Ledger files contain sensitive financial records.

Mitigation: Limit access to necessary files, avoid sharing third-party ledgers, and remove private account details before using outputs outside the trusted environment.

Risk: Financial, tax, or investment outputs may be incomplete or unsuitable for a user's circumstances.

Mitigation: Treat outputs as educational analysis and verify major decisions with qualified financial, tax, or investment professionals.

## Reference(s):

- [Personal Finance Beancount on ClawHub](https://clawhub.ai/y1feng200156/skills/beancount-skill)
- [Beancount documentation](https://beancount.github.io/docs/index.html)
- [Fava documentation](https://beancount.github.io/fava/)
- [Beancount syntax reference](artifact/references/beancount_syntax.md)
- [Beancount query reference](artifact/references/beancount_query.md)
- [Fava features reference](artifact/references/fava_features.md)
- [Fava dashboards reference](artifact/references/fava_dashboards.md)
- [Financial analysis guide](artifact/references/financial_analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with Beancount, BQL, Python, and shell code blocks when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May analyze user-provided Beancount files with the included Python script when appropriate.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
