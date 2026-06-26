## Description: <br>
Detect and tightly annotate tower-crane hook outlines in similar construction-site monitoring images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genlk](https://clawhub.ai/user/genlk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site-monitoring teams use this skill to batch-process stable construction-camera images, outline tower-crane hooks with a strict polygon, and export annotated images plus coordinate metadata for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick-start commands reference a local PowerShell script that is not included in the provided artifact. <br>
Mitigation: Confirm the script exists, inspect it before execution, and run it only against image folders you choose. <br>
Risk: Using ExecutionPolicy Bypass can run untrusted PowerShell code if the script source has not been verified. <br>
Mitigation: Avoid ExecutionPolicy Bypass for unreviewed scripts and follow local PowerShell execution policies. <br>


## Reference(s): <br>
- [Profile Tuning](references/profile-tuning.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with PowerShell command examples and JSON profile guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying workflow writes annotated images, optional debug ROI crops, and a manifest JSON when the referenced annotation script is present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
