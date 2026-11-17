## Description:

Speech-to-text skill that uses Qwen3-ASR-0.6B to transcribe audio, with claimed support for 22 Chinese dialects and multiple languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yszheda](https://clawhub.ai/user/yszheda)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to convert uploaded or webhook audio messages into text for downstream agent conversations. It supports optional language or dialect selection and returns structured transcription results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated audio processing is exposed on all network interfaces.

Mitigation: Deploy only in a contained local or private environment, bind the service to 127.0.0.1 when possible, and add authentication before wider network exposure.

Risk: Webhook and audio payload handling may accept unsafe inputs, including URLs or filesystem paths.

Mitigation: Validate webhook signatures, reject arbitrary URLs and filesystem paths, enforce audio type and size limits, and keep temporary audio cleanup enabled.

Risk: ASR inference can be resource intensive and may degrade host availability under load.

Mitigation: Rate-limit requests, cap inference concurrency, and set deployment resource limits appropriate for the model's memory and CPU requirements.

Risk: Unpinned dependencies and model downloads can change behavior across installations.

Mitigation: Pin Node.js and Python dependencies and review model source, version, and license before deployment.

Risk: The broad process stop command may terminate unrelated Node.js processes.

Mitigation: Replace it with a skill-specific process manager or PID-based stop mechanism.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yszheda/skills/asr-skill)
- [README](artifact/README.md)
- [Installation guide](artifact/INSTALL.md)
- [Developer guide](artifact/DEVELOPER-GUIDE.md)
- [Skill configuration](artifact/skill.yml)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON response containing transcription text, detected language or dialect, confidence, and duration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps or alignment data when those options are enabled.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact package and changelog reference 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
