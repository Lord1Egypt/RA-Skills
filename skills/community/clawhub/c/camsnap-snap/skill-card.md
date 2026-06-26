## Description: <br>
Take webcam snapshots with path validation, safe resource handling, and flexible output options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can ask an agent to capture a webcam snapshot, choose an output directory or image path, and optionally configure the camera index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a local webcam and save captured images when invoked. <br>
Mitigation: Install and run it only in environments where webcam capture is expected, and invoke it only for explicit snapshot requests. <br>
Risk: Output path validation is not a strict filesystem sandbox. <br>
Mitigation: Use explicit trusted output paths or directories and rely on caller-side filesystem controls for sandbox boundaries. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [Saved image file with a returned file path string or CLI status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, opencv-python, and webcam access; supported image extensions are .jpg, .jpeg, .png, .bmp, and .webp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
