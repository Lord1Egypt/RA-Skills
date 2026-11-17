## Description:

Aa Pair Analysis analyzes amino-acid functional-category adjacent-pair frequencies across protein-family sequences using MSA, consensus extraction, pair statistics, phi-value calculation, and formulation table generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhen9nine](https://clawhub.ai/user/wuhen9nine)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and developers use this skill to run protein-family amino-acid adjacent-pair analyses from FASTA inputs, compare species or groups, and generate Top 5 pair and phi-value summaries. The skill can also help produce monomer formulation tables from integrated analysis results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can fetch and enable an executable insecurely and modify the user's shell environment without enough control.

Mitigation: Review before installing; install dependencies manually from trusted package managers or an isolated virtual environment, avoid the HTTP binary fallback, and do not allow automatic shell profile edits.

Risk: Generated CSV files can be unsafe to open directly in spreadsheet software if task or output data is not trusted.

Mitigation: Use simple task names without slashes or '..' and inspect generated CSV files before opening them in spreadsheets.

Risk: Laboratory formulation tables may contain incorrect or incomplete values for real-world use.

Mitigation: Independently validate any laboratory formulation tables before use.

## Reference(s):

- [Complete analysis method](references/method.md)
- [Amino-acid functional classification](references/classification.md)
- [Clustal Omega](http://www.clustal.org/omega/)
- [ClawHub skill page](https://clawhub.ai/wuhen9nine/skills/aa-pair-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; generated CSV, JSON, and Word document outputs from scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary analysis outputs include species_formulations.csv, top_5_pairs_details.csv, formulation_summary.csv, integrated result reports, and monomer formulation tables.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
