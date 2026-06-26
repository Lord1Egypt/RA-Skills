## Description: <br>
AR Collections & Aging Analysis runs a QBO accounts receivable pipeline that produces a 7-tab Excel workbook with aging buckets, DSO, collection priority scoring, bad debt reserve, payment patterns, and CDC movement tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting and finance users use this skill to run QBO accounts receivable aging, collections analysis, DSO tracking, and bad debt reserve calculations for month-end, auditor, investor, or collections review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated Excel workbook and .cache/ar-collections data can contain sensitive client financial records. <br>
Mitigation: Install and run the skill only in a trusted accounting workspace, treat generated reports and cache files as sensitive records, and apply appropriate retention or deletion controls after use. <br>
Risk: Running the pipeline with the wrong client slug, QBO mode, permissions, or output directory can produce reports for the wrong environment or store them in an unintended location. <br>
Mitigation: Before execution, confirm the client slug, production versus sandbox mode, QBO permissions, and output directory. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated XLSX workbook and JSON cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a 7-tab Excel workbook under reports/ar-collections and stores CDC state in .cache/ar-collections.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
