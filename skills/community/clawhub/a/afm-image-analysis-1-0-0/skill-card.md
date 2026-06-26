## Description: <br>
Analyze AFM images to compute surface roughness, detect nanoparticles, extract line profiles, generate 3D renderings, and process batches with detailed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrayxiaoruiyang-pixel](https://clawhub.ai/user/xrayxiaoruiyang-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, lab analysts, and developers use this skill to run local AFM image analysis for roughness metrics, particle statistics, line-profile extraction, 3D surface visualization, and batch comparison reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Report files may be overwritten when the same output directory and input names are reused. <br>
Mitigation: Choose an output directory deliberately and keep separate directories for separate runs when preserving previous reports matters. <br>
Risk: Recursive batch mode can process more local files than intended if pointed at a broad or private directory. <br>
Mitigation: Run recursive mode only on a scoped AFM data folder and review the input path before execution. <br>
Risk: Grayscale image inputs default to a simple height scale when calibration is not supplied. <br>
Mitigation: Provide the correct scale factor for calibrated image data before using numeric height or roughness values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xrayxiaoruiyang-pixel/afm-image-analysis-1-0-0) <br>
- [Skill usage documentation](artifact/SKILL.md) <br>
- [AFM analysis script](artifact/scripts/analyze_afm.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration] <br>
**Output Format:** [Text guidance with shell commands; generated analysis files include PNG, CSV, and JSON reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local AFM arrays, text matrices, and grayscale images, then writes per-input output directories plus an optional batch summary CSV.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
