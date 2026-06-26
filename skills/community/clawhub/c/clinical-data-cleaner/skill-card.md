## Description: <br>
Cleans, validates, and standardizes clinical trial data for CDISC SDTM-oriented workflows, including missing value handling, outlier detection, date standardization, and audit report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renhaosu2024](https://clawhub.ai/user/renhaosu2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical programmers, data managers, and developers use this skill to prepare clinical trial datasets for SDTM-oriented review, analysis, migration, or submission workflows. It helps validate required DM, LB, and VS fields, standardize dates, handle missing values, detect outliers, and generate an audit report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical cleaning actions can alter trial datasets in ways that affect analysis or submission decisions. <br>
Mitigation: Run the tool on copies of raw data, keep raw clinical data unchanged, review audit reports, and require independent clinical, statistical, or regulatory QC before relying on results. <br>
Risk: Removing or capping outliers can discard or change clinically meaningful values. <br>
Mitigation: Prefer flagging outliers unless removal or capping is explicitly approved for the study workflow. <br>
Risk: Outputs may contain PHI or trial identifiers. <br>
Mitigation: Protect input and output files in a controlled environment and apply the organization's handling requirements for clinical data. <br>
Risk: Unpinned dependencies can change runtime behavior over time. <br>
Mitigation: Pin and review dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/renhaosu2024/clinical-data-cleaner) <br>
- [CDISC SDTM Implementation Guide Reference](references/sdtm_ig_guide.md) <br>
- [Domain-specific field requirements](references/domain_specs.json) <br>
- [Clinical outlier thresholds](references/outlier_thresholds.json) <br>
- [Common usage patterns](references/common-patterns.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Sample demographics dataset](references/sample_dm.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and bash examples; executed workflows can produce CSV or Excel datasets and JSON audit reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports DM, LB, and VS SDTM domains; runtime behavior depends on selected missing-value and outlier handling options.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
