## Description:

Arch Video Cut automates architectural video editing by merging clips, adding timed subtitles and background music, and producing landscape and portrait MP4 outputs with saved editing preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baushua](https://clawhub.ai/user/baushua)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, architects, and developers use this skill to turn local architectural footage and narration into short videos in landscape and portrait formats. It is useful when repeated edits should reuse saved subtitle, audio, and duration preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell commands are built from editable saved preferences, which can create command-execution risk if preference files are untrusted or shared.

Mitigation: Install and run only in a contained workspace with trusted media and trusted config/user_preferences.json; review or patch subprocess command construction before installation.

Risk: The workflow overwrites fixed output video paths and writes local editing preference history.

Mitigation: Run on copies of input media, review the data/ output directory before each run, and disable or clear learning preferences when retaining local edit history is undesirable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baushua/skills/arch-video-cut)
- [Publisher profile](https://clawhub.ai/user/baushua)
- [Author website](http://www.ual-studio.com/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated MP4 files and JSON preferences on disk]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces fixed landscape and portrait output filenames under data/ and writes local preference history when learning is enabled.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
