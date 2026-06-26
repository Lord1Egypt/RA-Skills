## Description: <br>
Control the local computer's built-in camera for capturing photos and basic operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddjj0](https://clawhub.ai/user/dddjj0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent list local cameras, preview a webcam, and capture photos for later analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access the local webcam and captured images may include sensitive surroundings. <br>
Mitigation: Run capture or preview only after user intent is clear, and review or delete files in ~/.openclaw/workspace/captures/ as needed. <br>
Risk: The skill saves captured photos locally by default. <br>
Mitigation: Use explicit output paths when needed and manage captured files according to local privacy requirements. <br>


## Reference(s): <br>
- [Camera Capture on ClawHub](https://clawhub.ai/dddjj0/camera-capture) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text stdout path and JPEG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Captured photos are saved locally under ~/.openclaw/workspace/captures/ by default.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
