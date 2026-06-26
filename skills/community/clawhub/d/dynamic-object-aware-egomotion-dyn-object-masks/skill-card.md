## Description: <br>
Generate dynamic-object binary masks after global motion compensation, output CSR sparse format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computer-vision engineers use this skill to detect moving objects in scenes with camera motion and produce sparse binary masks aligned to sampled frames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local environment may be missing the numpy or OpenCV dependencies needed to apply the guidance. <br>
Mitigation: Confirm numpy and OpenCV are available before use. <br>
Risk: Mask quality can be degraded if border fill, noise, or small components are treated as foreground. <br>
Mitigation: Use the valid-region mask, adaptive median/MAD thresholding, morphology, connected-component area filtering, and CSR self-checks described by the artifact. <br>
Risk: Video frames may contain data the user does not want processed. <br>
Mitigation: Process only frames the user is comfortable handling locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/dynamic-object-aware-egomotion-dyn-object-masks) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code] <br>
**Output Format:** [Markdown with Python code sketch] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for CSR sparse mask fields including data, indices, indptr, and shape.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
