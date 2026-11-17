## Description:

Analyzes 3D mesh files (STL) to calculate geometric properties, identify connected components, and extract STL attribute data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze STL meshes from 3D scans, isolate the largest connected component, compute volume, and read material or color attribute IDs for downstream calculations such as mass estimation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed, adversarial, or extremely large STL files could stall or exhaust resources during local parsing and connected-component analysis.

Mitigation: Run the skill with external CPU and memory limits and avoid direct processing of untrusted or oversized mesh files.

Risk: Mass or dimensional conclusions can be wrong if users assume coordinate units or mix incompatible density units.

Mitigation: Confirm the STL coordinate system and use density data expressed in matching units before calculating mass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/3d-scan-calc-mesh-analysis)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [Python module usage guidance and dictionary-style analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports largest-component volume, material attribute ID, and component count; volume remains in the STL coordinate units cubed.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
