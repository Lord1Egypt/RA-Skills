## Description:

Analyze 23andMe raw genome data to generate comprehensive health, trait, and family comparison reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nomadrex](https://clawhub.ai/user/nomadrex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run local educational analysis of 23andMe raw genome files, generate health and trait summaries, and compare genome files in family mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive DNA and health data may be processed or exposed without proper authorization.

Mitigation: Use only genome files you are authorized to process and keep reports in controlled local storage.

Risk: Family comparison can process genome files from multiple people without clear consent.

Mitigation: Run family comparison only after each person's consent has been obtained.

Risk: Report content may be mistaken for medical or medication guidance.

Mitigation: Treat results as rough educational summaries and do not use them for medical, medication, or clinical decisions.

Risk: Generated HTML reports from untrusted genome files may be unsafe until escaping and validation are fixed.

Mitigation: Avoid opening generated HTML reports from untrusted genome files; review and validate inputs before HTML use.

## Reference(s):

- [SNP database](references/snp_database.json)
- [ClawHub skill page](https://clawhub.ai/nomadrex/skills/genome-report)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML, Files]

**Output Format:** [Plain text, JSON, or HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write HTML reports to a path and compare multiple genome files in family mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
