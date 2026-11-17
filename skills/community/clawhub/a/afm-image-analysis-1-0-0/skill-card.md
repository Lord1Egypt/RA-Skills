## Description:

Analyze AFM images to compute surface roughness, detect nanoparticles, extract line profiles, generate 3D renderings, and process batches with detailed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xrayxiaoruiyang-pixel](https://clawhub.ai/user/xrayxiaoruiyang-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, lab engineers, and developers use this skill to run local AFM image analysis for roughness measurement, nanoparticle statistics, line-profile extraction, 3D visualization, and batch comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive batch mode can process many matching files below the selected directory and create analysis artifacts there.

Mitigation: Use explicit input folders and output directories, and review the directory scope before enabling recursive mode.

Risk: Image-based height mapping depends on calibration, and grayscale inputs default to a 1 gray-level to 1 nm scale unless overridden.

Mitigation: Set the scale parameter from instrument calibration before relying on quantitative height or roughness values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xrayxiaoruiyang-pixel/skills/afm-image-analysis-1-0-0)
- [Publisher profile](https://clawhub.ai/user/xrayxiaoruiyang-pixel)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files, JSON, CSV, Images]

**Output Format:** [Markdown guidance with bash commands; generated analysis artifacts include PNG images, CSV tables, and JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-selected AFM data and writes per-file output directories plus a batch summary CSV.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
