## Description:

Audio denoising skill for removing background noise from user-provided recordings with Alibaba Cloud DashScope/FunAudioDenoise, supporting common formats such as wav, mp3, aac, opus, amr, and pcm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songguocola](https://clawhub.ai/user/songguocola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and audio workflow operators use this skill to denoise recordings, prepare audio for speech recognition, and improve meeting, podcast, interview, education, and audiobook audio quality. It can be used through a command-line interface or imported Python API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User audio is uploaded to Alibaba Cloud/DashScope for processing and may contain sensitive personal, business, or biometric information.

Mitigation: Only process audio the user is authorized to upload, and handle recordings according to the user's privacy, consent, and data-retention requirements.

Risk: Runtime behavior depends on external Python packages and a DashScope API key.

Mitigation: Install the skill in a virtual environment, pin dependency versions where practical, and keep API keys in environment variables or a managed secret store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songguocola/skills/fun-denoise)
- [Denoise.py source reference](audio_process/Denoise.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces denoised audio files and processing metadata when run by the user with a valid DashScope API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
