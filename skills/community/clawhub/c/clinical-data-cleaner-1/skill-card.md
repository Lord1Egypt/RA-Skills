## Description: <br>
Cleans, validates, and standardizes clinical trial data for CDISC SDTM-oriented regulatory submission workflows, including missing-value handling, outlier detection, date standardization, and audit reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, clinical data managers, and regulatory data teams use this skill to clean CSV or Excel clinical trial datasets, validate supported SDTM domains, flag or handle outliers, standardize dates, and produce an audit report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical trial data can contain sensitive regulated information, and local file outputs may expose or overwrite important datasets if paths and options are not reviewed. <br>
Mitigation: Install and run the skill only in an environment appropriate for sensitive clinical data, confirm input and output paths before execution, avoid overwriting raw datasets, and review the generated audit report. <br>
Risk: Missing-value handling and outlier actions can materially change regulated datasets or produce misleading analysis inputs if used without domain review. <br>
Mitigation: Use conservative settings such as flagging outliers when preparing submission data, validate results against the applicable SDTM requirements, and have qualified reviewers approve cleaning decisions before downstream use. <br>
Risk: Unpinned numerical dependencies can make repeatable regulated workflows harder to reproduce. <br>
Mitigation: Pin vetted versions of numpy, pandas, and scipy for regulated or repeatable workflows and record the runtime environment with the audit artifacts. <br>


## Reference(s): <br>
- [Clinical Data Cleaner Release](https://clawhub.ai/aipoch-ai/clinical-data-cleaner-1) <br>
- [CDISC SDTM Implementation Guide Reference](references/sdtm_ig_guide.md) <br>
- [Domain Specifications](references/domain_specs.json) <br>
- [Clinical Outlier Thresholds](references/outlier_thresholds.json) <br>
- [Common Patterns](references/common-patterns.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Sample Demographics Dataset](references/sample_dm.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python and shell examples; the packaged script can produce cleaned CSV or Excel files and JSON audit reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports DM, LB, and VS domains; configurable missing-value strategy, outlier method, outlier action, and optional JSON configuration path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
