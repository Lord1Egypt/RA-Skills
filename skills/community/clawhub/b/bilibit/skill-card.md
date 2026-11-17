## Description:

bilibit helps agents download Bilibili videos and optional danmaku from user-provided URLs without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aoturlab](https://clawhub.ai/user/aoturlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a simple CLI workflow for downloading Bilibili videos, optional danmaku XML, selected quality levels, and local download history from a supplied video URL. The skill is URL-driven and does not provide Bilibili search, playback, account management, cloud storage, editing, or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can automatically download a third-party BBDown executable from GitHub without cryptographic verification.

Mitigation: Install BBDown separately from a trusted source when possible and review the executable provenance before using the skill.

Risk: The exported bbdown wrapper runs through a shell-enabled child process and may expose shell metacharacters in arguments to unintended command execution.

Mitigation: Avoid untrusted or unsanitized arguments, run the tool with least privilege, and do not use it from privileged automation.

Risk: Cookie files may be needed for premium quality downloads and local history is written under the user's home directory.

Mitigation: Pass cookie files only when necessary, protect cookie file permissions, and inspect or clear ~/.bilibit/history.json when history retention is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aoturlab/skills/bilibit)
- [Project link from artifact docs](https://github.com/AoturLab/bilibit)
- [Issue tracker from artifact docs](https://github.com/AoturLab/bilibit/issues)
- [npm package](https://www.npmjs.com/package/bilibit)
- [BBDown releases](https://github.com/nilaoda/BBDown/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with CLI commands and preserved command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download video files, danmaku XML, and local history records through the bilibit and BBDown command-line tools.]

## Skill Version(s):

0.1.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
