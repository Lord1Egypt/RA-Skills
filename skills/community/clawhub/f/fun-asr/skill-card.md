## Description:

Fun-ASR speech recognition transcribes audio files with the Aliyun DashScope API when an agent receives audio or a transcription request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengzhendong](https://clawhub.ai/user/pengzhendong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to transcribe local audio files such as WAV, MP3, M4A, FLAC, and OGG files into text through Alibaba Cloud DashScope Fun-ASR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted audio is processed by Alibaba Cloud DashScope.

Mitigation: Avoid sending confidential, regulated, or consent-sensitive recordings unless that cloud processing is acceptable for the use case.

Risk: Python dependencies are installed at runtime and may vary by environment.

Mitigation: Install the skill in a virtual environment and use reviewed dependency versions where possible.

Risk: The artifact grants WebSearch permission even though the skill behavior centers on DashScope transcription.

Mitigation: Remove the unnecessary WebSearch permission before deployment if it is not needed.

## Reference(s):

- [ClawHub Fun-ASR skill page](https://clawhub.ai/pengzhendong/skills/fun-asr)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text transcription with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DASHSCOPE_API_KEY environment variable and sends submitted audio to Alibaba Cloud DashScope for processing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
