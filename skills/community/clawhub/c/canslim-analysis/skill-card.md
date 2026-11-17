## Description:

Executes a hybrid quantitative and qualitative CANSLIM analysis on US stocks using a fixed schema and a modular Python pipeline, returning a ranked shortlist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkmsteven](https://clawhub.ai/user/lkmsteven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to screen US stocks with CANSLIM-style quantitative criteria, enrich candidates with qualitative checks, and generate a ranked shortlist with JSON and PDF reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependency and market-data supply-chain exposure from installing broad dependency ranges.

Mitigation: Install only in the documented virtual environment and review dependency resolution before deployment.

Risk: External public market-data and AI-enrichment processing may produce incomplete, delayed, or incorrect stock analysis.

Mitigation: Treat output as research, review the generated reports before use, and do not rely on results as investment advice.

Risk: Running the analysis with unnecessary local credentials in scope could increase impact if dependencies or external processing are compromised.

Mitigation: Run the skill in a clean environment without unrelated credentials or sensitive files available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkmsteven/skills/canslim-analysis)
- [S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON report files, and a generated PDF report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include intermediate_canslim.json, enriched_canslim.json, final_canslim_report.json, canslim_analysis.log, and Scripts/out/canslim_report_{date}.pdf.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
