## Description: <br>
Capture photos from MacBook webcams using documented ffmpeg commands for Brio and FaceTime HD camera views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users ask an agent to capture front, side, or multi-angle photos from local MacBook-connected webcams for inspection or visual context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate local Mac cameras and save captured media to /tmp. <br>
Mitigation: Use only when the user explicitly asks for photos, and review or delete /tmp/brio.jpg, /tmp/facetime.jpg, and warmup MP4 files after use if the media should not be retained. <br>
Risk: Camera capture may fail or capture the wrong angle if another camera app is open or the FaceTime camera command omits its required pixel format. <br>
Mitigation: Close other camera applications before capture and use the documented FaceTime command with -pixel_format nv12. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JPEG photos in /tmp and temporary warmup MP4 files when the documented commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
