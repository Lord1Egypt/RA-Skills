## Description: <br>
Create and edit macOS hackathon demo clips via terminal commands to record, crop, trim, and apply presets using ffmpeg and ffprobe locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and hackathon participants use this skill on macOS to prepare short demo videos locally from terminal workflows, including screen capture, cropping, trimming, and recording presets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screen recording can accidentally capture sensitive windows, notifications, or desktop content. <br>
Mitigation: Close sensitive windows and notifications before recording, and grant Screen Recording permission only to a trusted terminal app. <br>
Risk: ffmpeg commands can overwrite existing output files during record, crop, trim, or preset operations. <br>
Mitigation: Verify input and output paths before running crop or trim commands and choose non-conflicting output filenames. <br>
Risk: The skill depends on local ffmpeg and ffprobe binaries. <br>
Mitigation: Use trusted ffmpeg and ffprobe installations and confirm they are present before relying on the generated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edmonddantesj/aoi-demo-clip-maker) <br>
- [Publisher profile](https://clawhub.ai/user/edmonddantesj) <br>
- [Support issues](https://github.com/edmonddantesj/aoi-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local video files through ffmpeg and ffprobe commands run by the user.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
