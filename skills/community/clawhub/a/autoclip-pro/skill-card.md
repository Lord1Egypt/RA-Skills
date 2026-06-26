## Description: <br>
AutoClip Pro helps video creators batch process local video folders with FFmpeg-based resizing, trimming, watermarking, transitions, thumbnails, and style templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdp6539](https://clawhub.ai/user/gdp6539) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External video creators, media operators, and developers use this skill to configure and run local batch video processing workflows for short-form, educational, vlog, entertainment, and ecommerce content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell-built FFmpeg commands may mishandle untrusted filenames, paths, or configuration values. <br>
Mitigation: Run only in a limited test folder with trusted files, avoid shell metacharacters in filenames, and prefer a future implementation that invokes FFmpeg with argument arrays and shell:false. <br>
Risk: Promotional playbooks are included beside the operational video-processing files and may distract from technical review. <br>
Mitigation: Treat the sales and promotion documents as non-operational material and review or remove them before deployment. <br>
Risk: Documentation refers to install.bat and run.bat, but those files are not present in the release evidence. <br>
Mitigation: Use the documented manual Node.js command path or update the release to include accurate launcher files. <br>


## Reference(s): <br>
- [AutoClip Pro ClawHub release](https://clawhub.ai/gdp6539/autoclip-pro) <br>
- [gdp6539 publisher profile](https://clawhub.ai/user/gdp6539) <br>
- [Node.js](https://nodejs.org) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Windows FFmpeg builds](https://www.gyan.dev/ffmpeg/builds/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown instructions, JSON configuration, command-line progress text, processed MP4 files, and generated thumbnail images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Node.js and FFmpeg; reads videos from an input folder and writes processed outputs to an output folder.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and package.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
