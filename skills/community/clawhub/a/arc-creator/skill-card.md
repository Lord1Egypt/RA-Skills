## Description: <br>
Create and populate Annotated Research Contexts (ARCs) following the nfdi4plants ARC specification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IngoGiebel](https://clawhub.ai/user/IngoGiebel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, data stewards, and developers use this skill to create ARC research repositories, collect investigation, study, assay, workflow, run, contact, and publication metadata, and prepare optional DataHUB synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating an ARC in a non-empty or cloud-synced folder can mix unrelated files or cause Git conflicts. <br>
Mitigation: Use a dedicated empty ARC folder and avoid OneDrive, Dropbox, or similar synchronized directories. <br>
Risk: Committing or pushing an ARC can publish unintended files, large data, or sensitive metadata. <br>
Mitigation: Review copied files and git status before git add -A, and configure Git LFS for large assay data before committing. <br>
Risk: DataHUB synchronization can send the ARC to the wrong host or repository visibility level. <br>
Mitigation: Confirm the DataHUB host, remote URL, repository visibility, and token scope before pushing. <br>


## Reference(s): <br>
- [ARC specification reference](references/arc-spec.md) <br>
- [ARC Creator release page](https://clawhub.ai/IngoGiebel/arc-creator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with interactive prompts and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local ARC repository files when the user confirms command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
