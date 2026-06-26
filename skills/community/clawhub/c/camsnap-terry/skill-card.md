## Description: <br>
Take camera snapshots and save them to disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture a single image from the default webcam and save it locally when a user requests a photo or snapshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill activates the default webcam and saves live camera images locally. <br>
Mitigation: Use it only after a clear user request for a photo, verify the saved path, and delete retained images that should not persist. <br>
Risk: User-supplied paths are passed through a shell command in a way the security evidence flags as risky. <br>
Mitigation: Use simple output paths without shell metacharacters and prefer structurally passed or quoted arguments in future revisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown status text with a local image file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a locally saved image file, typically under ./snapshots/ when no output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
