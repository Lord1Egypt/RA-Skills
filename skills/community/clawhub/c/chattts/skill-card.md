## Description:

High-quality, conversational Text-to-Speech (TTS) generation via local ChatTTS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djttt](https://clawhub.ai/user/djttt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate conversational speech from text through a ChatTTS server, with optional controls for seed, temperature, and top-p sampling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to a plaintext HTTP endpoint configured by default to a private-network address.

Mitigation: Use the skill only with a trusted ChatTTS server; prefer setting CHATTTS_API_URL to a loopback or HTTPS endpoint under your control.

Risk: Sensitive input text could be exposed to the configured TTS service.

Mitigation: Avoid submitting sensitive text unless the endpoint is local, protected, and approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djttt/skills/chattts)
- [Publisher profile](https://clawhub.ai/user/djttt)
- [Configured ChatTTS API endpoint](http://172.23.252.114:8020)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Command-line output containing the absolute local path to a generated .wav audio file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a reachable ChatTTS FastAPI server; CHATTTS_API_URL can override the default endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
