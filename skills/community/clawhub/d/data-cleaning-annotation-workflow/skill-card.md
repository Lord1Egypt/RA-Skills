## Description: <br>
Complete workflow for time series datasets from Kaggle to the Data Annotation platform, including downloading, pandas-based cleaning, raw and cleaned uploads, metadata configuration, units, column types, and group assignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Deyashmukh](https://clawhub.ai/user/Deyashmukh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data practitioners, and dataset curators use this skill to prepare time series datasets for ML workflows on the Data Annotation platform. It guides dataset discovery, download, cleaning, metadata setup, group assignment, and final upload to CLEAN status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses Kaggle downloads and uploads data to data.smlcrm.com. <br>
Mitigation: Use public or approved datasets and upload sensitive data only when the destination platform is authorized for that data. <br>
Risk: The Kaggle downloader installs or relies on local dependencies and extracts downloaded ZIP files. <br>
Mitigation: Run the downloader in a trusted environment and a new empty folder so extraction and cleanup do not affect unrelated files. <br>
Risk: Local dataset cleaning changes CSV contents by filling missing values, removing duplicates, and normalizing timestamps. <br>
Mitigation: Review the generated column summary and cleaned output before upload, and keep the original raw CSV for comparison. <br>


## Reference(s): <br>
- [Data Annotation Platform Configuration Reference](references/platform_guide.md) <br>
- [Data Annotation Platform](https://data.smlcrm.com) <br>
- [Steel Industry Energy Consumption dataset example](https://www.kaggle.com/datasets/csafrit2/steel-industry-energy-consumption) <br>
- [ClawHub skill page](https://clawhub.ai/Deyashmukh/data-cleaning-annotation-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with inline shell commands, CSV-cleaning code usage, and platform configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce cleaned CSV files and console column summaries when the included cleaning script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
