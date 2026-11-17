## Description:

Guides an agent through installing the Python biliup CLI, logging in to Bilibili with QR authorization, collecting upload metadata, submitting videos, and reporting upload results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pokerskun](https://clawhub.ai/user/pokerskun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content publishers use this skill to prepare and upload local videos to a Bilibili account through the biliup command-line tool. It helps the agent handle setup, QR login, metadata collection, category selection, upload execution, and result reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install Python packages before upload operations.

Mitigation: Review the installation step, prefer an isolated environment such as pipx when available, and proceed only if installing biliup and QR-code dependencies is acceptable.

Risk: Bilibili login stores an access credential in cookies.json.

Mitigation: Keep cookies.json private, avoid committing or sharing it, and remove or rotate it when it is no longer needed.

Risk: The upload workflow can publish videos to the user's Bilibili account.

Mitigation: Confirm the target account, video files, title, tags, category, copyright setting, and source information before running the upload command.

Risk: The workflow can download user-provided video URLs before upload.

Mitigation: Use trusted URLs and verify downloaded files before submitting them to Bilibili.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/pokerskun/skills/biliup-skills)
- [Publisher profile](https://clawhub.ai/user/pokerskun)
- [Bilibili category tid list](references/tid_list.md)
- [biliup project](https://github.com/biliup/biliup)
- [Bilibili upload category reference](https://member.bilibili.com/platform/upload/video/frame)
- [pip installation documentation](https://pip.pypa.io/en/stable/installation/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files, Markdown]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference a QR-code PNG and a local cookies.json credential file during login.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
