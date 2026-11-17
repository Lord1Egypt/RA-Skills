## Description:

Transcribes recorded audio files through ByteDance/Volcengine Doubao Seed-ASR 2.0, with Chinese-focused speech recognition, speaker diarization, JSON output, and SRT subtitle export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahnxu](https://clawhub.ai/user/vahnxu)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, operators, and external users use this skill to configure Volcengine credentials and transcribe recorded audio, meeting recordings, or voice memos into speaker-labeled text, JSON, or SRT subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio is sent to Volcengine for transcription and local files are uploaded to the user's Volcengine TOS bucket.

Mitigation: Use a dedicated TOS bucket, least-privileged Volcengine credentials, lifecycle deletion for uploaded recordings, and avoid confidential audio unless Volcengine retention and compliance terms fit the use case.

Risk: Incorrect bucket permissions can prevent transcription or expose recordings if users make objects public as a workaround.

Mitigation: Grant read and write access through the scoped bucket policy described by the skill, and avoid public-read object ACLs except as a temporary diagnostic.

Risk: Using an unreviewed dependency version could change the code that handles audio, credentials, and network requests.

Mitigation: Install the pinned dependency set from requirements.txt and re-review the skill before changing dependency versions.

## Reference(s):

- [Volcengine Doubao Audio File Recognition 2.0 Documentation](https://www.volcengine.com/docs/6561/1354868)
- [ClawHub Doubao Asr Skill Page](https://clawhub.ai/vahnxu/skills/doubao-asr)

## Skill Output:

**Output Type(s):** [text, JSON, SRT subtitles, shell commands, configuration guidance]

**Output Format:** [Plain text transcripts, JSON service responses, SRT subtitle files, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write transcript outputs under the working directory or /tmp; the offpeak tier can return a request ID for later retrieval.]

## Skill Version(s):

0.23.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
