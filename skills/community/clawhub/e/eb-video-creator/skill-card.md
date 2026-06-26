## Description: <br>
Creates videos from scratch using ffmpeg, programming, and assets for tutorials, presentations, social videos, slideshows, demos, narrated videos, and other video formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emersonbraun](https://clawhub.ai/user/emersonbraun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to plan, script, and generate videos with ffmpeg, Python, and local media assets. It is suited for reproducible video assembly, format conversion, overlays, subtitles, audio handling, and platform-specific exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated media-processing commands can overwrite, transform, or delete local files if run in the wrong directory. <br>
Mitigation: Review generated scripts and run them in a dedicated working folder with copies of input assets. <br>
Risk: Video workflows may download, remix, or publish media without confirming reuse rights. <br>
Mitigation: Use only media you own or are licensed to use, and confirm platform and rights requirements before publishing. <br>
Risk: Local ffmpeg, Python, ImageMagick, yt-dlp, sox, or transcription commands may execute with the user's filesystem permissions. <br>
Mitigation: Install tools from trusted sources, inspect commands before execution, and avoid running generated scripts against sensitive folders. <br>


## Reference(s): <br>
- [FFmpeg Recipes](references/ffmpeg-recipes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/emersonbraun/eb-video-creator) <br>
- [Publisher Profile](https://clawhub.ai/user/emersonbraun) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable local media-processing commands and generated scripts for video creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
