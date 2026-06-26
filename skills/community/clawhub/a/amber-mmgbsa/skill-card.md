## Description: <br>
End-to-end guide for running MM/GBSA binding free energy calculations using AmberTools/Amber on a pre-existing receptor-ligand complex without molecular dynamics sampling, covering structure preparation, ligand parameterization, topology construction, MMPBSA.py execution, and result interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ning-kun](https://clawhub.ai/user/ning-kun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, computational chemists, and developers use this skill to produce a reproducible single-structure Amber MM/GBSA workflow for rapid pose scoring and mechanistic energy decomposition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes shell commands that create and overwrite files inside project directories. <br>
Mitigation: Review commands before running them, work in a dedicated project directory, and keep backups of important input structures and outputs. <br>
Risk: AmberTools commands depend on the local AmberTools installation selected by AMBERHOME. <br>
Mitigation: Confirm AMBERHOME and PATH point to the intended AmberTools installation before executing the workflow. <br>
Risk: Single-structure MM/GBSA results can be misleading for quantitative ranking or comparison with experimental binding free energies. <br>
Mitigation: Use the skill's stated uncertainty boundaries and upgrade to MD-based ensemble MM/GBSA when ranking ligands or making quantitative claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ning-kun/amber-mmgbsa) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ning-kun) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, text, and configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a step-by-step local AmberTools workflow and interpretation guidance; it does not execute commands by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
