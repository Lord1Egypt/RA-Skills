## Description: <br>
Create product demo videos by automating browser interactions and capturing frames with Playwright CDP screencast, then encoding them with FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xs4m1337](https://clawhub.ai/user/0xs4m1337) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and product teams use this skill to plan, record, and encode web application demos, walkthroughs, product showcases, and interactive videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recording script can capture visible browser content, including sensitive data shown during a demo. <br>
Mitigation: Use a dedicated demo browser profile with sanitized data, confirm the target page before recording, and review generated frames and videos before sharing. <br>
Risk: The recorder replaces files in its configured frame output directory. <br>
Mitigation: Point output paths at disposable demo folders and keep unrelated files out of those directories. <br>


## Reference(s): <br>
- [Demo planning guide](references/demo-planning.md) <br>
- [ClawHub skill page](https://clawhub.ai/0xs4m1337/demo-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; generated artifacts can include JPEG frames and MP4, GIF, or WebM videos.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records visible browser contents through Playwright CDP and encodes frame sequences with FFmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
