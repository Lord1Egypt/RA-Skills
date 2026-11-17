## Description:

Generate dynamic-object binary masks after global motion compensation, output CSR sparse format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design motion-compensated moving-object masks for video frames where camera motion would otherwise create false foreground detections. It guides thresholding, morphology, area filtering, and CSR encoding for sampled-frame mask outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect path, dependency, or array-shape handling in a downstream implementation could produce unusable masks or malformed CSR data.

Mitigation: Review the eventual implementation's input and output paths, OpenCV dependency usage, and CSR invariants before deployment.

Risk: Camera-motion compensation can mark border fill or alignment artifacts as foreground.

Mitigation: Compute threshold statistics only on the warped valid region and verify that border fill is excluded from foreground masks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/dynamic-object-aware-egomotion-dyn-object-masks)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with Python code sketch and checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for binary masks encoded as CSR arrays with per-frame data, indices, indptr, and shape metadata.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
