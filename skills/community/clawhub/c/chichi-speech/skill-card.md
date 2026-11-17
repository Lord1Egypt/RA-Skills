## Description:

A RESTful service for high-quality text-to-speech using Qwen3 and specialized voice cloning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hudeven](https://clawhub.ai/user/hudeven)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run a local FastAPI text-to-speech service, reuse a reference voice prompt, and call a synthesis endpoint that returns generated speech audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The synthesis server can expose an unauthenticated API.

Mitigation: Bind it to 127.0.0.1 unless intentional exposure is required, and place authentication or a trusted reverse proxy in front of any exposed deployment.

Risk: Text-to-speech generation is resource-heavy and may be abused or overloaded.

Mitigation: Add rate limits, request size limits, and operational monitoring before production use.

Risk: Voice cloning can misuse reference audio or clone a voice without authorization.

Mitigation: Use only reference audio that the operator is authorized to clone and review voice sample handling before release.

Risk: Runtime dependencies and model packages affect production security and reliability.

Mitigation: Pin, scan, and review dependencies before deploying the service in a production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hudeven/skills/chichi-speech)
- [Default Qwen3-TTS reference audio sample](https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-TTS-Repo/clone_2.wav)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Files]

**Output Format:** [Markdown guidance with inline shell commands, Python service code, HTTP requests, and generated WAV audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The service exposes a POST /synthesize endpoint and streams audio/wav responses.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
