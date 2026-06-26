## Description: <br>
Official-style Amber24 molecular dynamics workflow guide for proteins with an end-to-end procedure, command templates, input-file templates, and a manual example from PDB download through RMSD/RMSF analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ning-kun](https://clawhub.ai/user/ning-kun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and scientific researchers use this skill as a manual Amber24 and AmberTools24 workflow reference for preparing protein systems, running minimization, heating, equilibration, production MD, and analyzing trajectories with cpptraj. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide contains shell commands that create files, run Amber tools, and can consume local compute and storage. <br>
Mitigation: Run commands deliberately in a dedicated project directory and confirm expected paths, runtime, and storage before starting MD jobs. <br>
Risk: Incorrect or untrusted Amber or AmberTools installations could affect reproducibility or system integrity. <br>
Mitigation: Verify Amber and AmberTools installation sources and environment configuration before using the workflow. <br>
Risk: Unsupported ligands, cofactors, metal centers, or nonstandard residues can make the baseline protein-only workflow scientifically invalid. <br>
Mitigation: Inspect structures before simulation and either remove unsupported components for a protein-only baseline or parameterize them with appropriate Amber workflows. <br>


## Reference(s): <br>
- [Amber MD Parameter Guide](references/amber_parameter_guide.md) <br>
- [cpptraj Analysis Guide](references/cpptraj_analysis_guide.md) <br>
- [RCSB PDB 1AKI Download](https://files.rcsb.org/download/1AKI.pdb) <br>
- [ClawHub Skill Page](https://clawhub.ai/ning-kun/amber-md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and input-file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable automation scripts are bundled.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
