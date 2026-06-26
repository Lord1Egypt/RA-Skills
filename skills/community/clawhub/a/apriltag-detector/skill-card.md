## Description: <br>
AprilTag corner detection for camera calibration and pose estimation, including image inputs from file paths or numpy arrays, result drawing, and automatic installation of the detection library through gettool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when working with pywayne.cv.apriltag_detector to detect AprilTag fiducial markers in images for camera calibration, pose estimation, and visualization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The detector may automatically fetch the apriltag_detection dependency through gettool when the dependency is missing. <br>
Mitigation: Use the skill in a virtual environment and confirm that gettool and the dependency source are trusted or pinned before running detection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/apriltag-detector) <br>
- [Publisher profile](https://clawhub.ai/user/wangyendt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use detector methods that return tag IDs, hamming distance, center coordinates, corners, and optional annotated images.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
