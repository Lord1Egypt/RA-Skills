## Description: <br>
Helps agents create Chinese subtitles for ffmpeg workflows by rendering subtitle text onto images with Pillow before video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media automation agents use this skill to add Chinese subtitle text to images and compose simple subtitle-bearing videos while avoiding Windows ffmpeg text encoding issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted Pillow, ffmpeg, or ffprobe installations can introduce dependency or binary execution risk. <br>
Mitigation: Install Pillow and ffmpeg/ffprobe only from trusted sources. <br>
Risk: Example ffmpeg commands can overwrite existing media outputs without prompting. <br>
Mitigation: Review output paths before running commands and avoid reusing paths for files that must be preserved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/systiger/ffmpeg-chinese-subtitle) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/systiger) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local media paths, font settings, subtitle text, and output filenames supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
