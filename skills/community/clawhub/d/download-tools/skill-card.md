## Description:

CLI download tools for YouTube and WeChat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jqlong17](https://clawhub.ai/user/jqlong17)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to run CLI helpers that download WeChat article text and extract YouTube audio as MP3 files from user-provided URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts make outbound requests to URLs supplied by the user.

Mitigation: Use trusted YouTube and WeChat URLs and avoid running the scripts with elevated privileges.

Risk: The scripts write local output files and use temporary files during processing.

Mitigation: Run them in an intended working directory, choose safe output names, and add overwrite prompts or safer temporary-file handling before routine use.

Risk: The YouTube helper depends on locally installed command-line tools.

Mitigation: Install yt-dlp and ffmpeg from trusted package sources and keep them updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jqlong17/skills/download-tools)
- [Publisher profile](https://clawhub.ai/user/jqlong17)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown with inline bash code blocks and command-line file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates .txt files for WeChat articles and .mp3 files for YouTube audio in the current working directory when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
