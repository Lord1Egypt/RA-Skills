## Description: <br>
Generates local data-analysis reports for common dataset formats, including data quality checks, statistical summaries, visualizations, key insights, and Chinese-language recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiyongwang](https://clawhub.ai/user/ruiyongwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data analysts, business users, and developers use this skill to inspect local datasets and generate Chinese-language reports with quality checks, statistics, visual summaries, insights, and actionable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes local datasets that may contain sensitive or regulated information. <br>
Mitigation: Run it in a virtual environment, invoke it deliberately for sensitive files, and rely on local file-system permissions for dataset access. <br>
Risk: Generated statistics, insights, and recommendations may be incomplete or misleading if the input data is poor quality or sampled. <br>
Mitigation: Review the generated report, validate data quality findings, and confirm recommendations before using them for decisions. <br>
Risk: Future versions that add scheduling, email delivery, API integration, or automatic cleanup could change the security posture. <br>
Mitigation: Re-review and rescan future versions before deployment when those behaviors are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruiyongwang/data-analysis-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports with structured analysis summaries and chart/report file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local processing; report contents depend on the supplied dataset, selected report template, and available Python analysis libraries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
