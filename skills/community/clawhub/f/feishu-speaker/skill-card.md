## Description:

Feishu Speaker lets an agent transcribe Feishu voice messages with Whisper and send text-to-speech voice replies through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tel18610240060-collab](https://clawhub.ai/user/tel18610240060-collab)

### License/Terms of Use:

MIT License

## Use Case:

Developers and agent operators use this skill to add Feishu voice interaction workflows, including local voice transcription, text-to-speech generation, and sending voice replies to configured Feishu recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send audio through Feishu using a local app secret and an embedded default recipient.

Mitigation: Use only Feishu apps and recipient IDs you control, remove embedded default app and recipient values, and require explicit recipient and file inputs before sending.

Risk: Secrets may be exposed through command arguments or shell process details during Feishu API calls.

Mitigation: Keep the Feishu app secret in a protected local credential file and avoid passing secrets through process arguments or logs.

Risk: Unpinned dependencies and shell interpolation behavior can make execution results harder to review before installation.

Mitigation: Pin dependencies, review the shell script before use, and fix the python3 -c interpolation issue identified by the security guidance.

## Reference(s):

- [Feishu Developer Console](https://open.feishu.cn/app/)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu File Upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May transcribe local audio files, generate speech audio, and send audio messages when the generated commands are executed.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
