## Description:

Transcribes recordings with Alibaba Bailian Fun-ASR, supporting Chinese, English, automatic language detection, and speaker diarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can transcribe recordings for subtitles, meeting notes, or searchable text, with optional speaker separation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and could not verify the dLazy login flow or credential handling.

Mitigation: Review the CLI login and key-storage behavior before authenticating, and use an API key you can rotate or revoke.

Risk: Audio supplied as a local file is uploaded to dLazy media storage for hosted transcription.

Mitigation: Submit only recordings approved for external processing, and review the service's data handling terms before sending sensitive audio.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-fun-asr)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON transcription response containing recognized speech, with optional speaker labels and audio-event tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an asynchronous task identifier when requested.]

## Skill Version(s):

1.3.42 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
