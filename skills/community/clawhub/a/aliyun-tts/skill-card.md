## Description:

Alibaba Cloud Text-to-Speech synthesis service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guang384](https://clawhub.ai/user/guang384)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to synthesize text into Alibaba Cloud TTS audio files and include generated voice replies in chat responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The token request uses unencrypted HTTP, which can expose temporary service credentials on the network.

Mitigation: Review before installing and avoid use on untrusted networks unless the token request is changed to HTTPS.

Risk: Aliyun access credentials are account-sensitive.

Mitigation: Store credentials only in trusted configuration, avoid sharing or committing config files, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guang384/skills/aliyun-tts)
- [ClawHub publisher profile](https://clawhub.ai/user/guang384)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Aliyun app key, access key ID, and access key secret; default output is an MP3 file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
