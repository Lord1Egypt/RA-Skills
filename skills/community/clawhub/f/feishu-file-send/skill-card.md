## Description:

Sends files to Feishu, including images, audio, documents, and other file types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tazio7](https://clawhub.ai/user/tazio7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an agent needs to send workspace files through Feishu with an optional caption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send private, personal, or business-sensitive workspace files unintentionally.

Mitigation: Confirm the exact file path and contents before sending a file through Feishu.

Risk: File sending can fail or reach the wrong workflow when the file path is outside the expected workspace or when the wrong message parameter is used.

Mitigation: Use an absolute workspace path through media, file_path, or path, and avoid using the message parameter for files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tazio7/skills/feishu-file-send)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Code]

**Output Format:** [Markdown guidance with Python-style Feishu message tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses workspace file paths and optional captions for file delivery through Feishu.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
