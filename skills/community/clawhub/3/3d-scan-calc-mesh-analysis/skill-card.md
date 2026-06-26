## Description: <br>
Analyzes 3D mesh files (STL) to calculate geometric properties (volume, components) and extract attribute data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect STL mesh files, isolate the largest connected component from noisy scans, calculate mesh volume, and extract binary STL attribute data such as material IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs third-party Python locally against user-provided STL files. <br>
Mitigation: Install and run it only in environments where local third-party Python execution is acceptable, and provide only STL files intentionally selected for analysis. <br>
Risk: Volume values use the STL coordinate units cubed, so mass calculations can be wrong if coordinate units are assumed. <br>
Mitigation: Verify the STL coordinate units and use density data in matching units before multiplying volume by density. <br>
Risk: The documented import path may not match every Codex or OpenClaw installation. <br>
Mitigation: Adjust the local scripts path for the target agent environment before importing MeshAnalyzer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/3d-scan-calc-mesh-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python module usage guidance and dictionary-like analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The analyzer returns main_part_volume, main_part_material_id, and total_components for the largest connected component.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
