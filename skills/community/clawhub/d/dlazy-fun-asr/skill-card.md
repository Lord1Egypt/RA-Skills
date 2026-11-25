## Description:

Transcribes recordings with Alibaba Bailian Fun-ASR, supporting Chinese, English, multilingual recognition, automatic language detection, and speaker diarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to transcribe audio recordings for subtitles, meeting notes, and searchable text, with optional language selection and speaker separation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment notes an unexplained `dlazy` login and CLI in a transcription skill, and the scanner did not establish the CLI’s internal behavior.

Mitigation: Review the CLI package and its documented data flow before installing it or sending recordings; use only recordings you are comfortable processing through the documented service.

## Reference(s):

- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON transcription results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include speaker labels and asynchronous task status.]

## Skill Version(s):

1.3.45 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
