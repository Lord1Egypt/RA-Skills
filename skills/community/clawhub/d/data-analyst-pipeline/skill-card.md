## Description:

Automates a data-analysis pipeline from CSV, Excel, JSON, or SQLite ingestion through quality audit, cleaning, exploratory analysis, visualization, and HTML report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to run a repeatable local data-analysis workflow that loads tabular data, audits quality, cleans data, performs EDA, creates charts, and builds a shareable HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can render untrusted dataset text as active browser content.

Mitigation: Use trusted datasets, or sanitize and HTML-escape dataset values before opening generated reports in a browser.

Risk: Local report, chart, and summary files may retain sensitive dataset contents after analysis.

Mitigation: Write outputs only to approved local directories and delete or protect generated files according to the dataset's sensitivity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/data-analyst-pipeline)
- [README](README.md)
- [Business Rules Configuration](config/business_rules.yaml)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python and shell commands; generated artifacts include HTML reports, PNG charts, and JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local report, chart, and summary files; large datasets may be sampled when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
