## Description:

Local text-to-speech using Alibaba's CosyVoice3 on macOS Apple Silicon, with multilingual synthesis, Chinese dialect support, zero-shot voice cloning, cross-lingual synthesis, and fine-grained control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhuaizhong](https://clawhub.ai/user/lhuaizhong)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to install and run local speech synthesis on macOS Apple Silicon, including multilingual TTS, reference-audio voice cloning, dialect output, and audio file generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs mutable third-party code and downloads unverified components at install time.

Mitigation: Review or pin versions and hashes for Anaconda, the CosyVoice repository and submodules, PyPI/PyTorch packages, and ModelScope model artifacts before installation; run the skill as an unprivileged user.

Risk: Voice cloning can misuse a speaker's identity if reference audio is used without consent.

Mitigation: Use reference audio only when the speaker has consented to the intended synthesis, and keep generated audio aligned with that permission.

## Reference(s):

- [CosyVoice GitHub](https://github.com/FunAudioLLM/CosyVoice)
- [Fun-CosyVoice3 Demo](https://funaudiollm.github.io/cosyvoice3/)
- [ClawHub Skill Page](https://clawhub.ai/lhuaizhong/skills/cosyvoice3-macos)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, audio files]

**Output Format:** [Markdown guidance with inline bash and Python examples; generated speech is saved as WAV audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local macOS Apple Silicon, Conda/Python setup, model downloads, and optional reference audio for voice cloning.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
