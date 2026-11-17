## Description:

Complete workflow for time series datasets (Energy, Manufacturing, Climate) on Kaggle to Data Annotation platform (data.smlcrm.com), including download, pandas-based cleaning, raw and cleaned uploads, column configuration, units, and group assignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deyashmukh](https://clawhub.ai/user/deyashmukh)

### License/Terms of Use:


## Use Case:

Data practitioners, developers, and analysts use this skill to prepare Energy, Manufacturing, and Climate time series CSV datasets from Kaggle for upload and annotation in the Data Annotation platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Kaggle downloader extracts archives and removes zip files in the chosen output directory, which may overwrite or delete unrelated files if the directory is reused.

Mitigation: Run downloads in a fresh empty output directory and inspect the directory before extraction or cleanup.

Risk: The workflow uploads raw and cleaned datasets to an external data annotation platform.

Mitigation: Review dataset license terms, privacy sensitivity, and organizational approval before uploading any data.

Risk: The Kaggle CLI requires local credential configuration.

Mitigation: Install Kaggle tooling in a virtual environment and handle credentials through secure local configuration.

## Reference(s):

- [Data Annotation Platform Configuration Reference](references/platform_guide.md)
- [Data Annotation Platform](https://data.smlcrm.com)
- [Steel Industry Energy Consumption Dataset](https://www.kaggle.com/datasets/csafrit2/steel-industry-energy-consumption)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cleaned CSV files and console column summaries when the bundled cleaning script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
