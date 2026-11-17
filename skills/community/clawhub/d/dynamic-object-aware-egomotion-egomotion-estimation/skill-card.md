## Description:

Estimate camera motion with optical flow + affine/homography, allow multi-label per frame.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computer vision engineers use this skill to classify camera motion in video as Stay, Dolly, Pan, Tilt, or Roll, including multiple labels per frame. It also guides threshold tuning, temporal smoothing, and interval compression for frame-level camera-motion results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows may process private or sensitive video content.

Mitigation: Review future code before use and process only approved video data in an appropriate environment.

Risk: Heuristic thresholds and direction conventions can produce incorrect camera-motion labels if they are not calibrated for the video source.

Mitigation: Validate thresholds, direction conventions, and fallback behavior on representative footage before relying on the labels.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with Python pseudocode and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces camera-motion label logic, tuning guidance, and self-checks; no executable files are installed.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
