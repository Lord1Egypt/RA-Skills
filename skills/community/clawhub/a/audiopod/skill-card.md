## Description:

AudioPod guides agents in using AudioPod AI's API for music generation, stem separation, text-to-speech, noise reduction, transcription, speaker separation, media extraction, and wallet management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rakesh1002](https://clawhub.ai/user/rakesh1002)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to generate and process audio through AudioPod AI APIs, including creating music or speech, separating stems or speakers, transcribing media, cleaning noisy audio, and checking wallet usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio, URLs, text, lyrics, transcripts, voice samples, and job metadata may be sent to AudioPod for remote processing.

Mitigation: Submit only material the user is authorized to process, and avoid confidential, regulated, copyrighted, or third-party voice material unless use is permitted.

Risk: The skill relies on an AudioPod API key for authenticated requests.

Mitigation: Store AUDIOPOD_API_KEY in an environment variable or secret manager, avoid hardcoding it in prompts or files, and do not expose it in logs.

Risk: AudioPod jobs can consume wallet credits.

Mitigation: Use wallet balance, pricing, and cost-estimate endpoints before submitting long or high-volume processing jobs.

## Reference(s):

- [AudioPod Skill on ClawHub](https://clawhub.ai/rakesh1002/skills/audiopod)
- [Stem Separation Reference](artifact/references/stems.md)
- [Text to Speech Reference](artifact/references/tts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, Node.js, cURL, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AUDIOPOD_API_KEY; AudioPod API operations may return job IDs, status JSON, and output URLs.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
