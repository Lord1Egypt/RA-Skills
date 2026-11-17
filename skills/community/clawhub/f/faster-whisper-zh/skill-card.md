## Description:

使用 faster-whisper 进行本地语音转文字，支持 GPU 加速转录、词级时间戳和蒸馏模型。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapleshadow](https://clawhub.ai/user/mapleshadow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to transcribe local audio into Chinese-first text, timestamped segments, or JSON for meetings, interviews, notes, subtitles, podcasts, and other audio records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The batch transcription script can execute unintended shell commands when processing crafted filenames or options.

Mitigation: Avoid running the batch script on directories containing untrusted filenames until eval is removed; prefer the single-file transcribe.py path for trusted inputs.

Risk: The scripts force a third-party model mirror without clear opt-in.

Mitigation: Use the official Hugging Face endpoint unless the mirror is intentionally trusted, and set the model endpoint explicitly before running the skill.

Risk: Unpinned dependencies can make installs less reproducible.

Mitigation: Pin faster-whisper, torch, and model versions before production use or repeatable validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mapleshadow/skills/faster-whisper-zh)
- [faster-whisper project](https://github.com/guillaumekln/faster-whisper)
- [OpenAI Whisper project](https://github.com/openai/whisper)
- [PyTorch CUDA wheel index used by setup script](https://download.pytorch.org/whl/cu121)
- [Hugging Face mirror endpoint configured by scripts](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text transcripts or JSON transcription results, with agent guidance as Markdown containing shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include segment timestamps, word-level timestamps, language confidence, selected model, device, and compute type.]

## Skill Version(s):

1.0.5 (source: server release metadata, _meta.json, and artifact changelog dated 2026-04-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
