## Description: <br>
Automates architecture video editing by merging clips, adding subtitles and background music, and producing landscape and portrait outputs with learned editing preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baushua](https://clawhub.ai/user/baushua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content editors use this skill to run a local FFmpeg-based workflow for short architecture videos, including clip merging, subtitle creation, background audio mixing, and dual-format export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editable local preferences and file paths are used by shell commands during media processing. <br>
Mitigation: Inspect or recreate config/user_preferences.json before use, avoid importing preference files from untrusted sources, and review local paths before running the workflow. <br>
Risk: The workflow uses hardcoded local audio and output paths. <br>
Mitigation: Confirm the expected audio path and generated output filenames before execution. <br>
Risk: Preference and history data plus generated media files are written locally, and the documented learning opt-out may not be enforced. <br>
Mitigation: Run the skill only in a workspace where local history and generated media are acceptable, and reset or remove preferences after use when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baushua/arch-video-cut) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SELF_LEARNING_GUIDE.md](artifact/SELF_LEARNING_GUIDE.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and local media file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local MP4 video files and writes preference/history data under the skill directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
