## Description:

AprilTag corner detection for camera calibration and pose estimation with pywayne.cv.apriltag_detector, including image inputs from file paths or numpy arrays, detection visualization, and automatic library installation via gettool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when they need an agent to help detect AprilTag fiducial markers in images, visualize detected corners and IDs, and interpret detection fields for camera calibration or pose-estimation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use may download and install unpinned third-party code through gettool with the same permissions as the running agent.

Mitigation: Install or run the skill only in a virtual environment or contained workspace, and consider preinstalling a reviewed, pinned apriltag_detection dependency.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python code snippets and structured detection-result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe automatic installation of the apriltag_detection dependency through gettool.]

## Skill Version(s):

0.1.0 (source: server release metadata, released 2026-02-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
