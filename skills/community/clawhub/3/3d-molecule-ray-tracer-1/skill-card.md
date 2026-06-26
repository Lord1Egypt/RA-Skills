## Description: <br>
Generate photorealistic rendering scripts for PyMOL and UCSF ChimeraX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and visualization specialists use this skill to generate PyMOL or UCSF ChimeraX scripts for publication-quality molecular renders from a PDB ID or structure file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .pml or .cxc files are intended to be run by external visualization tools. <br>
Mitigation: Review generated scripts before execution and run them only with trusted PyMOL or ChimeraX installations. <br>
Risk: Rendering workflows may fetch public PDB structures when a four-character PDB ID is used. <br>
Mitigation: Expect network access only for public structure retrieval, or provide local PDB files when offline or network-restricted operation is required. <br>
Risk: The skill writes generated scripts to user-selected output paths. <br>
Mitigation: Keep output paths inside the workspace and avoid overwriting important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/3d-molecule-ray-tracer-1) <br>
- [PyMOL](https://pymol.org/) <br>
- [UCSF ChimeraX](https://www.cgl.ucsf.edu/chimerax/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with generated PyMOL .pml or ChimeraX .cxc script files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scripts write image render commands for separately installed PyMOL or ChimeraX.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
