## Description: <br>
Standardize video sampling and frame indexing so interval instructions and mask frames stay aligned with a valid key/index scheme. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose a video sampling stride or FPS and keep interval instructions, frame masks, and other per-frame artifacts aligned to the same valid frame indices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Frame sampling or interval boundaries can drift from downstream masks or per-frame artifacts. <br>
Mitigation: Check that sample IDs are strictly increasing, stay below the total frame count, and match the documented interval and artifact coverage policy. <br>
Risk: The agent may read the wrong local video path or assume an unavailable video-reading runtime. <br>
Mitigation: Confirm the intended input video path before use and verify that the runtime has an appropriate video-reading library such as OpenCV. <br>
Risk: Future releases could add scripts, dependencies, or broader file access not covered by the current clean scan. <br>
Mitigation: Review and scan each new version before installing or using it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code] <br>
**Output Format:** [Markdown with Python pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on sampled video frame IDs, interval keys, and per-frame artifact consistency checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
