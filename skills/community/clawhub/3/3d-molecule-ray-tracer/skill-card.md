## Description: <br>
Generate photorealistic rendering scripts for PyMOL and UCSF ChimeraX to create publication-quality molecular visualizations with ray tracing, depth of field, ambient occlusion, and cinematic lighting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renhaosu2024](https://clawhub.ai/user/renhaosu2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and visualization specialists use this skill to generate PyMOL or ChimeraX scripts for high-impact molecular structure images. It is intended for publication figures, covers, and presentations, not routine structural analysis or measurements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .pml or .cxc scripts may include user-provided PDB paths, output filenames, colors, or selection strings. <br>
Mitigation: Inspect generated scripts before running them when inputs came from untrusted text. <br>
Risk: The skill documentation mentions installing Python requirements, but no requirements.txt is included in the artifact. <br>
Mitigation: Do not run the documented requirements install unless a visible, trusted requirements.txt is present. <br>
Risk: Rendering depends on separately installed PyMOL or ChimeraX, and high-quality renders can be slow or resource intensive. <br>
Mitigation: Confirm the target renderer is installed and choose an appropriate preset or resolution for the available workstation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renhaosu2024/3d-molecule-ray-tracer) <br>
- [Publisher profile](https://clawhub.ai/user/renhaosu2024) <br>
- [PyMOL](https://pymol.org/) <br>
- [UCSF ChimeraX](https://www.cgl.ucsf.edu/chimerax/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration] <br>
**Output Format:** [PyMOL .pml or ChimeraX .cxc script files with console guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scripts can render PNG images in separately installed PyMOL or ChimeraX.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
