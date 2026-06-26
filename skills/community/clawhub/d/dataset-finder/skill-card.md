## Description: <br>
Use this skill when users need to search for datasets, download data files, or explore data repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anisafifi](https://clawhub.ai/user/anisafifi) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, data scientists, and ML practitioners use this skill to find datasets, download them from supported repositories, preview local data files, and generate dataset documentation for machine learning work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository access may require Kaggle or Hugging Face credentials. <br>
Mitigation: Install in a virtual environment and keep tokens or kaggle.json out of source control and shared logs. <br>
Risk: Downloaded datasets may be large, licensed differently, or unsuitable for the intended use. <br>
Mitigation: Download into a dedicated project directory and review dataset size, metadata, license, and citation requirements before use. <br>
Risk: Preview and generated data-card files may include raw sample rows from a dataset. <br>
Mitigation: Review generated previews and data cards before sharing them outside the project. <br>


## Reference(s): <br>
- [Dataset Finder README](references/readme.md) <br>
- [Dataset Finder on ClawHub](https://clawhub.ai/anisafifi/dataset-finder) <br>
- [Kaggle API](https://github.com/Kaggle/kaggle-api) <br>
- [Hugging Face Datasets Documentation](https://huggingface.co/docs/datasets/) <br>
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/) <br>
- [Data.gov APIs](https://www.data.gov/developers/apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, generated dataset cards, tabular previews, and optional JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download dataset files and write local previews or data-card files when the user runs the provided commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and references/readme.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
