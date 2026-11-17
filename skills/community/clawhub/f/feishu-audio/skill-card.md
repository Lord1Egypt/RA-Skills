## Description:

Converts local audio files to Feishu-playable voice messages by using ffmpeg to create Opus audio, uploading the result to Feishu, and sending an audio message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyn1990](https://clawhub.ai/user/tianyn1990)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to send an existing or generated local audio file as a playable Feishu voice message to a specified Open ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads local audio to Feishu using user-provided Feishu app credentials.

Mitigation: Install and run it only when sending the selected audio through your own Feishu app is intended.

Risk: Audio may be sent to the wrong Feishu recipient if the receiver Open ID is incorrect.

Mitigation: Check the recipient Open ID before running the send script.

Risk: Sensitive local audio may be exposed through uploads or temporary files on shared machines.

Mitigation: Avoid sensitive audio on shared machines and review the temporary-file handling before routine use.

## Reference(s):

- [Feishu tenant_access_token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands, environment variables, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated workflow depends on ffmpeg, jq, Feishu app credentials, and a valid Feishu receiver Open ID.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
