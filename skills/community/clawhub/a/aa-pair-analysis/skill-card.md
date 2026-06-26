## Description: <br>
Analyzes functional amino-acid adjacent-pair frequencies across protein-family sequences by running MSA, extracting consensus sequences, computing Top 5 pair types and phi values, and generating formulation outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhen9nine](https://clawhub.ai/user/wuhen9nine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bioinformatics developers and protein-analysis users use this skill to run amino-acid pair-frequency workflows on protein families, compare pair composition across species or groups, and generate CSV and Word formulation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can fetch a ClustalOmega executable over plain HTTP and make persistent shell changes. <br>
Mitigation: Review scripts/setup.sh before installation, prefer installing ClustalOmega from a trusted package manager or verified release, and confirm whether shell startup files were modified. <br>
Risk: Some helper scripts include hard-coded /home/lenovo/.openclaw paths that may not match the target runtime. <br>
Mitigation: Confirm and adjust local paths before running PDF or report-update helpers. <br>


## Reference(s): <br>
- [Complete Analysis Method](references/method.md) <br>
- [Amino Acid Functional Classification](references/classification.md) <br>
- [Clustal Omega](http://www.clustal.org/omega/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python workflow scripts, CSV outputs, JSON intermediate data, and Word document reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces species-level formulation CSV files, Top 5 pair detail CSV files, summary CSV files, integrated reports, and optional monomer formulation tables.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
