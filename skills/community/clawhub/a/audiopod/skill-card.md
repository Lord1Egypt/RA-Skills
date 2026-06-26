## Description: <br>
AudioPod helps agents use AudioPod AI APIs for music generation, stem separation, text-to-speech, noise reduction, transcription, speaker separation, and media extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rakesh1002](https://clawhub.ai/user/Rakesh1002) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and audio workflow agents use this skill to create or process audio through AudioPod AI, including generated music, separated stems, speech, cleaned recordings, transcripts, and extracted media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An AudioPod API key can create billable jobs and access usage, balance, jobs, or voices. <br>
Mitigation: Store the key in AUDIOPOD_API_KEY or another secret store, keep wallet exposure limited, and review billable requests before execution. <br>
Risk: Audio files, URLs, transcripts, and voice samples may include sensitive or third-party content. <br>
Mitigation: Submit only media the user has permission to process and avoid sending confidential or unauthorized material to AudioPod. <br>
Risk: Provider SDK or endpoint differences may cause failed or unintended text-to-speech requests. <br>
Mitigation: Follow the reference notes for raw HTTP TTS requests, including form data and the input_text field, when reliability matters. <br>


## Reference(s): <br>
- [AudioPod ClawHub listing](https://clawhub.ai/Rakesh1002/audiopod) <br>
- [Stem Separation Reference](references/stems.md) <br>
- [Text to Speech Reference](references/tts.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, JavaScript, cURL, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API requests, job IDs, output URLs, transcript formats, and wallet or usage checks through AudioPod.] <br>

## Skill Version(s): <br>
1.2.3 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
