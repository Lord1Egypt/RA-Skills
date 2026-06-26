## Description: <br>
Estimate camera motion from video using optical flow and affine or homography transforms, with multi-label classification per frame. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide an agent in classifying camera motion in video as stay, dolly, pan, tilt, or roll, including multiple labels on the same frame. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video inputs may contain sensitive visual content. <br>
Mitigation: Avoid giving an agent sensitive videos unless the user is comfortable with that agent processing their visual contents. <br>
Risk: Heuristic motion classification can be wrong when thresholds, frame rate, resolution, texture, lighting, or direction conventions are not validated. <br>
Mitigation: Tune thresholds to the footage, validate direction conventions, use an identity-transform fallback on tracking failure, and review compressed intervals before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/dynamic-object-aware-egomotion-egomotion-estimation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code] <br>
**Output Format:** [Markdown with Python code block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no credentials, network access, installation hooks, persistence, or privileged actions requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
