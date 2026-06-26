## Description: <br>
Generates a talking digital human video from a portrait image plus either uploaded audio or text-based speech, then returns a public video link when processing completes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[focus-aim](https://clawhub.ai/user/focus-aim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create digital human talking videos from a user-provided image and audio or text, including preset voice or voice-clone speech generation. It helps automate job submission, polling, task-status review, and retrieval of the resulting public video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive face images, voice samples, generated speech, and digital-human video outputs. <br>
Mitigation: Use only images, audio, and voice samples that the user has rights and consent to upload, and review generated videos before sharing. <br>
Risk: Returned video URLs should be treated as public or shareable links. <br>
Mitigation: Avoid submitting sensitive media unless public-link exposure is acceptable, and manage or delete generated links and local task history when they are no longer needed. <br>
Risk: The skill requires an aim-secret-key and stores local runtime configuration. <br>
Mitigation: Prefer a secure secrets mechanism or out-of-band setup, use scoped and revocable credentials, never commit .env, and delete .env and .task-history.jsonl when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/focus-aim/aim-digital-human-video) <br>
- [AIM skills registration](https://tools.mentarc.cn/aim-skills/) <br>
- [FFmpeg and ffprobe](https://ffmpeg.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated media result is returned as a public video URL; task status may also be persisted locally for later polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
