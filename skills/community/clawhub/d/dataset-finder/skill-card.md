## Description:

Dataset Finder helps agents find, download, preview, and document datasets from repositories such as Kaggle, Hugging Face, and UCI ML Repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anisafifi](https://clawhub.ai/user/anisafifi)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and data practitioners use this skill to discover candidate datasets, download repository-hosted data, inspect local dataset structure and statistics, and generate dataset-card Markdown for machine learning projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote dataset loading can retrieve untrusted or unexpected data.

Mitigation: Run the skill in a virtual environment or container and use trusted dataset identifiers before downloading or loading data.

Risk: Preview and data-card commands can expose raw rows from private or sensitive datasets.

Mitigation: Avoid previewing private datasets unless sample rows are safe to display, and review generated data cards before sharing or committing them.

Risk: Local file reads and writes have weak scoping and can affect user-selected paths.

Mitigation: Run from a dedicated project directory, set output paths deliberately, and inspect generated files before reuse.

Risk: Some documentation appears broader than the implemented command surface.

Mitigation: Confirm available commands with the script help output before relying on documented advanced workflows.

## Reference(s):

- [Dataset Finder README](references/readme.md)
- [OpenClawCLI](https://clawhub.ai/)
- [Kaggle API](https://github.com/Kaggle/kaggle-api)
- [Hugging Face Datasets documentation](https://huggingface.co/docs/datasets/)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/)
- [Data.gov APIs](https://www.data.gov/developers/apis)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; invoked commands can produce terminal text, JSON result files, downloaded data files, and dataset-card Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local files under user-selected output paths and previews containing sample rows from datasets.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
