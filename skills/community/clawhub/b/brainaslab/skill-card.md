## Description: <br>
Automatically analyzes FreeSurfer cortical stats files to compute asymmetry indices and generate CSV results with plots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxxx536](https://clawhub.ai/user/xxxx536) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Neuroimaging researchers and developers use this skill to process paired FreeSurfer lh.aparc.stats and rh.aparc.stats files, compute cortical asymmetry indices for thickness, area, and volume, and collect CSV and plot outputs for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input paths are interpolated into MATLAB code and could be interpreted as code. <br>
Mitigation: Use only trusted file paths in a contained working directory until argument handling is fixed. <br>
Risk: The MATLAB analyzer source is not packaged for review. <br>
Mitigation: Request the analyzer source from the publisher and review it before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xxxx536/brainaslab) <br>


## Skill Output: <br>
**Output Type(s):** [Files, CSV, Images] <br>
**Output Format:** [Python dictionary with file paths to generated CSV and PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATLAB available in PATH and paired FreeSurfer stats inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
