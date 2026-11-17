## Description:

通过 AIOZ Stream API 以默认配置上传本地音频文件，并返回 HLS 流媒体播放链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, media teams, and developers use this skill to upload chosen audio files to AIOZ Stream, trigger server-side transcoding, and retrieve HLS links for publication or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill transmits local audio files to an external AIOZ Stream upload endpoint using user credentials.

Mitigation: Require explicit user confirmation for the chosen file before upload, avoid private or regulated recordings, and prefer upload-limited keys.

Risk: Server evidence flags the hard-coded upload endpoint and broad command guidance as requiring review.

Mitigation: Verify the endpoint with the user's AIOZ account or official documentation before use, and constrain commands to the documented upload flow.

Risk: AIOZ Stream credentials are included in HTTP request headers during API calls.

Mitigation: Collect credentials securely, avoid logging or storing them, and rotate keys if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/audio-upload-aioz-stream-free)
- [AIOZ Stream create endpoint](https://api-w3stream.attoaioz.cyou/api/videos/create)
- [AIOZ Stream part upload endpoint](https://api-w3stream.attoaioz.cyou/api/videos/AUDIO_ID/part)
- [AIOZ Stream complete endpoint](https://api-w3stream.attoaioz.cyou/api/videos/AUDIO_ID/complete)
- [AIOZ Stream audio detail endpoint](https://api-w3stream.attoaioz.cyou/api/videos/AUDIO_ID)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and HLS link text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided AIOZ Stream public and secret keys plus a local audio file path; returns an HLS link after asynchronous transcoding when available.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
