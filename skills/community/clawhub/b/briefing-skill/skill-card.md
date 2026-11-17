## Description:

Automatically tracks creator channels on YouTube, Bilibili, and TikTok, transcribes new videos, and uses memory-based updates to avoid duplicate downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yutaigu](https://clawhub.ai/user/yutaigu)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to operate the briefing CLI for tracking creator channels, managing source URLs and configuration, and returning newly generated transcript text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-run bootstrap can execute shell commands, request sudo, install system and Python packages, and create a persistent launcher.

Mitigation: Review and run the installer manually when possible, prefer a user-local install path, and confirm each privileged or persistent change before enabling the skill.

Risk: The installer can download mutable remote code and current dependencies.

Mitigation: Review or pin the remote repository and dependency set before installation.

Risk: The installer can edit shell startup files to add the launcher directory to PATH.

Mitigation: Inspect profile file changes and remove the added PATH entry if it is not wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yutaigu/skills/briefing-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and transcript text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read transcript files from output/<filename>/whisper.txt after the CLI reports [WHISPER DONE].]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
